# 📊 Complete Monitoring Setup Guide

## 🎯 Overview

This guide shows how to set up **complete real-time monitoring** for the GitHub Gists API using **GitHub free runners** and industry-standard tools.

---

## ✅ What You Get

| Feature | Tool | Status |
|---------|------|--------|
| **CI/CD Pipeline** | GitHub Actions | ✅ Included |
| **Synthetic Monitoring** | GitHub Actions (every 5 min) | ✅ Included |
| **Load Testing** | k6 | ✅ Included |
| **Metrics Collection** | Prometheus | ✅ Configured |
| **Dashboards** | Grafana | ✅ Included |
| **Alerts** | Grafana Alerts | ✅ Configured |
| **API Gateway** | Gateway API (K8s) | ✅ Included |
| **Service Mesh** | Istio (optional) | ✅ Included |
| **Load Balancer** | K8s Service + Gateway | ✅ Included |
| **SSL/TLS** | cert-manager + Let's Encrypt | ✅ Configured |

---

## 🚀 Quick Start (5 Minutes)

### 1. **Enable GitHub Actions Workflows**

All workflows are in `.github/workflows/`:
- `ci.yml` - Tests, security scans, build
- `cd.yml` - Kubernetes deployment
- `monitoring.yml` - **NEW** Synthetic monitoring every 5 min
- `grafana-cloud-sync.yml` - **NEW** Push metrics to Grafana

### 2. **Set GitHub Secrets**

Go to your repo → Settings → Secrets → Actions:

```bash
# Kubernetes (for CD)
KUBECONFIG=<base64 encoded kubeconfig>

# Grafana Cloud (free tier available)
GRAFANA_CLOUD_API_KEY=<your-api-key>
GRAFANA_CLOUD_URL=https://prometheus-prod-XX-XX.grafana.net

# Slack (optional)
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# PagerDuty (optional, for critical alerts)
PAGERDUTY_INTEGRATION_KEY=<your-key>
```

### 3. **Enable Workflows**

```bash
# In your repo root
git add .github/workflows/*.yml
git commit -m "feat: Add comprehensive monitoring"
git push origin main
```

**That's it!** Monitoring runs automatically every 5 minutes on GitHub free runners.

---

## 📈 Monitoring Features

### 1. **Synthetic Monitoring** (`.github/workflows/monitoring.yml`)

Runs **every 5 minutes** on GitHub runners:

- ✅ Health endpoint check
- ✅ User API test (with octocat)
- ✅ Error handling validation
- ✅ Latency measurement (10 requests, avg/p95)
- ✅ SSL certificate expiry check
- ✅ Slack alerts on failure

**View Results**: 
- GitHub Actions → Monitoring workflow → Latest run
- Each run shows metrics in job summary

### 2. **Load Testing** (k6)

Automatically runs in CI/CD:

```javascript
// Simulates realistic traffic
- Ramp up to 10 concurrent users (30s)
- Sustain 10 users for 1 minute
- Ramp down (30s)

// Thresholds
- p95 latency < 2s
- Error rate < 10%
```

**View Results**: GitHub Actions → Artifacts → `k6-results`

### 3. **Grafana Dashboards**

Import `monitoring/grafana-dashboard.json`:

**Panels**:
- Request rate (by endpoint, method)
- Response time (p50, p95, p99)
- Error rate (4xx, 5xx)
- Active pods
- CPU/Memory usage
- GitHub API rate limits

**Grafana Cloud Free Tier**:
- 10K series
- 14-day retention
- 3 users
- ✅ Perfect for this project!

Sign up: https://grafana.com/auth/sign-up/create-user

### 4. **Prometheus Alerts**

Import `monitoring/grafana-alerts.yaml`:

