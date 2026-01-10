# 🔍 Complete Observability Stack

> **Enterprise-grade monitoring with Grafana, Prometheus, Loki, Tempo, and Synthetic Monitoring**

## 📊 Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         OBSERVABILITY STACK                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐   │
│  │   Browser   │    │   FastAPI   │    │    Istio    │    │ Kubernetes  │   │
│  │    (RUM)    │    │     App     │    │   Proxy     │    │   Nodes     │   │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘    └──────┬──────┘   │
│         │                  │                  │                  │           │
│         │ Web Vitals       │ Traces           │ Service Mesh     │ Metrics   │
│         │ User Sessions    │ Metrics          │ mTLS            │ Logs      │
│         ▼                  ▼                  ▼                  ▼           │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐   │
│  │    Faro     │    │   Tempo     │    │ Prometheus  │    │    Loki     │   │
│  │  Collector  │    │  (Traces)   │    │  (Metrics)  │    │   (Logs)    │   │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘    └──────┬──────┘   │
│         │                  │                  │                  │           │
│         └──────────────────┴──────────────────┴──────────────────┘           │
│                                      │                                        │
│                                      ▼                                        │
│                           ┌─────────────────────┐                            │
│                           │      GRAFANA        │                            │
│                           │  kishoregrafana.local│                           │
│                           │                     │                            │
│                           │  • Dashboards       │                            │
│                           │  • Alerts           │                            │
│                           │  • Explore          │                            │
│                           └─────────────────────┘                            │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Deploy the Complete Stack

```powershell
# Navigate to project root
cd d:\Kishore\eq-assessment

# Run the deployment script
.\monitoring\deploy-monitoring.ps1
```

### Manual Deployment

```bash
# 1. Add Helm repos
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

# 2. Create namespace
kubectl create namespace monitoring

# 3. Deploy Tempo (Tracing)
helm install tempo grafana/tempo -n monitoring -f monitoring/tempo-values.yaml

# 4. Deploy Loki (Logs)
helm install loki grafana/loki-stack -n monitoring -f monitoring/loki-values.yaml

# 5. Deploy Prometheus + Grafana
helm install kube-prometheus-stack prometheus-community/kube-prometheus-stack \
  -n monitoring -f monitoring/kube-prometheus-stack-values.yaml

# 6. Deploy Synthetic Monitoring
kubectl apply -f monitoring/synthetic-monitoring.yaml -n monitoring

# 7. Deploy Faro RUM Collector (optional)
kubectl apply -f monitoring/faro-rum-collector.yaml -n monitoring
```

## 🌐 Access URLs

| Service | URL | Credentials |
|---------|-----|-------------|
| Grafana | https://kishoregrafana.local | admin / admin123 |
| Prometheus | http://localhost:9090 (port-forward) | - |
| Loki | http://localhost:3100 (port-forward) | - |
| Tempo | http://localhost:3200 (port-forward) | - |

### DNS Configuration

Add to `C:\Windows\System32\drivers\etc\hosts`:
```
172.18.255.200    kishoregrafana.local
```

## 📈 Components

### 1. **Prometheus** - Metrics Collection
- Time-series metrics database
- Service discovery for Kubernetes
- Alert rules and recording rules
- 15-day retention

**Key Metrics:**
- `http_requests_total` - Total HTTP requests
- `http_request_duration_seconds` - Request latency histogram
- `cache_hits_total` / `cache_misses_total` - Cache performance
- `github_api_requests_total` - GitHub API call tracking

### 2. **Grafana** - Visualization
- Pre-built dashboards for GitHub Gists API
- Explore view for ad-hoc queries
- Unified alerting
- Trace-to-logs correlation

**Dashboards Included:**
- GitHub Gists API - Complete Observability
- Kubernetes Cluster Overview
- Node Exporter Dashboard
- Istio Service Mesh Dashboard

### 3. **Loki** - Log Aggregation
- Prometheus-style labels for logs
- LogQL query language
- Log correlation with traces
- 30-day retention

**Log Labels:**
- `namespace` - Kubernetes namespace
- `app` - Application name
- `pod` - Pod name
- `container` - Container name

### 4. **Tempo** - Distributed Tracing
- OpenTelemetry native support
- Jaeger/Zipkin compatible
- Service graphs
- Span metrics

**Trace Protocols:**
- OTLP gRPC (port 4317)
- OTLP HTTP (port 4318)
- Jaeger (port 14268)
- Zipkin (port 9411)

### 5. **Blackbox Exporter** - Synthetic Monitoring
- HTTP endpoint probing
- SSL certificate monitoring
- Response time tracking
- Alert on endpoint failures

**Probes Configured:**
- Health endpoint (`/health`)
- Metrics endpoint (`/metrics`)
- API endpoints

