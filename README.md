<![CDATA[<div align="center">

# 🚀 Production-Grade GitHub Gists API

### Enterprise Kubernetes Deployment with CI/CD, Service Mesh & Security Best Practices

[![CI Pipeline](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF?logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![CD Pipeline](https://img.shields.io/badge/CD-Kind%20Cluster-326CE5?logo=kubernetes&logoColor=white)](https://kind.sigs.k8s.io/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Production--Ready-326CE5?logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![Istio](https://img.shields.io/badge/Istio-Service%20Mesh-466BB0?logo=istio&logoColor=white)](https://istio.io/)
[![Security](https://img.shields.io/badge/Security-Trivy%20%7C%20Snyk%20%7C%20Bandit-FF6B6B)](https://trivy.dev/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

<p align="center">
  <img src="https://img.shields.io/badge/Load%20Balancing-MetalLB-orange?style=for-the-badge" alt="MetalLB"/>
  <img src="https://img.shields.io/badge/TLS-Self--Signed-blue?style=for-the-badge" alt="TLS"/>
  <img src="https://img.shields.io/badge/mTLS-Enabled-green?style=for-the-badge" alt="mTLS"/>
  <img src="https://img.shields.io/badge/Observability-Prometheus-red?style=for-the-badge" alt="Prometheus"/>
</p>

---

**A showcase of modern DevOps practices: From code to production-ready Kubernetes deployment**

[Features](#-features) • [Architecture](#-architecture) • [Quick Start](#-quick-start) • [CI/CD Pipeline](#-cicd-pipeline) • [Best Practices](#-best-practices-implemented) • [API Reference](#-api-reference)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [CI/CD Pipeline](#-cicd-pipeline)
- [Kubernetes Deployment](#-kubernetes-deployment)
- [Security Implementation](#-security-implementation)
- [Monitoring & Observability](#-monitoring--observability)
- [API Reference](#-api-reference)
- [Best Practices Implemented](#-best-practices-implemented)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

---

## 🎯 Overview

This project demonstrates a **production-grade implementation** of a GitHub Gists API service, showcasing modern DevOps and Platform Engineering practices. It serves as a comprehensive reference architecture for:

- **Cloud-Native Development** with Python FastAPI
- **Container Security** with multi-stage Docker builds
- **Kubernetes Operations** with Helm charts and raw manifests
- **Service Mesh Integration** with Istio for advanced traffic management
- **CI/CD Automation** with GitHub Actions
- **Security-First Approach** with multiple vulnerability scanning tools

### 🏆 Key Achievements

| Metric | Result |
|--------|--------|
| **Load Test Success Rate** | 100% (100/100 requests) |
| **Average Response Time** | 21ms |
| **Security Vulnerabilities** | 0 Critical, 0 High (application) |
| **Container Image Size** | ~150MB (optimized) |
| **Deployment Time** | < 3 minutes |

---

## ✨ Features

### Application Features
- 🔍 **GitHub Gists Lookup** - Fetch public gists for any GitHub user
- � **Pagination Support** - Control results with `page` and `per_page` parameters
- ⚡ **In-Memory Caching** - 5-minute TTL cache to reduce API calls and improve latency
- 📊 **Prometheus Metrics** - Built-in observability with custom metrics
- 💪 **Health Endpoints** - Kubernetes-ready health and readiness probes
- 🚀 **High Performance** - Async HTTP client with connection pooling
- 🔐 **Token Support** - Optional GitHub token for 5000 req/hour (vs 60)

### Infrastructure Features
- 🐳 **Multi-stage Docker Build** - Secure, optimized container images
- ☸️ **Kubernetes Native** - Deployment, Service, HPA, PDB
- 🌐 **Istio Service Mesh** - Traffic management, mTLS, observability
- ⚖️ **Load Balancing** - MetalLB for LoadBalancer IP assignment
- 🔒 **TLS Termination** - HTTPS with self-signed certificates
- 📈 **Auto-scaling** - HPA with CPU/memory based scaling

### CI/CD Features
- ✅ **Automated Testing** - pytest with coverage reporting
- 🔍 **Code Quality** - flake8, mypy, SonarCloud
- 🛡️ **Security Scanning** - Trivy, Snyk, Bandit, TruffleHog
- 📦 **Container Scanning** - Multi-tool vulnerability detection
- 🚀 **GitOps Ready** - Automated deployment to Kind cluster

---

## 🏗 Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              GITHUB ACTIONS                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                   │
│  │   CI Pipeline │    │  CD Pipeline │    │ Security Scan│                   │
│  │  ├─ Lint     │    │  ├─ Build    │    │  ├─ Trivy    │                   │
│  │  ├─ Test     │    │  ├─ Deploy   │    │  ├─ Snyk     │                   │
│  │  ├─ Coverage │    │  └─ Verify   │    │  └─ Bandit   │                   │
│  │  └─ Sonar    │    │              │    │              │                   │
│  └──────────────┘    └──────────────┘    └──────────────┘                   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         KIND KUBERNETES CLUSTER                              │
│                                                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                        ISTIO SERVICE MESH                            │   │
│   │                                                                      │   │
│   │   ┌──────────────┐         ┌──────────────────────────────────┐    │   │
│   │   │    Gateway   │────────▶│         VirtualService           │    │   │
│   │   │   (TLS/443)  │         │   - Retry Logic (3 attempts)     │    │   │
│   │   └──────────────┘         │   - Timeout (30s)                │    │   │
│   │                            │   - Traffic Routing              │    │   │
│   │                            └──────────────────────────────────┘    │   │
│   │                                         │                          │   │
│   │                                         ▼                          │   │
│   │   ┌──────────────────────────────────────────────────────────┐    │   │
│   │   │              PRODUCTION NAMESPACE (mTLS STRICT)           │    │   │
│   │   │                                                           │    │   │
│   │   │   ┌─────────┐    ┌─────────┐    ┌─────────┐             │    │   │
│   │   │   │  Pod 1  │    │  Pod 2  │    │  Pod 3  │             │    │   │
│   │   │   │ :8080   │    │ :8080   │    │ :8080   │             │    │   │
│   │   │   └─────────┘    └─────────┘    └─────────┘             │    │   │
│   │   │        │              │              │                    │    │   │
│   │   │        └──────────────┼──────────────┘                    │    │   │
│   │   │                       ▼                                   │    │   │
│   │   │              ┌───────────────┐                           │    │   │
│   │   │              │   Service     │                           │    │   │
│   │   │              │  (ClusterIP)  │                           │    │   │
│   │   │              └───────────────┘                           │    │   │
│   │   │                                                           │    │   │
│   │   └──────────────────────────────────────────────────────────┘    │   │
│   │                                                                    │   │
│   └────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│   ┌────────────────────┐    ┌────────────────────┐                         │
│   │      MetalLB       │    │   Istio Ingress    │                         │
│   │ (172.18.255.x IP)  │────│   Gateway LB       │                         │
│   └────────────────────┘    └────────────────────┘                         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                    ┌──────────────────────────────┐
                    │         CLIENT ACCESS        │
                    │   https://gists.kishore.local │
                    │   https://gists.local         │
                    └──────────────────────────────┘
```

### Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Application** | Python 3.12 + FastAPI | High-performance async API |
| **Container** | Docker (multi-stage) | Secure, minimal images |
| **Orchestration** | Kubernetes (Kind) | Container orchestration |
| **Service Mesh** | Istio 1.23.4 | Traffic management, security |
| **Load Balancer** | MetalLB 0.14.9 | External IP assignment |
| **TLS** | OpenSSL | Certificate generation |
| **CI/CD** | GitHub Actions | Automated pipelines |
| **Monitoring** | Prometheus + Grafana | Observability |
| **Security** | Trivy, Snyk, Bandit | Vulnerability scanning |

---

## 📦 Prerequisites

### Required Software

| Software | Version | Installation |
|----------|---------|--------------|
| **Docker Desktop** | 4.x+ | [Download](https://www.docker.com/products/docker-desktop/) |
| **Kind** | 0.20+ | `choco install kind` or [GitHub](https://kind.sigs.k8s.io/) |
| **kubectl** | 1.28+ | `choco install kubernetes-cli` |
| **Helm** | 3.x+ | `choco install kubernetes-helm` |
| **Git** | 2.x+ | [Download](https://git-scm.com/) |
| **Python** | 3.12+ | [Download](https://www.python.org/) |

### For CI/CD Pipeline

| Requirement | Purpose |
|-------------|---------|
| **GitHub Repository** | Code hosting & Actions |
| **Self-Hosted Runner** | Windows runner with `[self-hosted, Windows, X64]` labels |
| **Kind Cluster** | Pre-created cluster named `kind-dev` |
| **Istio** | Service mesh (demo profile) |

### Optional Enhancements

| Software | Purpose |
|----------|---------|
| **SonarCloud Account** | Code quality analysis |
| **Snyk Account** | Dependency vulnerability scanning |
| **GitHub Token** | Increase API rate limit to 5000/hour |

---

## 🚀 Quick Start

### Option 1: Local Docker (Fastest)

```bash
# Clone the repository
git clone https://github.com/your-username/eq-assessment.git
cd eq-assessment

# Build and run
docker build -t github-gists-api .
docker run -p 8080:8080 github-gists-api

# Test
curl http://localhost:8080/health
curl http://localhost:8080/octocat
```

### Option 2: Full Kubernetes Deployment

#### Step 1: Create Kind Cluster with Istio

```powershell
# Create Kind cluster with extra ports
kind create cluster --name kind-dev --config - <<EOF
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  extraPortMappings:
  - containerPort: 30080
    hostPort: 80
  - containerPort: 30443
    hostPort: 443
EOF

# Install Istio
istioctl install --set profile=demo -y

# Verify
kubectl get pods -n istio-system
```

#### Step 2: Deploy Application

```powershell
# Build and load image
docker build -t github-gists-api:latest .
kind load docker-image github-gists-api:latest --name kind-dev

# Create namespace with Istio injection
kubectl create namespace production
kubectl label namespace production istio-injection=enabled

# Deploy
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/istio-gateway.yaml

# Wait for deployment
kubectl rollout status deployment/github-gists-api -n production
```

#### Step 3: Setup MetalLB (LoadBalancer)

```powershell
# Install MetalLB
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.14.9/config/manifests/metallb-native.yaml

# Wait for MetalLB pods
kubectl wait --namespace metallb-system --for=condition=ready pod --selector=app=metallb --timeout=120s

# Configure IP pool (adjust for your Docker network)
kubectl apply -f - <<EOF
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: kind-pool
  namespace: metallb-system
spec:
  addresses:
  - 172.18.255.200-172.18.255.250
---
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: kind-l2
  namespace: metallb-system
spec:
  ipAddressPools:
  - kind-pool
EOF
```

#### Step 4: Access the Application

```powershell
# Add to Windows hosts file (C:\Windows\System32\drivers\etc\hosts)
# 127.0.0.1 gists.kishore.local gists.local

# Port forward for HTTPS access
kubectl port-forward -n istio-system svc/istio-ingressgateway 443:443

# Test (new terminal)
curl -k https://gists.kishore.local/health
curl -k https://gists.kishore.local/octocat
```

---

## 🔄 CI/CD Pipeline

### Pipeline Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                         CI PIPELINE (ci.yml)                            │
│                         Runs on: ubuntu-latest                          │
├────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    │
│  │  LINT & TEST    │    │ SECURITY SCAN   │    │  BUILD & SCAN   │    │
│  │                 │    │                 │    │                 │    │
│  │  ├─ flake8      │    │  ├─ Bandit      │    │  ├─ Docker Build│    │
│  │  ├─ mypy        │    │  ├─ TruffleHog  │    │  ├─ Trivy Scan  │    │
│  │  ├─ pytest      │    │  └─ Snyk        │    │  ├─ Snyk Scan   │    │
│  │  ├─ coverage    │    │                 │    │  └─ Push Image  │    │
│  │  └─ SonarCloud  │    │                 │    │                 │    │
│  └────────┬────────┘    └────────┬────────┘    └────────┬────────┘    │
│           │                      │                      │              │
│           └──────────────────────┼──────────────────────┘              │
│                                  ▼                                      │
│                        ┌─────────────────┐                             │
│                        │   QUALITY GATE  │                             │
│                        │   All checks    │                             │
│                        │   must pass     │                             │
│                        └─────────────────┘                             │
│                                                                         │
└────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      CD PIPELINE (cd-local.yml)                         │
│                  Runs on: [self-hosted, Windows, X64]                   │
├────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐              │
│  │  BUILD IMAGE  │─▶│ LOAD TO KIND  │─▶│    DEPLOY     │              │
│  │               │  │               │  │               │              │
│  │  docker build │  │  kind load    │  │  kubectl      │              │
│  │               │  │  docker-image │  │  apply        │              │
│  └───────────────┘  └───────────────┘  └───────────────┘              │
│                                                │                        │
│                                                ▼                        │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐              │
│  │ SETUP METALLB │─▶│  GENERATE TLS │─▶│CONFIGURE ISTIO│              │
│  │               │  │               │  │               │              │
│  │  IP Pool      │  │  OpenSSL cert │  │  Gateway +    │              │
│  │  L2 Advertise │  │  TLS Secret   │  │  VirtualSvc   │              │
│  └───────────────┘  └───────────────┘  └───────────────┘              │
│                                                │                        │
│                                                ▼                        │
│                          ┌───────────────────────────┐                 │
│                          │   DEPLOYMENT COMPLETE     │                 │
│                          │   https://gists.local     │                 │
│                          └───────────────────────────┘                 │
│                                                                         │
└────────────────────────────────────────────────────────────────────────┘
```

### CI Pipeline Jobs

| Job | Description | Tools |
|-----|-------------|-------|
| **lint-and-test** | Code quality & testing | flake8, mypy, pytest, SonarCloud |
| **security-scan** | Security analysis | Bandit, TruffleHog |
| **build-and-scan** | Container build & scan | Docker, Trivy, Snyk |

### CD Pipeline Steps

| Step | Description |
|------|-------------|
| **Build Image** | Multi-stage Docker build |
| **Load to Kind** | Load image into Kind cluster |
| **Deploy** | Apply Kubernetes manifests |
| **Setup GitHub Token** | Configure API rate limit secret |
| **Setup MetalLB** | Configure LoadBalancer IP pool |
| **Generate TLS** | Create self-signed certificate |
| **Configure Istio** | Apply Gateway & VirtualService |

### Running the Pipelines

```bash
# Trigger CI Pipeline (manual dispatch)
gh workflow run ci.yml

# Trigger CD Pipeline (manual dispatch)  
gh workflow run cd-local.yml

# Or via GitHub UI:
# Repository → Actions → Select Workflow → Run workflow
```

---

## ☸️ Kubernetes Deployment

### Kubernetes Manifests

```
k8s/
├── deployment.yaml      # Deployment, Service, HPA, PDB
├── istio-gateway.yaml   # Gateway, VirtualService, DestinationRule
├── ingress-nginx.yaml   # Alternative: NGINX Ingress
└── gateway-api.yaml     # Alternative: Gateway API
```

### Key Kubernetes Features

#### Deployment Configuration

```yaml
# Highlights from k8s/deployment.yaml
spec:
  replicas: 3                    # High availability
  strategy:
    type: RollingUpdate          # Zero-downtime deployments
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0

  template:
    spec:
      securityContext:           # Pod-level security
        runAsNonRoot: true
        runAsUser: 1000
        seccompProfile:
          type: RuntimeDefault

      containers:
      - name: api
        securityContext:         # Container-level security
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop: ["ALL"]

        resources:               # Resource limits
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "500m"
```

#### Horizontal Pod Autoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
spec:
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

#### Pod Disruption Budget

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
spec:
  minAvailable: 2    # Always keep 2 pods running
```

---

## 🔒 Security Implementation

### Security Layers

```
┌──────────────────────────────────────────────────────────────────────┐
│                     SECURITY ARCHITECTURE                             │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │                    APPLICATION SECURITY                         │  │
│  │  ├─ Input validation (Pydantic models)                         │  │
│  │  ├─ Secure HTTP headers                                        │  │
│  │  └─ GitHub token authentication (optional)                     │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │                    CONTAINER SECURITY                           │  │
│  │  ├─ Multi-stage build (minimal attack surface)                 │  │
│  │  ├─ Non-root user (UID 1000)                                   │  │
│  │  ├─ Read-only root filesystem                                  │  │
│  │  ├─ No privilege escalation                                    │  │
│  │  ├─ Dropped all Linux capabilities                             │  │
│  │  └─ Base image: python:3.12-slim-bookworm                      │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │                   KUBERNETES SECURITY                           │  │
│  │  ├─ Namespace isolation (production)                           │  │
│  │  ├─ Resource limits (prevent DoS)                              │  │
│  │  ├─ Security context (pod & container level)                   │  │
│  │  ├─ Secrets management (K8s secrets)                           │  │
│  │  └─ Network policies (Istio mTLS)                              │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │                     NETWORK SECURITY                            │  │
│  │  ├─ TLS termination at Istio Gateway                           │  │
│  │  ├─ mTLS STRICT mode (pod-to-pod encryption)                   │  │
│  │  ├─ Traffic policies (rate limiting, retries)                  │  │
│  │  └─ Custom DNS (gists.kishore.local)                           │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │                    CI/CD SECURITY                               │  │
│  │  ├─ Dependency scanning (Snyk)                                 │  │
│  │  ├─ Container scanning (Trivy)                                 │  │
│  │  ├─ Code scanning (Bandit, SonarCloud)                         │  │
│  │  ├─ Secret scanning (TruffleHog)                               │  │
│  │  └─ SBOM generation (Trivy)                                    │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

### Security Scanning Tools

| Tool | Purpose | Integration |
|------|---------|-------------|
| **Trivy** | Container vulnerability scanning | CI Pipeline |
| **Snyk** | Dependency & container scanning | CI Pipeline |
| **Bandit** | Python security linter | CI Pipeline |
| **TruffleHog** | Secret detection | CI Pipeline |
| **SonarCloud** | Code quality & security | CI Pipeline |

---

## 📊 Monitoring & Observability

### Prometheus Metrics

The application exposes metrics at `/metrics`:

| Metric | Type | Description |
|--------|------|-------------|
| `http_requests_total` | Counter | Total HTTP requests by method, endpoint, status |
| `http_request_duration_seconds` | Histogram | Request latency distribution |
| `http_requests_active` | Gauge | Currently active requests |
| `github_api_requests_total` | Counter | GitHub API calls by status |

### Grafana Dashboard

A pre-configured Grafana dashboard is available at `monitoring/grafana-dashboard.json`:

```bash
# Import to Grafana
# 1. Open Grafana UI
# 2. Go to Dashboards → Import
# 3. Upload monitoring/grafana-dashboard.json
```

### Prometheus Alerting Rules

```bash
# Deploy alerting rules
kubectl apply -f monitoring/prometheus-rules.yaml
```

### Istio Observability

With Istio service mesh, you get automatic:
- **Distributed Tracing** (Jaeger/Zipkin)
- **Service Graph** (Kiali)
- **Metrics** (Prometheus)
- **Logs** (Access logging)

```bash
# Access Kiali dashboard
istioctl dashboard kiali

# Access Grafana
istioctl dashboard grafana

# Access Jaeger (tracing)
istioctl dashboard jaeger
```

---

## 📚 API Reference

### Base URL
```
https://gists.kishore.local
```

### Endpoints

#### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "github-gists-api"
}
```

#### Get User Gists (with Pagination & Caching)
```http
GET /{username}
```

**Path Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `username` | string | GitHub username (1-39 characters) |

**Query Parameters:**
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `page` | int | 1 | Page number (1-100) |
| `per_page` | int | 30 | Items per page (1-100) |
| `use_cache` | bool | true | Use cached data if available |

**Example Requests:**
```bash
# Get first 30 gists (default)
curl https://gists.kishore.local/octocat

# Get page 2 with 10 items per page
curl https://gists.kishore.local/octocat?page=2&per_page=10

# Force fresh fetch (bypass cache)
curl https://gists.kishore.local/octocat?use_cache=false
```

**Response:**
```json
{
  "data": [
    {
      "id": "aa5a315d61ae9438b18d",
      "description": "Hello World Example",
      "url": "https://gist.github.com/aa5a315d61ae9438b18d",
      "created_at": "2010-04-14T02:15:15Z",
      "files": {
        "hello_world.rb": {
          "filename": "hello_world.rb",
          "type": "application/x-ruby",
          "language": "Ruby",
          "raw_url": "...",
          "size": 167
        }
      }
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 30,
    "count": 8,
    "has_next": false,
    "has_prev": false
  },
  "cache": {
    "hit": false,
    "ttl_seconds": 300
  }
}
```

**Error Response (404):**
```json
{
  "detail": "User 'nonexistent' not found"
}
```

#### Cache Statistics
```http
GET /cache/stats
```

**Response:**
```json
{
  "size": 5,
  "hits": 42,
  "misses": 10,
  "hit_rate": 0.807,
  "ttl_seconds": 300
}
```

#### Clear Cache
```http
DELETE /cache
```

**Response:**
```json
{
  "message": "Cache cleared successfully"
}
```

#### Prometheus Metrics
```http
GET /metrics
```

Returns Prometheus-formatted metrics including:
- `http_requests_total` - Total HTTP requests
- `http_request_duration_seconds` - Request latency histogram
- `http_requests_active` - Currently active requests
- `github_api_requests_total` - GitHub API calls
- `cache_hits_total` - Cache hits counter
- `cache_misses_total` - Cache misses counter

### Rate Limits

| Mode | Limit | How to Enable |
|------|-------|---------------|
| **Anonymous** | 60 requests/hour | Default |
| **Authenticated** | 5000 requests/hour | Set `GITHUB_TOKEN` env var |

### Caching Behavior

| Feature | Description |
|---------|-------------|
| **TTL** | 5 minutes (configurable via `CACHE_TTL` env var) |
| **Cache Key** | `gists:{username}:page{N}:per_page{N}` |
| **Bypass** | Use `?use_cache=false` query parameter |
| **Clear** | `DELETE /cache` endpoint |
| **Stats** | `GET /cache/stats` endpoint |

---

## ✅ Best Practices Implemented

### 1. Container Best Practices

- [x] **Multi-stage builds** - Separate build and runtime stages
- [x] **Non-root user** - Container runs as UID 1000
- [x] **Minimal base image** - python:3.12-slim-bookworm
- [x] **No privilege escalation** - `allowPrivilegeEscalation: false`
- [x] **Read-only filesystem** - `readOnlyRootFilesystem: true`
- [x] **Dropped capabilities** - `capabilities.drop: ["ALL"]`
- [x] **Health checks** - HEALTHCHECK instruction in Dockerfile
- [x] **Metadata labels** - LABEL for maintainer, version, description

### 2. Kubernetes Best Practices

- [x] **Resource limits** - CPU and memory requests/limits
- [x] **Health probes** - Liveness and readiness probes
- [x] **Rolling updates** - Zero-downtime deployments
- [x] **Pod Disruption Budget** - Maintain availability during updates
- [x] **Horizontal Pod Autoscaler** - Scale based on metrics
- [x] **Security contexts** - Pod and container level security
- [x] **Namespace isolation** - Dedicated production namespace
- [x] **ConfigMaps & Secrets** - External configuration management

### 3. Service Mesh Best Practices (Istio)

- [x] **mTLS STRICT mode** - Encrypted pod-to-pod communication
- [x] **Traffic management** - Retry logic, timeouts
- [x] **Rate limiting** - Protect from abuse
- [x] **Circuit breaking** - Fail fast on errors
- [x] **TLS termination** - HTTPS at gateway level
- [x] **Observability** - Automatic metrics, tracing

### 4. CI/CD Best Practices

- [x] **Pipeline as Code** - GitHub Actions YAML
- [x] **Multi-stage pipelines** - Lint → Test → Build → Deploy
- [x] **Security gates** - Multiple security scanning tools
- [x] **Artifact management** - Docker image versioning
- [x] **Environment separation** - Different configs per environment
- [x] **Secret management** - GitHub Secrets integration
- [x] **Automated testing** - pytest with coverage

### 5. Application Best Practices

- [x] **Async programming** - FastAPI with httpx async client
- [x] **Input validation** - Pydantic models
- [x] **Structured logging** - Python logging module
- [x] **Health endpoints** - `/health` endpoint
- [x] **Metrics endpoint** - Prometheus `/metrics`
- [x] **Graceful shutdown** - Lifespan context manager
- [x] **Connection pooling** - Shared HTTP client
- [x] **Error handling** - Proper HTTP status codes

### 6. Security Best Practices

- [x] **Dependency scanning** - Snyk, pip-audit
- [x] **Container scanning** - Trivy
- [x] **Code scanning** - Bandit, SonarCloud
- [x] **Secret scanning** - TruffleHog
- [x] **SBOM generation** - Software Bill of Materials
- [x] **CVE remediation** - Regular dependency updates

---

## 🔧 Troubleshooting

### Common Issues

#### 1. ImagePullBackOff
```bash
# Check if image is loaded in Kind
docker exec -it kind-dev-control-plane crictl images | grep gists

# Reload image
kind load docker-image github-gists-api:latest --name kind-dev
```

#### 2. Pod Not Starting
```bash
# Check pod status
kubectl describe pod -l app=github-gists-api -n production

# Check logs
kubectl logs -l app=github-gists-api -n production --tail=100
```

#### 3. No External IP (LoadBalancer)
```bash
# Check MetalLB status
kubectl get pods -n metallb-system
kubectl get ipaddresspool -n metallb-system
```

#### 4. TLS Certificate Issues
```bash
# Check secret exists
kubectl get secret gists-tls-secret -n istio-system

# Recreate certificate
kubectl delete secret gists-tls-secret -n istio-system
# Re-run CD pipeline
```

#### 5. DNS Resolution
```powershell
# Windows: Add to C:\Windows\System32\drivers\etc\hosts
127.0.0.1 gists.kishore.local gists.local

# Linux/Mac: Add to /etc/hosts
sudo echo "127.0.0.1 gists.kishore.local gists.local" >> /etc/hosts
```

#### 6. GitHub Rate Limit
```bash
# Check current rate limit
curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/rate_limit

# Add token to Kubernetes
kubectl create secret generic github-token \
  --from-literal=GITHUB_TOKEN=your_token \
  -n production
kubectl rollout restart deployment/github-gists-api -n production
```

---

## 📁 Project Structure

```
eq-assessment/
├── .github/
│   └── workflows/
│       ├── ci.yml              # CI Pipeline (lint, test, scan)
│       └── cd-local.yml        # CD Pipeline (Kind deployment)
├── app/
│   ├── __init__.py
│   └── main.py                 # FastAPI application
├── helm/
│   ├── Chart.yaml              # Helm chart metadata
│   ├── values.yaml             # Default values
│   └── templates/
│       ├── _helpers.tpl        # Template helpers
│       └── deployment.yaml     # Kubernetes deployment
├── k8s/
│   ├── deployment.yaml         # K8s manifests (Deploy, Svc, HPA, PDB)
│   ├── istio-gateway.yaml      # Istio Gateway & VirtualService
│   ├── ingress-nginx.yaml      # NGINX Ingress alternative
│   └── gateway-api.yaml        # Gateway API alternative
├── monitoring/
│   ├── grafana-dashboard.json  # Grafana dashboard
│   └── prometheus-rules.yaml   # Alerting rules
├── tests/
│   ├── __init__.py
│   └── test_main.py            # pytest tests
├── Dockerfile                  # Multi-stage Docker build
├── requirements.txt            # Production dependencies
├── requirements-dev.txt        # Development dependencies
├── setup.cfg                   # Python tooling config
└── README.md                   # This file
```

---

## 🚀 Self-Hosted Runner Setup

### Prerequisites for GitHub Actions Runner

1. **Create Kind Cluster**
```powershell
kind create cluster --name kind-dev
```

2. **Install Istio**
```powershell
istioctl install --set profile=demo -y
```

3. **Configure GitHub Runner**
```powershell
# Download runner from GitHub Repository → Settings → Actions → Runners
# Configure with labels: self-hosted, Windows, X64
./config.cmd --url https://github.com/YOUR_ORG/YOUR_REPO --token YOUR_TOKEN --labels self-hosted,Windows,X64
./run.cmd
```

4. **Add Repository Secrets**
   - `GH_API_TOKEN` - GitHub personal access token (optional, for 5000 req/hour)
   - `DOCKERHUB_USERNAME` - DockerHub username (for CI)
   - `DOCKERHUB_TOKEN` - DockerHub access token (for CI)
   - `SONAR_TOKEN` - SonarCloud token (for code quality)
   - `SNYK_TOKEN` - Snyk token (for security scanning)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone repo
git clone https://github.com/your-username/eq-assessment.git
cd eq-assessment

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements-dev.txt

# Run tests
pytest -v

# Run locally
uvicorn app.main:app --reload --port 8080
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Istio](https://istio.io/) - Service mesh
- [Kubernetes](https://kubernetes.io/) - Container orchestration
- [Kind](https://kind.sigs.k8s.io/) - Kubernetes in Docker
- [GitHub](https://github.com/) - Code hosting and CI/CD

---

<div align="center">

### 🌟 Star this repository if you found it helpful!

**Built with ❤️ for the DevOps Community**

[![LinkedIn](https://img.shields.io/badge/Share%20on-LinkedIn-0077B5?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/sharing/share-offsite/?url=https://github.com/your-username/eq-assessment)
[![Twitter](https://img.shields.io/badge/Share%20on-Twitter-1DA1F2?style=for-the-badge&logo=twitter)](https://twitter.com/intent/tweet?url=https://github.com/your-username/eq-assessment&text=Check%20out%20this%20production-grade%20Kubernetes%20deployment%20with%20Istio%20and%20CI/CD!)

---

**Keywords:** `kubernetes` `istio` `service-mesh` `fastapi` `python` `docker` `github-actions` `ci-cd` `devops` `platform-engineering` `mtls` `metallb` `kind` `helm` `prometheus` `grafana` `security` `trivy` `snyk`

</div>
]]>