**Alerts**:
- 🚨 **Critical**: API down > 2 min → PagerDuty
- ⚠️ **Warning**: Error rate > 5% → Slack
- ⚠️ **Warning**: p95 latency > 2s → Slack
- ⚠️ **Warning**: Low pod count → Slack
- ⚠️ **Warning**: SSL expires < 30 days → Email
- ⚠️ **Warning**: GitHub rate limit hit → Slack
- ℹ️ **Info**: CPU throttling → Slack

---

## 🏗️ Infrastructure Setup

### **Load Balancer** (Kubernetes Service)

Already in `k8s/deployment.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: github-gists-api
spec:
  type: LoadBalancer  # ← Cloud provider LB (AWS ELB, GCP LB, etc.)
  selector:
    app: github-gists-api
  ports:
    - port: 80
      targetPort: 8080
```

### **API Gateway** (Gateway API)

Already in `k8s/gateway-api.yaml`:

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: github-gists-gateway
spec:
  gatewayClassName: nginx  # or istio, envoy
  listeners:
    - name: https
      port: 443
      protocol: HTTPS
      tls:
        certificateRefs:
          - name: gists-api-tls  # ← Auto-issued by cert-manager
```

**Features**:
- ✅ TLS termination
- ✅ HTTP → HTTPS redirect
- ✅ Request timeout (30s)
- ✅ Header manipulation
- ✅ Path-based routing

### **Istio Service Mesh** (Optional)

Already in `k8s/ingress-istio.yaml`:

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: github-gists-api
spec:
  http:
    - timeout: 30s
      retries:
        attempts: 3
        perTryTimeout: 10s
      fault:
        delay:  # Chaos engineering
          percentage:
            value: 0.1
          fixedDelay: 5s
```

**Extra Features**:
- 🔄 Automatic retries
- ⚡ Circuit breaking
- 📊 Distributed tracing (Jaeger)
- 🔐 mTLS between services
- 🎭 Canary deployments
- 💥 Fault injection (testing)

**Enable Istio**:
```bash
# Install Istio
curl -L https://istio.io/downloadIstio | sh -
istioctl install --set profile=demo -y

# Label namespace for auto-injection
kubectl label namespace production istio-injection=enabled

# Apply Istio config
kubectl apply -f k8s/ingress-istio.yaml
```

---

## 📊 Real-Time Monitoring URLs

Once deployed:

### **Application**
```
https://gists-api.example.com/health
https://gists-api.example.com/octocat
```

### **Grafana Dashboard**
```
https://your-org.grafana.net/d/gist-api
```

### **Prometheus**
```
https://prometheus.example.com/graph
```

### **Istio Kiali** (if using Istio)
```
http://kiali.istio-system.svc.cluster.local:20001
```

### **Istio Jaeger** (distributed tracing)
```
http://jaeger.istio-system.svc.cluster.local:16686
```

---

## 🔧 GitHub Actions Monitoring Output

Example from `.github/workflows/monitoring.yml`:

```
✅ Health check passed: HTTP 200
📊 Response time: 245ms
📡 Status code: 200
✅ Response structure valid
✅ 404 handling works correctly

Running latency tests...
Request 1: 234ms
Request 2: 198ms
Request 3: 256ms
...
📊 Average latency: 227ms
```

### **Slack Alerts** (on failure):

```
🚨 *Gist API Monitoring Alert*
• Health: 500
• Status: 500
• Latency: 5432ms
• Time: 2026-01-10 18:30:42 UTC
```

---

## 🎯 Cost Breakdown (All FREE!)

| Service | Plan | Cost |
|---------|------|------|
| **GitHub Actions** | Free tier: 2000 min/month | $0 |
| **Grafana Cloud** | Free tier: 10K series | $0 |
| **Prometheus** | Self-hosted in K8s | $0 |
| **Let's Encrypt** | Free SSL certificates | $0 |
| **Kubernetes** | Use your existing cluster | $0* |

*Note: You need a K8s cluster (EKS, GKE, AKS, minikube, kind)

---

## 🚀 Advanced Features

### **1. Custom Metrics Endpoint**

Add to `app/main.py`:

```python
from prometheus_client import Counter, Histogram, generate_latest

# Metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'Request latency')

@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest(), media_type="text/plain")
```

### **2. Distributed Tracing**

Add to `requirements.txt`:
```
opentelemetry-api==1.21.0
opentelemetry-instrumentation-fastapi==0.42b0
```

Enable in `app/main.py`:
```python
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

FastAPIInstrumentor.instrument_app(app)
```

### **3. Real User Monitoring (RUM)**

Add Grafana Faro to a frontend:
```html
<script src="https://unpkg.com/@grafana/faro-web-sdk@^1.0.0"></script>
<script>
  window.faro = FaroSDK.initializeFaro({
    url: 'https://faro-collector.grafana.net',
    apiKey: 'your-key',
    app: { name: 'gist-api-frontend' }
  });
</script>
```

---

## 📋 Checklist: Full Production Setup

- [x] CI/CD pipeline (GitHub Actions)
- [x] Synthetic monitoring (every 5 min)
- [x] Load testing (k6)
- [x] Kubernetes deployment
- [x] Load balancer (K8s Service)
- [x] API Gateway (Gateway API)
- [x] Istio service mesh (optional)
- [x] Prometheus metrics
- [x] Grafana dashboards
- [x] Alerting (Slack, PagerDuty)
- [x] SSL/TLS (cert-manager)
- [x] Security scanning (Trivy, Bandit)
- [x] SBOM generation
- [ ] Custom /metrics endpoint
- [ ] Distributed tracing
- [ ] Real User Monitoring

---

## 🎓 Interview Talking Points

### **Question**: "How do you monitor your application?"

**Your Answer**:
> "I implemented comprehensive monitoring using:
> 1. **Synthetic monitoring** via GitHub Actions every 5 minutes - tests health, latency, and error handling
> 2. **Prometheus** for metrics collection from Kubernetes pods
> 3. **Grafana dashboards** showing request rate, p95 latency, error rates, and resource usage
> 4. **Grafana Alerts** for critical issues (API down, high error rate, SSL expiry) with Slack/PagerDuty integration
> 5. **Load testing** with k6 in CI/CD to catch performance regressions
> 6. **Istio service mesh** for advanced observability with distributed tracing and automatic retries
> 
> All of this runs on GitHub's free runners, making it cost-effective while maintaining production-grade monitoring."

### **Question**: "How do you handle load balancing?"

**Your Answer**:
> "Three layers:
> 1. **Kubernetes Service** (LoadBalancer type) - distributes traffic across pods
> 2. **Gateway API** (modern replacement for Ingress) - handles TLS termination, routing, and timeout policies
> 3. **Istio** (optional) - advanced traffic management with retries, circuit breaking, and canary deployments
> 
> Plus horizontal pod autoscaling (HPA) based on CPU/memory to automatically scale from 3-10 replicas under load."

---

## 🔗 Useful Links

- **Grafana Cloud**: https://grafana.com/products/cloud/
- **Prometheus**: https://prometheus.io/docs/
- **k6 Load Testing**: https://k6.io/docs/
- **Gateway API**: https://gateway-api.sigs.k8s.io/
- **Istio**: https://istio.io/latest/docs/
- **cert-manager**: https://cert-manager.io/docs/

---

## ✅ Summary

You now have:
- ✅ **Full CI/CD** with security scanning
- ✅ **Synthetic monitoring** every 5 minutes (GitHub free runners)
- ✅ **Load testing** in CI/CD
- ✅ **Grafana dashboards** for visualization
- ✅ **Prometheus alerts** for critical issues
- ✅ **API Gateway** for modern traffic management
- ✅ **Istio** for service mesh (optional)
- ✅ **Load balancing** at multiple layers
- ✅ **SSL/TLS** with auto-renewal
- ✅ **Cost: $0** using free tiers!

**Everything runs on GitHub's free runner tier (2000 min/month)** - perfect for personal projects and demonstrating production skills! 🚀
