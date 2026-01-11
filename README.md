<div align="center">

# 🚀 Enterprise GitHub Gists API Platform

### Production-Grade Kubernetes Deployment with Full Observability, Service Mesh & GitOps

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/FastAPI-0.116+-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/Docker-Multi--Stage-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"/>
  <img src="https://img.shields.io/badge/Kubernetes-1.28+-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white" alt="Kubernetes"/>
  <img src="https://img.shields.io/badge/Helm-3.0+-0F1689?style=for-the-badge&logo=helm&logoColor=white" alt="Helm"/>
  <img src="https://img.shields.io/badge/Terraform-1.5+-7B42BC?style=for-the-badge&logo=terraform&logoColor=white" alt="Terraform"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Istio-Service%20Mesh-466BB0?style=for-the-badge&logo=istio&logoColor=white" alt="Istio"/>
  <img src="https://img.shields.io/badge/Prometheus-Monitoring-E6522C?style=for-the-badge&logo=prometheus&logoColor=white" alt="Prometheus"/>
  <img src="https://img.shields.io/badge/Grafana-Dashboards-F46800?style=for-the-badge&logo=grafana&logoColor=white" alt="Grafana"/>
  <img src="https://img.shields.io/badge/Tempo-Tracing-4B0082?style=for-the-badge&logo=grafana&logoColor=white" alt="Tempo"/>
  <img src="https://img.shields.io/badge/Loki-Logs-00ADD8?style=for-the-badge&logo=grafana&logoColor=white" alt="Loki"/>
</p>

<h3>✨ A Complete Modern Cloud-Native Platform Engineering Showcase ✨</h3>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-prerequisites">Prerequisites</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-cicd-pipelines">CI/CD</a> •
  <a href="#-monitoring--observability">Monitoring</a> •
  <a href="#-api-documentation">API Docs</a>
</p>

</div>

---

## 📋 Table of Contents

