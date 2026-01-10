# Local Deployment Script for Kind Cluster
# Run this from PowerShell: .\deploy-local.ps1

Write-Host "🚀 Deploying GitHub Gists API to Kind Cluster" -ForegroundColor Green
Write-Host ""

# Configuration
$IMAGE_NAME = "github-gists-api"
$IMAGE_TAG = "local"
$DOCKERHUB_USERNAME = $env:DOCKERHUB_USERNAME  # Set this in your environment
$NAMESPACE = "production"
$KIND_CLUSTER_NAME = "kind-dev"  # Use your local kind cluster name

# Step 1: Check prerequisites
Write-Host "📋 Checking prerequisites..." -ForegroundColor Yellow

# Check Docker
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker not found. Please install Docker Desktop." -ForegroundColor Red
    exit 1
}
Write-Host "✅ Docker Desktop: Found"

# Check kubectl
if (-not (Get-Command kubectl -ErrorAction SilentlyContinue)) {
    Write-Host "❌ kubectl not found. Please enable Kubernetes in Docker Desktop." -ForegroundColor Red
    exit 1
}
Write-Host "✅ kubectl: Found"

# Check Kind
if (-not (Get-Command kind -ErrorAction SilentlyContinue)) {
    Write-Host "⚠️  Kind not found. Installing via Chocolatey..." -ForegroundColor Yellow
    choco install kind -y
}
Write-Host "✅ Kind: Found"

# Step 2: Verify Kind cluster exists
Write-Host ""
Write-Host "🔍 Checking Kind cluster..." -ForegroundColor Yellow

$clusters = kind get clusters 2>$null
if ($clusters -notcontains $KIND_CLUSTER_NAME) {
    Write-Host "Creating Kind cluster ($KIND_CLUSTER_NAME)..."
    kind create cluster --name $KIND_CLUSTER_NAME --config - @"
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  extraPortMappings:
  - containerPort: 30080
    hostPort: 8080
    protocol: TCP
"@
    Write-Host "✅ Kind cluster created"
} else {
    Write-Host "✅ Kind cluster already exists: $KIND_CLUSTER_NAME"
}

# Set kubectl context
kubectl config use-context kind-$KIND_CLUSTER_NAME
Write-Host "✅ Using context: kind-$KIND_CLUSTER_NAME"

# Step 3: Build Docker image
Write-Host ""
Write-Host "🐳 Building Docker image..." -ForegroundColor Yellow
docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker build failed" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Image built: ${IMAGE_NAME}:${IMAGE_TAG}"

# Step 4: Load image into Kind
Write-Host ""
Write-Host "📦 Loading image into Kind cluster..." -ForegroundColor Yellow
kind load docker-image ${IMAGE_NAME}:${IMAGE_TAG} --name $KIND_CLUSTER_NAME
Write-Host "✅ Image loaded into Kind"

# Step 5: Create namespace
Write-Host ""
Write-Host "📁 Creating namespace..." -ForegroundColor Yellow
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -
Write-Host "✅ Namespace: $NAMESPACE"

# Step 6: Update deployment YAML
Write-Host ""
Write-Host "📝 Updating deployment configuration..." -ForegroundColor Yellow

$deploymentContent = Get-Content "k8s/deployment.yaml" -Raw
$deploymentContent = $deploymentContent -replace 'YOUR_DOCKERHUB_USERNAME/github-gists-api:latest', "${IMAGE_NAME}:${IMAGE_TAG}"
$deploymentContent = $deploymentContent -replace 'imagePullPolicy: Always', 'imagePullPolicy: Never'

# Save temporary deployment file
Set-Content -Path "k8s/deployment-local.yaml" -Value $deploymentContent

# Update service to use NodePort for local access
$serviceContent = @"
apiVersion: v1
kind: Service
metadata:
  name: github-gists-api
  namespace: $NAMESPACE
  labels:
    app: github-gists-api
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "8080"
    prometheus.io/path: "/metrics"
spec:
  type: NodePort
  selector:
    app: github-gists-api
  ports:
  - name: http
    port: 80
    targetPort: 8080
    nodePort: 30080
    protocol: TCP
  - name: metrics
    port: 8080
    targetPort: 8080
    protocol: TCP
"@
Set-Content -Path "k8s/service-local.yaml" -Value $serviceContent

Write-Host "✅ Configuration updated for local deployment"

# Step 7: Deploy to Kind
Write-Host ""
Write-Host "🚀 Deploying to Kind cluster..." -ForegroundColor Yellow

kubectl apply -f k8s/deployment-local.yaml
kubectl apply -f k8s/service-local.yaml

Write-Host "⏳ Waiting for deployment to be ready..."
kubectl rollout status deployment/github-gists-api -n $NAMESPACE --timeout=3m

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Deployment failed" -ForegroundColor Red
    kubectl get pods -n $NAMESPACE
    kubectl describe pods -n $NAMESPACE -l app=github-gists-api
    exit 1
}

Write-Host "✅ Deployment successful!"

# Step 8: Verify deployment
Write-Host ""
Write-Host "🔍 Verifying deployment..." -ForegroundColor Yellow

Write-Host ""
Write-Host "Pods:"
kubectl get pods -n $NAMESPACE -l app=github-gists-api

Write-Host ""
Write-Host "Services:"
kubectl get svc -n $NAMESPACE -l app=github-gists-api

# Step 9: Test the API
Write-Host ""
Write-Host "🧪 Testing API endpoints..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

try {
    # Test health endpoint
    Write-Host ""
    Write-Host "Testing http://localhost:8080/health"
    $health = Invoke-RestMethod http://localhost:8080/health
    Write-Host "✅ Health: $($health.status)" -ForegroundColor Green
    
    # Test user endpoint
    Write-Host ""
    Write-Host "Testing http://localhost:8080/octocat"
    $gists = Invoke-RestMethod http://localhost:8080/octocat
    Write-Host "✅ Found $($gists.Count) gists for octocat" -ForegroundColor Green
    
    # Test metrics endpoint
    Write-Host ""
    Write-Host "Testing http://localhost:8080/metrics"
    $metrics = Invoke-WebRequest http://localhost:8080/metrics -UseBasicParsing
    if ($metrics.Content -like "*http_requests_total*") {
        Write-Host "✅ Metrics endpoint working" -ForegroundColor Green
    }
    
} catch {
    Write-Host "⚠️  API not yet accessible. Checking pods..." -ForegroundColor Yellow
    kubectl logs -n $NAMESPACE -l app=github-gists-api --tail=20
}

# Step 10: Display access information
Write-Host ""
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "✅ DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""
Write-Host "📍 API Endpoints:" -ForegroundColor Cyan
Write-Host "   Health:  http://localhost:8080/health"
Write-Host "   Metrics: http://localhost:8080/metrics"
Write-Host "   Gists:   http://localhost:8080/<username>"
Write-Host ""
Write-Host "🔧 Useful Commands:" -ForegroundColor Cyan
Write-Host "   View pods:    kubectl get pods -n $NAMESPACE"
Write-Host "   View logs:    kubectl logs -n $NAMESPACE -l app=github-gists-api -f"
Write-Host "   Port forward: kubectl port-forward -n $NAMESPACE svc/github-gists-api 8080:80"
Write-Host "   Delete app:   kubectl delete -f k8s/deployment-local.yaml"
Write-Host ""
Write-Host "🛑 To stop:" -ForegroundColor Cyan
Write-Host "   kubectl delete namespace $NAMESPACE"
Write-Host "   kind delete cluster --name kind"
Write-Host ""
