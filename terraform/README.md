# Terraform - Kind Cluster Provisioning

This Terraform configuration provisions a local Kind (Kubernetes in Docker) cluster for the GitHub Gists API project on Windows.

## Prerequisites

1. **Docker Desktop** - Running on Windows
2. **Terraform** - v1.0.0 or higher
3. **kubectl** - For cluster interaction
4. **Helm** - v3.x for chart deployments

## Quick Start

```powershell
# Initialize Terraform
cd terraform
terraform init

# Preview changes
terraform plan

# Create the cluster
terraform apply -auto-approve
```

## What Gets Created

| Resource | Description |
|----------|-------------|
| Kind Cluster | `kind-dev` with 1 control-plane + 2 workers |
| MetalLB | LoadBalancer support for Kind |
| Istio | Service mesh with ingress gateway |
| Namespaces | `production`, `monitoring`, `istio-system` |

## Configuration

Edit `terraform.tfvars` to customize:

```hcl
cluster_name       = "kind-dev"
kubernetes_version = "v1.28.0"
worker_nodes       = 2
install_istio      = true
install_metallb    = true
custom_dns         = "gists.kishore.local"
grafana_dns        = "kishoregrafana.local"
```

## After Cluster Creation

1. **Set kubectl context:**
   ```powershell
   kubectl config use-context kind-kind-dev
   ```

2. **Build and load image:**
   ```powershell
   docker build -t github-gists-api:latest .
   kind load docker-image github-gists-api:latest --name kind-dev
   ```

3. **Deploy with Helm:**
   ```powershell
   helm upgrade --install gists-api ./helm -n production --create-namespace
   ```

4. **Or deploy with raw manifests:**
   ```powershell
   kubectl apply -f k8s/deployment.yaml
   kubectl apply -f k8s/istio-gateway.yaml
   ```

## Destroy Cluster

```powershell
terraform destroy -auto-approve
```

## Troubleshooting

### Check cluster status
```powershell
kind get clusters
kubectl cluster-info --context kind-kind-dev
```

### View Terraform state
```powershell
terraform state list
terraform show
```

### Reset cluster
```powershell
terraform destroy -auto-approve
terraform apply -auto-approve
```
