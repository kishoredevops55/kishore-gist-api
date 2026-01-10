#!/bin/bash
# =============================================================================
# 🚀 COMPREHENSIVE MONITORING STACK DEPLOYMENT SCRIPT
# GitHub Gists API - Full Observability Stack
# Grafana + Prometheus + Loki + Tempo + Synthetic Monitoring
# =============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
MONITORING_NAMESPACE="monitoring"
GRAFANA_HOST="kishoregrafana.local"
CLUSTER_NAME="kind-dev"
METALLB_IP_RANGE="172.18.255.200-172.18.255.250"

echo -e "${PURPLE}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  🚀 COMPREHENSIVE MONITORING STACK DEPLOYMENT                  ║"
echo "║  GitHub Gists API - Full Observability                         ║"
echo "║  Grafana | Prometheus | Loki | Tempo | Synthetic Monitoring   ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# =============================================================================
# PRE-FLIGHT CHECKS
# =============================================================================
echo -e "\n${CYAN}[1/10] 🔍 Pre-flight Checks${NC}"

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}❌ kubectl is not installed${NC}"
    exit 1
fi

# Check if helm is available
if ! command -v helm &> /dev/null; then
    echo -e "${RED}❌ Helm is not installed${NC}"
    exit 1
fi

# Check cluster connection
if ! kubectl cluster-info &> /dev/null; then
    echo -e "${RED}❌ Cannot connect to Kubernetes cluster${NC}"
    exit 1
fi

echo -e "${GREEN}✅ All pre-flight checks passed${NC}"

# =============================================================================
# ADD HELM REPOSITORIES
# =============================================================================
echo -e "\n${CYAN}[2/10] 📦 Adding Helm Repositories${NC}"

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts 2>/dev/null || true
helm repo add grafana https://grafana.github.io/helm-charts 2>/dev/null || true
helm repo update

echo -e "${GREEN}✅ Helm repositories configured${NC}"

# =============================================================================
# CREATE MONITORING NAMESPACE
# =============================================================================
echo -e "\n${CYAN}[3/10] 🏗️  Creating Monitoring Namespace${NC}"

kubectl create namespace ${MONITORING_NAMESPACE} --dry-run=client -o yaml | kubectl apply -f -
kubectl label namespace ${MONITORING_NAMESPACE} istio-injection=enabled --overwrite 2>/dev/null || true

echo -e "${GREEN}✅ Namespace ${MONITORING_NAMESPACE} created${NC}"

# =============================================================================
# DEPLOY TEMPO (Distributed Tracing)
# =============================================================================
echo -e "\n${CYAN}[4/10] 🔍 Deploying Tempo (Distributed Tracing)${NC}"

helm upgrade --install tempo grafana/tempo \
    --namespace ${MONITORING_NAMESPACE} \
    --values monitoring/tempo-values.yaml \
    --wait --timeout 5m

echo -e "${GREEN}✅ Tempo deployed${NC}"

# =============================================================================
# DEPLOY LOKI (Log Aggregation)
# =============================================================================
echo -e "\n${CYAN}[5/10] 📝 Deploying Loki (Log Aggregation)${NC}"

helm upgrade --install loki grafana/loki-stack \
    --namespace ${MONITORING_NAMESPACE} \
    --values monitoring/loki-values.yaml \
    --wait --timeout 5m

echo -e "${GREEN}✅ Loki deployed${NC}"

# =============================================================================
# DEPLOY KUBE-PROMETHEUS-STACK (Prometheus + Grafana)
# =============================================================================
echo -e "\n${CYAN}[6/10] 📊 Deploying Prometheus + Grafana Stack${NC}"

helm upgrade --install kube-prometheus-stack prometheus-community/kube-prometheus-stack \
    --namespace ${MONITORING_NAMESPACE} \
    --values monitoring/kube-prometheus-stack-values.yaml \
    --set grafana.adminPassword=admin123 \
    --wait --timeout 10m

echo -e "${GREEN}✅ Prometheus + Grafana deployed${NC}"

# =============================================================================
# DEPLOY SYNTHETIC MONITORING
# =============================================================================
echo -e "\n${CYAN}[7/10] 🌐 Deploying Synthetic Monitoring${NC}"

kubectl apply -f monitoring/synthetic-monitoring.yaml -n ${MONITORING_NAMESPACE}

echo -e "${GREEN}✅ Synthetic monitoring deployed${NC}"

# =============================================================================
# IMPORT GRAFANA DASHBOARDS
# =============================================================================
echo -e "\n${CYAN}[8/10] 📈 Importing Grafana Dashboards${NC}"

# Create ConfigMap for dashboard
kubectl create configmap github-gists-api-dashboard \
    --from-file=github-gists-api.json=monitoring/grafana-complete-dashboard.json \
    --namespace ${MONITORING_NAMESPACE} \
    --dry-run=client -o yaml | kubectl apply -f -

# Label it for Grafana sidecar
kubectl label configmap github-gists-api-dashboard grafana_dashboard=1 -n ${MONITORING_NAMESPACE} --overwrite

echo -e "${GREEN}✅ Dashboards imported${NC}"

