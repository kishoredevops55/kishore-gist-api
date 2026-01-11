# =============================================================================
# Default values for local development (Windows)
# Matches existing cd-local.yml configuration
# =============================================================================

cluster_name       = "kind-tf"
kubernetes_version = "v1.28.0"

# Port mappings (Avoid conflicts with existing kind-dev or kind-proxy)
api_server_port = 6444
http_port       = 8090
https_port      = 8443

# Cluster topology (1 Control Plane + 2 Workers = 3 Nodes)
worker_nodes = 2

# Service mesh
install_istio = true
istio_version = "1.20.0"

# LoadBalancer support
install_metallb  = true
metallb_ip_range = "172.18.255.200-172.18.255.250"

# Namespaces
namespace            = "production"
monitoring_namespace = "monitoring"

# DNS configuration
custom_dns  = "gists.kishore.local"
grafana_dns = "kishoregrafana.local"
