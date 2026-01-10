# 🏠 Local Deployment Guide - Kind Cluster on Windows

Complete guide to deploy the GitHub Gists API to your local Kind cluster using Docker Desktop.

---

## ✅ What You Have

- ✅ **Windows machine**
- ✅ **Docker Desktop** (with Kubernetes enabled)
- ✅ **WSL** (Windows Subsystem for Linux)
- ✅ **Kind cluster** (Kubernetes in Docker)

---

## 🚀 Quick Start (One Command!)

```powershell
# Run from PowerShell (in project root)
.\deploy-local.ps1
```

**That's it!** The script will:
1. ✅ Check prerequisites (Docker, kubectl, Kind)
2. ✅ Create Kind cluster if needed
3. ✅ Build Docker image
4. ✅ Load image into Kind
5. ✅ Deploy to Kubernetes
6. ✅ Test all endpoints
7. ✅ Display access URLs

---

## 📋 Detailed Setup

### **Option 1: Automated Deployment (Recommended)**

```powershell
# Navigate to project
cd d:\Kishore\eq-assessment

# Make script executable and run
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\deploy-local.ps1
```

**Access your API**:
```
Health:  http://localhost:8080/health
Metrics: http://localhost:8080/metrics
Gists:   http://localhost:8080/octocat
```

---

### **Option 2: Manual Step-by-Step**

#### **Step 1: Install Prerequisites**

**Install Kind** (if not already installed):
```powershell
# Via Chocolatey
choco install kind

# OR download from: https://kind.sigs.k8s.io/docs/user/quick-start/#installation
```

**Verify installations**:
```powershell
docker --version          # Docker Desktop
kubectl version --client  # Kubernetes CLI
kind version              # Kind
```

#### **Step 2: Create Kind Cluster**

```powershell
# Create cluster with port mapping
kind create cluster --name kind --config - @"
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  extraPortMappings:
  - containerPort: 30080
    hostPort: 8080
    protocol: TCP
"@

# Verify cluster
kubectl cluster-info --context kind-kind
kubectl get nodes
```

#### **Step 3: Build and Load Image**

```powershell
# Build Docker image
docker build -t github-gists-api:local .

# Load into Kind cluster
kind load docker-image github-gists-api:local --name kind

# Verify image in cluster
docker exec -it kind-control-plane crictl images | Select-String github-gists-api
```

#### **Step 4: Create Namespace**

```powershell
kubectl create namespace production
kubectl config set-context --current --namespace=production
```

#### **Step 5: Update Deployment for Local**

Create `k8s/deployment-local.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: github-gists-api
  namespace: production
  labels:
    app: github-gists-api
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "8080"
    prometheus.io/path: "/metrics"
spec:
  replicas: 2
  selector:
    matchLabels:
      app: github-gists-api
  template:
    metadata:
      labels:
        app: github-gists-api
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
        prometheus.io/path: "/metrics"
    spec:
      containers:
      - name: api
        image: github-gists-api:local  # Local image
        imagePullPolicy: Never          # Don't pull from registry
        ports:
        - containerPort: 8080
          name: http
        env:
        - name: LOG_LEVEL
          value: "info"
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: github-gists-api
  namespace: production
  labels:
    app: github-gists-api
spec:
  type: NodePort
  selector:
    app: github-gists-api
  ports:
  - name: http
    port: 80
    targetPort: 8080
    nodePort: 30080  # Access via localhost:8080
    protocol: TCP
  - name: metrics
    port: 8080
    targetPort: 8080
    protocol: TCP
```

#### **Step 6: Deploy**

```powershell
# Apply deployment
kubectl apply -f k8s/deployment-local.yaml

# Wait for pods to be ready
kubectl rollout status deployment/github-gists-api -n production

# Check pods
kubectl get pods -n production
```

#### **Step 7: Test**

```powershell
# Test endpoints
Invoke-RestMethod http://localhost:8080/health
Invoke-RestMethod http://localhost:8080/octocat
Invoke-RestMethod http://localhost:8080/metrics
```

---

## 🔧 Useful Commands

### **View Resources**

```powershell
# Pods
kubectl get pods -n production

# Services
kubectl get svc -n production

# Deployments
kubectl get deployments -n production

# Logs (follow)
kubectl logs -n production -l app=github-gists-api -f

# Pod details
kubectl describe pods -n production -l app=github-gists-api
```

### **Port Forwarding** (Alternative access method)

```powershell
# Forward service to localhost:8080
kubectl port-forward -n production svc/github-gists-api 8080:80

# Access API
curl http://localhost:8080/health
```

### **Update Image**

```powershell
# Rebuild image
docker build -t github-gists-api:local .

# Reload into Kind
kind load docker-image github-gists-api:local --name kind

# Restart pods to pick up new image
kubectl rollout restart deployment/github-gists-api -n production
```

### **Cleanup**