# =============================================================================
# CONFIGURE ISTIO GATEWAY FOR GRAFANA
# =============================================================================
echo -e "\n${CYAN}[9/10] 🔐 Configuring Grafana Ingress${NC}"

# Create Istio Gateway and VirtualService for Grafana
cat <<EOF | kubectl apply -f -
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: grafana-gateway
  namespace: ${MONITORING_NAMESPACE}
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "${GRAFANA_HOST}"
  - port:
      number: 443
      name: https
      protocol: HTTPS
    tls:
      mode: SIMPLE
      credentialName: grafana-tls-secret
    hosts:
    - "${GRAFANA_HOST}"
---
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: grafana-vs
  namespace: ${MONITORING_NAMESPACE}
spec:
  hosts:
  - "${GRAFANA_HOST}"
  gateways:
  - grafana-gateway
  http:
  - match:
    - uri:
        prefix: /
    route:
    - destination:
        host: kube-prometheus-stack-grafana.${MONITORING_NAMESPACE}.svc.cluster.local
        port:
          number: 80
EOF

echo -e "${GREEN}✅ Grafana Istio Gateway configured${NC}"

# =============================================================================
# CREATE TLS CERTIFICATE FOR GRAFANA
# =============================================================================
echo -e "\n${CYAN}[9b/10] 🔒 Creating TLS Certificate for Grafana${NC}"

# Create TLS certificate for Grafana
mkdir -p /tmp/grafana-certs
openssl req -x509 -sha256 -nodes -days 365 -newkey rsa:2048 \
    -subj "/O=Kishore/CN=${GRAFANA_HOST}" \
    -keyout /tmp/grafana-certs/grafana.key \
    -out /tmp/grafana-certs/grafana.crt 2>/dev/null

kubectl create secret tls grafana-tls-secret \
    --key=/tmp/grafana-certs/grafana.key \
    --cert=/tmp/grafana-certs/grafana.crt \
    -n istio-system \
    --dry-run=client -o yaml | kubectl apply -f -

rm -rf /tmp/grafana-certs

echo -e "${GREEN}✅ TLS certificate created${NC}"

# =============================================================================
# UPDATE DNS CONFIGURATION
# =============================================================================
echo -e "\n${CYAN}[10/10] 📡 DNS Configuration${NC}"

# Get Istio Ingress Gateway IP
INGRESS_IP=$(kubectl get svc istio-ingressgateway -n istio-system -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null || echo "pending")

if [ "$INGRESS_IP" == "pending" ] || [ -z "$INGRESS_IP" ]; then
    INGRESS_IP="172.18.255.200"
fi

echo -e "${YELLOW}📝 Add this to your hosts file (C:\\Windows\\System32\\drivers\\etc\\hosts):${NC}"
echo -e "${GREEN}${INGRESS_IP}    ${GRAFANA_HOST}${NC}"

# =============================================================================
# DEPLOYMENT SUMMARY
# =============================================================================
echo -e "\n${PURPLE}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  🎉 MONITORING STACK DEPLOYMENT COMPLETE!                      ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${CYAN}📊 Deployed Components:${NC}"
echo -e "  ├── ${GREEN}✅ Prometheus${NC} - Metrics collection"
echo -e "  ├── ${GREEN}✅ Grafana${NC} - Visualization"
echo -e "  ├── ${GREEN}✅ Loki${NC} - Log aggregation"
echo -e "  ├── ${GREEN}✅ Tempo${NC} - Distributed tracing"
echo -e "  └── ${GREEN}✅ Blackbox Exporter${NC} - Synthetic monitoring"

echo -e "\n${CYAN}🌐 Access URLs:${NC}"
echo -e "  ├── Grafana:     ${GREEN}https://${GRAFANA_HOST}${NC}"
echo -e "  ├── Prometheus:  ${GREEN}http://localhost:9090${NC} (port-forward)"
echo -e "  └── API:         ${GREEN}https://gists.kishore.local${NC}"

echo -e "\n${CYAN}🔐 Grafana Credentials:${NC}"
echo -e "  ├── Username: ${GREEN}admin${NC}"
echo -e "  └── Password: ${GREEN}admin123${NC}"

echo -e "\n${CYAN}📈 Available Dashboards:${NC}"
echo -e "  ├── GitHub Gists API - Complete Observability"
echo -e "  ├── Kubernetes / Compute Resources"
echo -e "  └── Istio Service Mesh Dashboard"

echo -e "\n${CYAN}🔧 Useful Commands:${NC}"
echo -e "  # Port-forward Grafana (alternative access):"
echo -e "  ${YELLOW}kubectl port-forward svc/kube-prometheus-stack-grafana 3000:80 -n monitoring${NC}"
echo -e ""
echo -e "  # Port-forward Prometheus:"
echo -e "  ${YELLOW}kubectl port-forward svc/kube-prometheus-stack-prometheus 9090:9090 -n monitoring${NC}"
echo -e ""
echo -e "  # View Tempo traces:"
echo -e "  ${YELLOW}kubectl port-forward svc/tempo 3200:3200 -n monitoring${NC}"
echo -e ""
echo -e "  # Check monitoring pods:"
echo -e "  ${YELLOW}kubectl get pods -n monitoring${NC}"

echo -e "\n${GREEN}🚀 Your complete observability stack is ready!${NC}"
