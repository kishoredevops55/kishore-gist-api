# Kubernetes Networking Migration Guide

## Gateway API (Recommended)

As of December 2025, the Kubernetes community has officially announced the retirement of the Ingress NGINX controller, with end-of-life (EOL) scheduled for **March 26, 2026**. The recommended migration path is to adopt the **Gateway API**.

### Why Gateway API?

1. **Modern Standard**: Gateway API is the official successor to Ingress, designed with lessons learned from years of Ingress limitations
2. **Role-Oriented**: Separates infrastructure (Gateway) from application routing (HTTPRoute), enabling team autonomy
3. **Rich Features**: Native support for traffic splitting, header routing, weighted backends, timeouts - no more "annotation hell"
4. **Active Ecosystem**: Backed by AWS, GCP, Azure, NGINX, Envoy, Istio, and other major vendors
5. **Security**: Active maintenance and security patching, unlike EOL Ingress NGINX

### Migration Options

#### Option 1: Gateway API (Primary Recommendation)
```bash
kubectl apply -f k8s/gateway-api.yaml
```

Features:
- HTTP to HTTPS redirect
- TLS termination with cert-manager
- Request timeouts
- Clean, annotation-free configuration

#### Option 2: Istio Service Mesh
```bash
kubectl apply -f k8s/ingress-istio.yaml
```

Features:
- Advanced traffic management (retries, circuit breaking)
- mTLS between services
- Observability (distributed tracing)
- Connection pooling and load balancing

#### Option 3: Legacy Ingress (Deprecated)
```bash
# Only for existing deployments - DO NOT use for new projects
kubectl apply -f k8s/ingress-nginx.yaml
```

**Warning**: Ingress NGINX will receive no security patches after March 2026. This option is provided only for legacy compatibility.

### Installation Requirements

**Gateway API CRDs** (required for Option 1):
```bash
kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.0.0/standard-install.yaml
```

**Gateway Controller** (choose one):
- NGINX Gateway Fabric: `kubectl apply -f https://github.com/nginxinc/nginx-gateway-fabric/releases/latest/download/crds.yaml`
- Envoy Gateway: `helm install eg oci://docker.io/envoyproxy/gateway-helm --version v1.0.0`
- Cloud provider-managed (GKE, EKS, AKS)

**Istio** (required for Option 2):
```bash
istioctl install --set profile=production
```

### Migration Timeline

- **Now - March 2026**: Plan and execute migration to Gateway API
- **March 26, 2026**: Ingress NGINX EOL - no more security patches
- **Post-March 2026**: Running Ingress NGINX poses significant security risk

### Automated Migration Tool

Use `ingress2gateway` to convert existing Ingress resources:
```bash
ingress2gateway print --input-file=k8s/ingress-nginx.yaml
```

### References

- [Gateway API Documentation](https://gateway-api.sigs.k8s.io/)
- [Ingress NGINX Retirement Announcement](https://kubernetes.io/blog/2024/11/25/nginx-ingress-retirement/)
- [Migration Guide](https://gateway-api.sigs.k8s.io/guides/migrating-from-ingress/)