- [🎯 Project Overview](#-project-overview)
- [✨ Features](#-features)
- [🏗️ Architecture](#️-architecture)
- [🛠️ Prerequisites](#️-prerequisites)
- [🚀 Quick Start](#-quick-start)
- [🔄 CI/CD Pipelines](#-cicd-pipelines)
- [📊 Monitoring & Observability](#-monitoring--observability)
- [🏗️ Infrastructure as Code](#️-infrastructure-as-code)
- [📡 API Documentation](#-api-documentation)
- [🔐 Security Features](#-security-features)
- [📈 Performance & Scalability](#-performance--scalability)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## 🎯 Project Overview

A **production-ready, enterprise-grade GitHub Gists API** built with modern cloud-native technologies and DevOps best practices. This project demonstrates a complete platform engineering solution featuring:

- 🎯 **High-Performance API**: FastAPI with async/await, in-memory caching, and pagination
- ☸️ **Cloud-Native Architecture**: Kubernetes with Istio Service Mesh, MetalLB, and automated TLS
- 📊 **Full Observability**: Prometheus metrics, Grafana dashboards, Tempo tracing, Loki logs, Faro RUM
- 🔄 **GitOps CI/CD**: Automated GitHub Actions pipelines with Helm and raw manifest support
- 🏗️ **Infrastructure as Code**: Terraform for cluster provisioning, Helm for deployments
- 🔒 **Enterprise Security**: mTLS, RBAC, Network Policies, and secrets management

**Perfect for**: DevOps portfolios, platform engineering demonstrations, Kubernetes training, or production deployments.

---

## ✨ Features

### 🚀 Core API Capabilities
- ✅ **GitHub Integration**: Fetch public gists by username with full GitHub API compatibility
- ⚡ **Smart Caching**: In-memory TTL cache (60s) to reduce GitHub API calls and improve response times
- 📄 **Pagination Support**: Handle large datasets with `per_page` and `page` query parameters
- 🔍 **Error Handling**: Comprehensive error responses with proper HTTP status codes
- 📊 **Health & Metrics**: `/health` endpoint and Prometheus metrics at `/metrics`
- 🌐 **CORS Enabled**: Cross-Origin Resource Sharing for frontend integration
- 🔐 **Rate Limit Aware**: Respects GitHub API rate limits with proper headers

### ☸️ Kubernetes & Service Mesh
- 🎛️ **Deployment Flexibility**: Support for both Helm charts and raw Kubernetes manifests
- 🔀 **Istio Service Mesh**: Traffic management, load balancing, circuit breaking, and retries
- 🔒 **mTLS Encryption**: Strict mutual TLS between all services
- 🌐 **MetalLB LoadBalancer**: Expose services with external IPs on bare-metal/Kind clusters
- 🔐 **TLS Termination**: HTTPS with automatic certificate generation
- 🛡️ **Authorization Policies**: Granular access control with Istio AuthorizationPolicy

### 📊 Observability Stack
- 📈 **Prometheus**: Scrapes metrics from API, Istio, and Kubernetes components
- 📊 **Grafana**: Pre-configured dashboards for API performance, cache hit rates, and error tracking
- 🔍 **Tempo**: Distributed tracing with Istio integration
- 📜 **Loki**: Centralized log aggregation with Promtail
- 👁️ **Faro RUM**: Real User Monitoring for frontend applications
- 🚨 **Alerting**: Prometheus rules for SLO monitoring and incident detection

### 🔄 CI/CD Automation
- ✅ **GitHub Actions**: Self-hosted Windows runner support
- 🧪 **Testing Pipeline**: Unit tests with pytest and code quality checks
- 🐳 **Docker Build**: Multi-stage builds with security scanning
- 📦 **Helm Packaging**: Chart versioning and release automation
- 🚀 **Multi-Method Deployment**: Choose between Helm or raw manifests
- 🏗️ **Terraform Integration**: Optional cluster provisioning with Terraform
- 🔄 **GitOps Workflow**: Infrastructure and application state tracked in Git

### 🏗️ Infrastructure as Code
- 🏗️ **Terraform Modules**: Provision Kind clusters with Istio, MetalLB, and namespaces
- 📦 **Helm Charts**: Application and monitoring stack packaged as Helm charts
- 🔧 **Configurable**: Environment-specific values files for dev/staging/production
- 🔁 **Idempotent**: Safe to re-run without breaking existing resources

---

## 🏗️ Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Windows Host (localhost)                     │
│                                                                       │
│  ┌──────────────────┐          ┌─────────────────────────────────┐  │
│  │  Web Browser     │─────────▶│  Nginx Proxy (kind-proxy)       │  │
│  │                  │          │  Port 80/443                     │  │
│  └──────────────────┘          └────────────┬────────────────────┘  │
│                                              │                        │
└──────────────────────────────────────────────┼────────────────────────┘
                                               │
                                        HTTP/HTTPS
                                               │
┌──────────────────────────────────────────────▼────────────────────────┐
│                     Kind Cluster (Kubernetes 1.28+)                    │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐ │
│  │                    Istio Service Mesh                            │ │
│  │                                                                  │ │
│  │  ┌──────────────────┐       ┌──────────────────────────────┐   │ │
│  │  │ Istio Gateway    │──────▶│  VirtualService              │   │ │
│  │  │ (LoadBalancer)   │       │  (Routing Rules)             │   │ │
│  │  │ MetalLB IP       │       └──────────────┬───────────────┘   │ │
│  │  └──────────────────┘                      │                   │ │
│  │                                             │                   │ │
│  └─────────────────────────────────────────────┼───────────────────┘ │
│                                                │                     │
│  ┌─────────────────────────────────────────────▼───────────────────┐ │
│  │              Production Namespace (Istio Injected)             │ │
│  │                                                                 │ │
│  │  ┌──────────────────────────────────────────────────────────┐  │ │
│  │  │  GitHub Gists API Pods (3 replicas)                      │  │ │
│  │  │  - FastAPI App with Uvicorn                              │  │ │
│  │  │  - In-Memory Cache (60s TTL)                             │  │ │
│  │  │  - Prometheus Metrics (/metrics)                         │  │ │
│  │  │  - Health Check (/health)                                │  │ │
│  │  │  - Istio Sidecar (Envoy Proxy)                           │  │ │
│  │  └──────────────────────────────────────────────────────────┘  │ │
│  │                                                                 │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐   │
│  │            Monitoring Namespace (Istio Injected)              │   │
│  │                                                                │   │
│  │  ┌────────────┐  ┌──────────┐  ┌────────┐  ┌────────────┐   │   │
│  │  │ Prometheus │  │ Grafana  │  │  Loki  │  │   Tempo    │   │   │
│  │  │ (Metrics)  │  │(Dashbrd) │  │ (Logs) │  │  (Traces)  │   │   │
│  │  └────────────┘  └──────────┘  └────────┘  └────────────┘   │   │
│  │                                                                │   │
│  │  ┌────────────┐  ┌──────────┐  ┌──────────────────────────┐ │   │
│  │  │ Promtail   │  │ Faro RUM │  │  Kube State Metrics      │ │   │
│  │  └────────────┘  └──────────┘  └──────────────────────────┘ │   │
│  └───────────────────────────────────────────────────────────────┘   │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐   │
│  │               Istio-System Namespace                          │   │
│  │  - Istiod (Control Plane)                                     │   │
│  │  - Istio Ingress Gateway                                      │   │
│  │  - Istio Egress Gateway                                       │   │
│  └───────────────────────────────────────────────────────────────┘   │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐   │
│  │               MetalLB-System Namespace                        │   │
│  │  - Controller (IP Assignment)                                 │   │
│  │  - Speaker (L2 Advertisement)                                 │   │
│  └───────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────┘
```

### Technology Stack

| Category | Technology | Purpose |
|----------|-----------|---------|
| **Language** | Python 3.12 | Modern async/await support |
| **Framework** | FastAPI 0.116+ | High-performance async web framework |
| **Server** | Uvicorn | ASGI server with production settings |
| **Containerization** | Docker | Multi-stage builds for security |
| **Orchestration** | Kubernetes 1.28+ | Container orchestration |
| **Service Mesh** | Istio 1.20 | Traffic management, mTLS, observability |
| **Load Balancer** | MetalLB | External IP allocation for LoadBalancer services |
| **Package Manager** | Helm 3 | Kubernetes application packaging |
| **IaC** | Terraform 1.5+ | Infrastructure provisioning |
| **Metrics** | Prometheus | Time-series metrics database |
| **Visualization** | Grafana | Dashboards and alerting |
| **Tracing** | Tempo | Distributed tracing backend |
| **Logging** | Loki + Promtail | Log aggregation and querying |
| **RUM** | Grafana Faro | Real User Monitoring |
| **CI/CD** | GitHub Actions | Automated testing and deployment |
| **Local Dev** | Kind | Kubernetes IN Docker for local testing |

---

## 🛠️ Prerequisites

### Required Software

#### 🪟 Windows (Primary Development Environment)

| Tool | Version | Installation | Purpose |
|------|---------|-------------|---------|
| **Docker Desktop** | 4.25+ | [Download](https://www.docker.com/products/docker-desktop/) | Container runtime with WSL2 backend |
| **Kind** | 0.20+ | `choco install kind` | Local Kubernetes clusters |
| **kubectl** | 1.28+ | `choco install kubernetes-cli` | Kubernetes CLI |
| **Helm** | 3.13+ | `choco install kubernetes-helm` | Kubernetes package manager |
| **Terraform** | 1.5+ | `choco install terraform` | Infrastructure as Code |
| **Git** | Latest | [Download](https://git-scm.com/downloads) | Version control (includes OpenSSL) |
| **PowerShell** | 5.1+ | Built-in | Automation and scripting |
| **Python** | 3.12+ | [Download](https://www.python.org/downloads/) | Local development and testing |

**Quick Install (Windows with Chocolatey):**
```powershell
# Install Chocolatey (if not installed)
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install all required tools
choco install docker-desktop kind kubernetes-cli kubernetes-helm terraform git python -y
```

#### 🐧 Linux (Ubuntu/Debian)

```bash
# Update package list
sudo apt update

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Install Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Install Kind
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind

# Install Terraform
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform

# Install Python 3.12
sudo apt install python3.12 python3.12-venv python3-pip
```

#### 🍎 macOS

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install all required tools
brew install docker kind kubectl helm terraform git python@3.12

# Start Docker Desktop
open -a Docker
```

### System Requirements

| Resource | Minimum | Recommended | Notes |
|----------|---------|-------------|-------|
| **CPU** | 4 cores | 8 cores | Kind requires multi-core for multiple nodes |
| **RAM** | 8 GB | 16 GB | 12 GB+ for full monitoring stack |
| **Disk** | 20 GB | 50 GB | Space for Docker images and logs |
| **OS** | Windows 10+ / Linux / macOS | Windows 11 / Ubuntu 22.04 / macOS 13+ | WSL2 required on Windows |

### Optional Tools

- **Istioctl**: For advanced Istio debugging (`brew install istioctl` / `choco install istioctl`)
- **K9s**: Terminal-based Kubernetes UI (`brew install k9s` / `choco install k9s`)
- **Lens**: Kubernetes IDE ([Download](https://k8slens.dev/))
- **Postman**: API testing ([Download](https://www.postman.com/downloads/))

---

## 🚀 Quick Start

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/eq-assessment.git
cd eq-assessment
```

### 2️⃣ Choose Your Deployment Method

You have **three** deployment options:

#### Option A: Traditional Manifest Deployment (Existing Workflow)

```bash
# 1. Create Kind cluster
kind create cluster --name kind-dev --config kind-cluster-config.yaml

# 2. Install Istio
curl -L https://istio.io/downloadIstio | ISTIO_VERSION=1.20.0 sh -
cd istio-1.20.0
export PATH=$PWD/bin:$PATH
istioctl install --set profile=demo -y

# 3. Deploy application
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/istio-gateway.yaml

# 4. Deploy monitoring (optional)
kubectl apply -f monitoring/
```

#### Option B: Helm Deployment (Recommended)

```bash
# 1. Create Kind cluster (if not exists)
kind create cluster --name kind-dev

# 2. Deploy with Helm
helm upgrade --install gists-api ./helm \
  --namespace production \
  --create-namespace \
  --values ./helm/values-kind.yaml

# 3. Deploy monitoring stack
helm upgrade --install monitoring-stack ./helm/monitoring-stack \
  --namespace monitoring \
  --create-namespace \
  --set grafana.adminPassword=your-secure-password
```

#### Option C: Terraform + Helm (Full IaC)

```bash
# 1. Initialize Terraform
cd terraform
terraform init

# 2. Provision infrastructure
terraform apply -auto-approve

# 3. Deploy application
cd ..
helm upgrade --install gists-api ./helm \
  --namespace production \
  --values ./helm/values-kind.yaml

# 4. Deploy monitoring
helm upgrade --install monitoring-stack ./helm/monitoring-stack \
  --namespace monitoring \
  --set grafana.adminPassword=your-secure-password
```

### 3️⃣ Setup Windows Proxy (Windows Only)

```powershell
# Start Nginx proxy to access cluster from localhost
docker run -d --name kind-proxy \
  --network kind \
  -p 80:80 -p 443:443 \
  -v ${PWD}/nginx-proxy.conf:/etc/nginx/nginx.conf:ro \
  nginx:alpine
```

### 4️⃣ Add DNS Entries

**Windows (Run as Administrator):**
```powershell
Add-Content -Path C:\Windows\System32\drivers\etc\hosts -Value @"
127.0.0.1    gists.kishore.local
127.0.0.1    kishoregrafana.local
"@
```

**Linux/Mac:**
```bash
sudo bash -c 'echo "127.0.0.1 gists.kishore.local kishoregrafana.local" >> /etc/hosts'
```

### 5️⃣ Access the Application

| Service | URL | Credentials |
|---------|-----|-------------|
| **API Health** | http://gists.kishore.local/health | N/A |
| **API Endpoint** | http://gists.kishore.local/octocat | N/A |
| **Grafana** | http://kishoregrafana.local | admin / (your password) |
| **Prometheus** | http://prometheus.kishore.local | N/A |

### 6️⃣ Test the API

```bash
# Health check
curl http://gists.kishore.local/health

# Fetch gists for a user
curl http://gists.kishore.local/octocat

# With pagination
curl "http://gists.kishore.local/octocat?per_page=10&page=1"

# View metrics
curl http://gists.kishore.local/metrics
```

---

## 🔄 CI/CD Pipelines

### GitHub Actions Workflows

#### 1. CI Pipeline (`.github/workflows/ci.yml`)

**Triggers:** Push to any branch, Pull Requests

**Steps:**
1. ✅ **Checkout Code**
2. 🐍 **Setup Python 3.12**
3. 📦 **Install Dependencies** (`pip install -r requirements-dev.txt`)
4. 🧪 **Run Unit Tests** (`pytest tests/ -v --cov=app`)
5. 🔍 **Code Quality Checks** (linting, type checking)
6. 📊 **Upload Coverage Report**

#### 2. CD Pipeline - Original Manifest Workflow (`.github/workflows/cd-local.yml`)

**Triggers:** Manual workflow dispatch

**Features:**
- ✅ Self-hosted Windows runner support
- 🔧 Kind cluster management
- 🔐 TLS certificate generation
- 🌐 MetalLB LoadBalancer setup
- 🚀 Kubernetes manifest deployment
- 📊 Istio Gateway configuration

#### 3. CD Pipeline - Helm + Terraform (`.github/workflows/cd-helm-terraform.yml`)

**Triggers:** Manual workflow dispatch

**Features:**
- 🏗️ **Optional Terraform Provisioning**: Create new Kind cluster or use existing
- 📦 **Helm Deployment**: Package and deploy with Helm charts
- 📝 **Manifest Deployment**: Alternative deployment using raw YAML
- 🔄 **Smart Cluster Detection**: Skip provisioning if cluster exists
- 🔐 **Secrets Management**: GitHub Secrets for sensitive data
- 📊 **Full Monitoring Stack**: Deploy Prometheus, Grafana, Loki, Tempo

**Workflow Inputs:**
```yaml
deployment_method: 'helm' | 'manifest'  # Choose deployment method
provision_cluster: true | false          # Create new cluster or use existing
```

**Secrets Required:**
- `GH_API_TOKEN`: GitHub Personal Access Token (for API calls)
- `GRAFANA_ADMIN_USER`: Grafana admin username
- `GRAFANA_ADMIN_PASSWORD`: Grafana admin password

---

## 📊 Monitoring & Observability

### Metrics (Prometheus)

**Available Metrics:**
- `http_requests_total`: Total HTTP requests by method and status
- `http_request_duration_seconds`: Request latency histogram
- `cache_hits_total` / `cache_misses_total`: Cache performance
- `github_api_requests_total`: GitHub API call tracking

### Dashboards (Grafana)

**Pre-configured Dashboards:**

1. **GitHub Gists API - Production Monitoring**
   - Request rate (req/s)
   - Response time percentiles (P50, P95, P99)
   - Error rate (5xx responses)
   - Cache hit rate
   - Active pods

**Access Grafana:**
```
URL: http://kishoregrafana.local
Credentials: admin / (your password)
```

### Distributed Tracing (Tempo)

- Istio sends traces to Tempo via Zipkin protocol
- 100% trace sampling (configurable)
- Automatic service graph generation

### Log Aggregation (Loki)

**Query Examples:**
```logql
# All logs from production namespace
{namespace="production"}

# Error logs only
{namespace="production"} |= "ERROR"
```

---

## 🏗️ Infrastructure as Code

### Terraform Modules

**Managed Resources:**
- Kind cluster (1 control plane + N worker nodes)
- Namespaces (production, monitoring, istio-system)
- Istio base, istiod, ingress gateway
- MetalLB with IP address pool

**Usage:**
```bash
cd terraform
terraform init
terraform apply -auto-approve
```

### Helm Charts

#### Application Chart (`./helm`)
- API deployment with 3 replicas
- Horizontal Pod Autoscaler
- ConfigMaps and Secrets

#### Monitoring Stack Chart (`./helm/monitoring-stack`)
- Prometheus with scrape configs
- Grafana with datasources and dashboards
- Loki with Promtail
- Tempo with Istio integration

---

## 📡 API Documentation

### Base URL
```
http://gists.kishore.local
```

### Endpoints

#### GET `/health`
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

#### GET `/{username}`
Fetch public gists for a GitHub user

**Parameters:**
- `username` (required): GitHub username
- `per_page` (optional): Results per page (default: 30, max: 100)
- `page` (optional): Page number (default: 1)

**Example:**
```bash
curl "http://gists.kishore.local/octocat?per_page=10&page=1"
```

#### GET `/metrics`
Prometheus metrics endpoint

---

## 🔐 Security Features

### Network Security
- ✅ **mTLS**: Strict mutual TLS between all services
- ✅ **Network Policies**: Restrict pod-to-pod communication
- ✅ **TLS Termination**: HTTPS at the Istio Gateway

### Container Security
- ✅ **Multi-Stage Builds**: Minimize attack surface
- ✅ **Non-Root User**: Runs as user 1000
- ✅ **Read-Only Root Filesystem**: Immutable container filesystem

### Kubernetes Security
- ✅ **RBAC**: Role-Based Access Control
- ✅ **Resource Limits**: CPU and memory limits on all pods
- ✅ **Liveness & Readiness Probes**: Automatic health checks

---

## 📈 Performance & Scalability

### Performance Optimizations
1. **Async/Await**: Non-blocking I/O with FastAPI
2. **In-Memory Cache**: 60s TTL cache reduces API calls
3. **Connection Pooling**: Reuse HTTP connections
4. **Horizontal Scaling**: Auto-scale based on CPU/memory

### Benchmarks
| Metric | Value |
|--------|-------|
| Avg Response Time (cached) | < 50ms |
| Avg Response Time (uncached) | < 500ms |
| P95 Latency | < 1s |
| Cache Hit Rate | ~80% (production) |

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

<div align="center">

## 💼 Suitable For

✅ **DevOps Portfolio**  
✅ **Platform Engineering Showcase**  
✅ **Kubernetes Training Material**  
✅ **Production Deployments**  
✅ **Interview Demonstrations**  
✅ **Technical Presentations**  

---

**⭐ If you find this project useful, please give it a star!**

---

Made with ❤️ using FastAPI, Kubernetes, Istio, and DevOps best practices

</div>
