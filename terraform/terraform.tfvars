# =============================================================================
# Default values for local development (Windows)
# Matches existing cd-local.yml configuration
# =============================================================================

cluster_name       = "kind-dev"
kubernetes_version = "v1.28.0"

# Port mappings
api_server_port = 6443
http_port       = 80
https_port      = 443

# Cluster topology
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