### 6. **Faro** - Real User Monitoring (RUM)
- Web Vitals (LCP, FID, CLS, TTFB)
- JavaScript error tracking
- User session tracking
- Frontend-to-backend trace correlation

## 🔧 Configuration Files

| File | Purpose |
|------|---------|
| `kube-prometheus-stack-values.yaml` | Grafana + Prometheus configuration |
| `loki-values.yaml` | Log aggregation settings |
| `tempo-values.yaml` | Distributed tracing settings |
| `synthetic-monitoring.yaml` | Blackbox exporter + probes |
| `faro-rum-collector.yaml` | Real User Monitoring |
| `grafana-complete-dashboard.json` | Main API dashboard |
| `deploy-monitoring.ps1` | PowerShell deployment script |
| `deploy-monitoring.sh` | Bash deployment script |

## 📊 Dashboard Panels

### Service Overview
- Running Pods count
- P95 Latency
- Error Rate
- Request Rate
- Cache Hit Rate
- Synthetic Probe Status

### Request Metrics
- Request rate by endpoint
- Response time percentiles (p50, p95, p99)
- Error rate trending

### Cache Performance
- Hit/Miss ratio pie chart
- Cache operations over time
- GitHub API calls by status

### Synthetic Monitoring
- Endpoint health status
- Probe response times
- SSL certificate expiry warnings

### Logs Panel
- Live application logs from Loki
- Filtered by namespace and app

### Traces Panel
- Recent traces from Tempo
- Service dependency graph

### Resource Usage
- CPU usage by pod
- Memory usage by pod

## 🚨 Alerting Rules

### Critical Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| EndpointDown | Probe fails for > 1 min | Critical |
| HighErrorRate | Error rate > 5% for 5 min | Critical |
| HighLatency | P95 > 2s for 5 min | Critical |

### Warning Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| SlowEndpoint | Response > 1s for 5 min | Warning |
| SSLCertExpiring | Cert expires in < 14 days | Warning |
| LowCacheHitRate | Hit rate < 50% for 15 min | Warning |

## 🔍 Useful Queries

### Prometheus (PromQL)
```promql
# Request rate by endpoint
sum(rate(http_requests_total[5m])) by (endpoint)

# P95 latency
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))

# Error rate percentage
sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) * 100

# Cache hit rate
sum(rate(cache_hits_total[5m])) / (sum(rate(cache_hits_total[5m])) + sum(rate(cache_misses_total[5m]))) * 100
```

### Loki (LogQL)
```logql
# Application logs
{namespace="production", app="github-gists-api"}

# Error logs only
{namespace="production", app="github-gists-api"} |= "error"

# JSON log parsing
{namespace="production"} | json | level="error"

# Rate of errors
sum(rate({namespace="production"} |= "error" [5m]))
```

### Tempo (TraceQL)
```traceql
# Find traces for a service
{ resource.service.name = "github-gists-api" }

# Find slow traces
{ resource.service.name = "github-gists-api" && duration > 500ms }

# Find error traces
{ resource.service.name = "github-gists-api" && status = error }
```

## 🔧 Port-Forward Commands

```powershell
# Grafana (if DNS not configured)
kubectl port-forward svc/kube-prometheus-stack-grafana 3000:80 -n monitoring

# Prometheus
kubectl port-forward svc/kube-prometheus-stack-prometheus 9090:9090 -n monitoring

# Loki
kubectl port-forward svc/loki 3100:3100 -n monitoring

# Tempo
kubectl port-forward svc/tempo 3200:3200 -n monitoring

# Alertmanager
kubectl port-forward svc/kube-prometheus-stack-alertmanager 9093:9093 -n monitoring
```

## ✅ Health Check Commands

```powershell
# Check all monitoring pods
kubectl get pods -n monitoring

# Check Prometheus targets
kubectl port-forward svc/kube-prometheus-stack-prometheus 9090:9090 -n monitoring
# Then visit: http://localhost:9090/targets

# Check Loki ready
kubectl exec -it deployment/loki -n monitoring -- wget -qO- http://localhost:3100/ready

# Check Tempo ready
kubectl exec -it deployment/tempo -n monitoring -- wget -qO- http://localhost:3200/ready
```

## 📚 References

- [Grafana Documentation](https://grafana.com/docs/grafana/latest/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Loki Documentation](https://grafana.com/docs/loki/latest/)
- [Tempo Documentation](https://grafana.com/docs/tempo/latest/)
- [OpenTelemetry Python](https://opentelemetry.io/docs/instrumentation/python/)
- [Grafana Faro](https://grafana.com/docs/grafana-cloud/monitor-applications/frontend-observability/)

---

<div align="center">

**🚀 Complete Observability for GitHub Gists API**

*Metrics • Logs • Traces • RUM • Synthetic Monitoring*

</div>
