# =============================================================================
# 🚀 COMPREHENSIVE MONITORING STACK DEPLOYMENT SCRIPT (PowerShell)
# GitHub Gists API - Full Observability Stack
# Grafana + Prometheus + Loki + Tempo + Synthetic Monitoring
# =============================================================================

# Stop on first error
$ErrorActionPreference = "Stop"

# Configuration
$MONITORING_NAMESPACE = "monitoring"
$GRAFANA_HOST = "kishoregrafana.local"
$CLUSTER_NAME = "kind-dev"

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Magenta
Write-Host "║  🚀 COMPREHENSIVE MONITORING STACK DEPLOYMENT                  ║" -ForegroundColor Magenta
Write-Host "║  GitHub Gists API - Full Observability                         ║" -ForegroundColor Magenta
Write-Host "║  Grafana | Prometheus | Loki | Tempo | Synthetic Monitoring   ║" -ForegroundColor Magenta
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Magenta
Write-Host ""

# =============================================================================
# PRE-FLIGHT CHECKS
# =============================================================================
Write-Host "[1/10] 🔍 Pre-flight Checks" -ForegroundColor Cyan

# Check kubectl
try {
    kubectl version --client | Out-Null
    Write-Host "  ✅ kubectl is installed" -ForegroundColor Green
} catch {
    Write-Host "  ❌ kubectl is not installed" -ForegroundColor Red
    exit 1
}

# Check helm
try {
    helm version | Out-Null
    Write-Host "  ✅ Helm is installed" -ForegroundColor Green
} catch {
    Write-Host "  ❌ Helm is not installed" -ForegroundColor Red
    exit 1
}

# Check cluster
try {
    kubectl cluster-info | Out-Null
    Write-Host "  ✅ Connected to Kubernetes cluster" -ForegroundColor Green
} catch {
    Write-Host "  ❌ Cannot connect to cluster" -ForegroundColor Red
    exit 1
}

# =============================================================================
# ADD HELM REPOSITORIES
# =============================================================================
Write-Host ""
Write-Host "[2/10] 📦 Adding Helm Repositories" -ForegroundColor Cyan

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts 2>$null
helm repo add grafana https://grafana.github.io/helm-charts 2>$null
helm repo update

Write-Host "  ✅ Helm repositories configured" -ForegroundColor Green

# =============================================================================
# CREATE MONITORING NAMESPACE
# =============================================================================
Write-Host ""
Write-Host "[3/10] 🏗️  Creating Monitoring Namespace" -ForegroundColor Cyan

kubectl create namespace $MONITORING_NAMESPACE --dry-run=client -o yaml | kubectl apply -f -
kubectl label namespace $MONITORING_NAMESPACE istio-injection=enabled --overwrite 2>$null

Write-Host "  ✅ Namespace $MONITORING_NAMESPACE created" -ForegroundColor Green

# =============================================================================
# DEPLOY TEMPO (Distributed Tracing)
# =============================================================================
Write-Host ""
Write-Host "[4/10] 🔍 Deploying Tempo (Distributed Tracing)" -ForegroundColor Cyan

helm upgrade --install tempo grafana/tempo `
    --namespace $MONITORING_NAMESPACE `
    --values monitoring/tempo-values.yaml `
    --wait --timeout 5m0s

Write-Host "  ✅ Tempo deployed" -ForegroundColor Green

# =============================================================================
# DEPLOY LOKI (Log Aggregation)
# =============================================================================
Write-Host ""
Write-Host "[5/10] 📝 Deploying Loki (Log Aggregation)" -ForegroundColor Cyan

helm upgrade --install loki grafana/loki-stack `
    --namespace $MONITORING_NAMESPACE `
    --values monitoring/loki-values.yaml `
    --wait --timeout 5m0s

Write-Host "  ✅ Loki deployed" -ForegroundColor Green

# =============================================================================
# DEPLOY KUBE-PROMETHEUS-STACK (Prometheus + Grafana)
# =============================================================================
Write-Host ""
Write-Host "[6/10] 📊 Deploying Prometheus + Grafana Stack" -ForegroundColor Cyan

helm upgrade --install kube-prometheus-stack prometheus-community/kube-prometheus-stack `
    --namespace $MONITORING_NAMESPACE `
    --values monitoring/kube-prometheus-stack-values.yaml `
    --set grafana.adminPassword=admin123 `
    --wait --timeout 10m0s

Write-Host "  ✅ Prometheus + Grafana deployed" -ForegroundColor Green

# =============================================================================
# DEPLOY SYNTHETIC MONITORING
# =============================================================================
Write-Host ""
Write-Host "[7/10] 🌐 Deploying Synthetic Monitoring" -ForegroundColor Cyan

kubectl apply -f monitoring/synthetic-monitoring.yaml -n $MONITORING_NAMESPACE

Write-Host "  ✅ Synthetic monitoring deployed" -ForegroundColor Green

# =============================================================================
# IMPORT GRAFANA DASHBOARDS
# =============================================================================
Write-Host ""
Write-Host "[8/10] 📈 Importing Grafana Dashboards" -ForegroundColor Cyan