```powershell
# Delete deployment
kubectl delete -f k8s/deployment-local.yaml

# Delete namespace
kubectl delete namespace production

# Delete Kind cluster
kind delete cluster --name kind
```

---

## 🎯 GitHub Actions with Self-Hosted Runner (Optional)

If you want GitHub Actions to deploy to your local Kind cluster:

### **Step 1: Setup Self-Hosted Runner**

```powershell
# Run setup script
.\setup-self-hosted-runner.ps1
```

### **Step 2: Configure Runner**

1. Go to: https://github.com/kishoredevops55/eq-assessment/settings/actions/runners/new
2. Copy the token
3. Run in `C:\actions-runner`:
   ```powershell
   .\config.cmd --url https://github.com/kishoredevops55/eq-assessment --token YOUR_TOKEN
   ```

### **Step 3: Start Runner**

```powershell
# Run interactively
.\run.cmd

# OR install as Windows Service
.\svc.sh install
.\svc.sh start
```

### **Step 4: Use in Workflow**

The workflow `.github/workflows/cd-local.yml` is already configured for self-hosted runners:
```yaml
runs-on: self-hosted  # Uses your Windows machine
```

---

## 🐳 Using Docker Desktop Kubernetes (Alternative to Kind)

If you prefer Docker Desktop's built-in Kubernetes:

### **Enable Kubernetes in Docker Desktop**

1. Docker Desktop → Settings → Kubernetes
2. Enable "Enable Kubernetes"
3. Click "Apply & Restart"

### **Deploy**

```powershell
# Use docker-desktop context
kubectl config use-context docker-desktop

# Create namespace
kubectl create namespace production

# Deploy
kubectl apply -f k8s/deployment-local.yaml

# Access (Docker Desktop automatically maps NodePort)
curl http://localhost:8080/health
```

---

## 🔍 Troubleshooting

### **Issue: Pods in CrashLoopBackOff**

```powershell
# Check logs
kubectl logs -n production -l app=github-gists-api --tail=50

# Check pod events
kubectl describe pods -n production -l app=github-gists-api
```

### **Issue: Image not found**

```powershell
# Verify image loaded in Kind
docker exec -it kind-control-plane crictl images

# Reload image
kind load docker-image github-gists-api:local --name kind

# Restart pods
kubectl rollout restart deployment/github-gists-api -n production
```

### **Issue: Port 8080 already in use**

```powershell
# Find process using port
netstat -ano | findstr :8080

# Kill process (replace PID)
taskkill /PID <PID> /F

# OR use different port in Kind cluster config
```

### **Issue: Cannot access API**

```powershell
# Check service
kubectl get svc -n production

# Check if pods are ready
kubectl get pods -n production

# Port forward directly to pod
kubectl port-forward -n production pod/<POD_NAME> 8080:8080
```

---

## 📊 Monitoring on Local Cluster

### **Install Prometheus (Optional)**

```powershell
# Add Prometheus Helm repo
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install Prometheus
helm install prometheus prometheus-community/kube-prometheus-stack `
  --namespace monitoring --create-namespace

# Access Prometheus
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090

# Access Grafana
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
# Default credentials: admin / prom-operator
```

### **Import Dashboard**

1. Open Grafana: http://localhost:3000
2. Login (admin / prom-operator)
3. Import `monitoring/grafana-dashboard.json`
4. View metrics from your API

---

## ✅ Verification Checklist

- [ ] Kind cluster running (`kind get clusters`)
- [ ] Image built (`docker images | grep github-gists-api`)
- [ ] Image loaded in Kind (`docker exec -it kind-control-plane crictl images`)
- [ ] Namespace created (`kubectl get ns production`)
- [ ] Deployment created (`kubectl get deployment -n production`)
- [ ] Pods running (`kubectl get pods -n production`)
- [ ] Service created (`kubectl get svc -n production`)
- [ ] Health endpoint works (`curl http://localhost:8080/health`)
- [ ] Metrics endpoint works (`curl http://localhost:8080/metrics`)
- [ ] User endpoint works (`curl http://localhost:8080/octocat`)

---

## 🎓 Comparison: CI vs Local

| Aspect | GitHub Actions CI/CD | Local Kind Deployment |
|--------|---------------------|----------------------|
| **Image Registry** | DockerHub | Local Docker |
| **Runners** | GitHub-hosted | Self-hosted (optional) |
| **Cluster** | Remote K8s | Local Kind |
| **Access** | Public URL | localhost:8080 |
| **Cost** | Free tier limits | Completely free |
| **Speed** | ~5-10 minutes | ~2 minutes |
| **Use Case** | Production | Development/Testing |

---

## 🚀 Next Steps

1. ✅ Deploy locally with `.\deploy-local.ps1`
2. ✅ Test all endpoints
3. ✅ Make code changes
4. ✅ Rebuild and redeploy
5. ✅ Optional: Setup self-hosted runner for GitHub Actions
6. ✅ Optional: Install Prometheus for monitoring

---

**You now have a complete local Kubernetes development environment!** 🎉