# Create ConfigMap for dashboard
kubectl create configmap github-gists-api-dashboard `
    --from-file=github-gists-api.json=monitoring/grafana-complete-dashboard.json `
    --namespace $MONITORING_NAMESPACE `
    --dry-run=client -o yaml | kubectl apply -f -

# Label it for Grafana sidecar
kubectl label configmap github-gists-api-dashboard grafana_dashboard=1 -n $MONITORING_NAMESPACE --overwrite

Write-Host "  ✅ Dashboards imported" -ForegroundColor Green

# =============================================================================
# CONFIGURE ISTIO GATEWAY FOR GRAFANA
# =============================================================================
Write-Host ""
Write-Host "[9/10] 🔐 Configuring Grafana Ingress" -ForegroundColor Cyan

$gatewayYaml = @"
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: grafana-gateway
  namespace: $MONITORING_NAMESPACE
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "$GRAFANA_HOST"
  - port:
      number: 443
      name: https
      protocol: HTTPS
    tls:
      mode: SIMPLE
      credentialName: grafana-tls-secret
    hosts:
    - "$GRAFANA_HOST"
---
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: grafana-vs
  namespace: $MONITORING_NAMESPACE
spec:
  hosts:
  - "$GRAFANA_HOST"
  gateways:
  - grafana-gateway
  http:
  - match:
    - uri:
        prefix: /
    route:
    - destination:
        host: kube-prometheus-stack-grafana.$MONITORING_NAMESPACE.svc.cluster.local
        port:
          number: 80
"@

$gatewayYaml | kubectl apply -f -

Write-Host "  ✅ Grafana Istio Gateway configured" -ForegroundColor Green

# =============================================================================
# CREATE TLS CERTIFICATE FOR GRAFANA
# =============================================================================
Write-Host ""
Write-Host "[9b/10] 🔒 Creating TLS Certificate for Grafana" -ForegroundColor Cyan

# Create temp directory
$certDir = "$env:TEMP\grafana-certs"
New-Item -ItemType Directory -Force -Path $certDir | Out-Null

# Generate certificate
openssl req -x509 -sha256 -nodes -days 365 -newkey rsa:2048 `
    -subj "/O=Kishore/CN=$GRAFANA_HOST" `
    -keyout "$certDir\grafana.key" `
    -out "$certDir\grafana.crt" 2>$null

# Create Kubernetes secret
kubectl create secret tls grafana-tls-secret `
    --key="$certDir\grafana.key" `
    --cert="$certDir\grafana.crt" `
    -n istio-system `
    --dry-run=client -o yaml | kubectl apply -f -

# Clean up
Remove-Item -Recurse -Force $certDir

Write-Host "  ✅ TLS certificate created" -ForegroundColor Green

# =============================================================================
# GET INGRESS IP
# =============================================================================
Write-Host ""
Write-Host "[10/10] 📡 DNS Configuration" -ForegroundColor Cyan

$INGRESS_IP = kubectl get svc istio-ingressgateway -n istio-system -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>$null
if ([string]::IsNullOrEmpty($INGRESS_IP)) {
    $INGRESS_IP = "172.18.255.200"
}

Write-Host ""
Write-Host "📝 Add this to your hosts file (C:\Windows\System32\drivers\etc\hosts):" -ForegroundColor Yellow
Write-Host "   $INGRESS_IP    $GRAFANA_HOST" -ForegroundColor Green

# =============================================================================
# DEPLOYMENT SUMMARY
# =============================================================================
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Magenta
Write-Host "║  🎉 MONITORING STACK DEPLOYMENT COMPLETE!                      ║" -ForegroundColor Magenta
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Magenta
Write-Host ""

Write-Host "📊 Deployed Components:" -ForegroundColor Cyan
Write-Host "  ├── ✅ Prometheus - Metrics collection" -ForegroundColor Green
Write-Host "  ├── ✅ Grafana - Visualization" -ForegroundColor Green
Write-Host "  ├── ✅ Loki - Log aggregation" -ForegroundColor Green
Write-Host "  ├── ✅ Tempo - Distributed tracing" -ForegroundColor Green
Write-Host "  └── ✅ Blackbox Exporter - Synthetic monitoring" -ForegroundColor Green

Write-Host ""
Write-Host "🌐 Access URLs:" -ForegroundColor Cyan
Write-Host "  ├── Grafana:     https://$GRAFANA_HOST" -ForegroundColor Green
Write-Host "  ├── Prometheus:  http://localhost:9090 (port-forward)" -ForegroundColor Green
Write-Host "  └── API:         https://gists.kishore.local" -ForegroundColor Green

Write-Host ""
Write-Host "🔐 Grafana Credentials:" -ForegroundColor Cyan
Write-Host "  ├── Username: admin" -ForegroundColor Green
Write-Host "  └── Password: admin123" -ForegroundColor Green

Write-Host ""
Write-Host "📈 Available Dashboards:" -ForegroundColor Cyan
Write-Host "  ├── GitHub Gists API - Complete Observability"
Write-Host "  ├── Kubernetes / Compute Resources"
Write-Host "  └── Istio Service Mesh Dashboard"

Write-Host ""
Write-Host "🔧 Useful Commands:" -ForegroundColor Cyan
Write-Host "  # Port-forward Grafana (alternative access):" -ForegroundColor Yellow
Write-Host "  kubectl port-forward svc/kube-prometheus-stack-grafana 3000:80 -n monitoring"
Write-Host ""
Write-Host "  # Port-forward Prometheus:" -ForegroundColor Yellow
Write-Host "  kubectl port-forward svc/kube-prometheus-stack-prometheus 9090:9090 -n monitoring"
Write-Host ""
Write-Host "  # Check monitoring pods:" -ForegroundColor Yellow
Write-Host "  kubectl get pods -n monitoring"

Write-Host ""
Write-Host "🚀 Your complete observability stack is ready!" -ForegroundColor Green
