# =============================================================================
# Kind Cluster Resource
# Matches existing kind-dev cluster configuration
# =============================================================================

resource "kind_cluster" "dev" {
  name           = var.cluster_name
  wait_for_ready = true

  kind_config {
    kind        = "Cluster"
    api_version = "kind.x-k8s.io/v1alpha4"

    # Control plane node
    node {
      role  = "control-plane"
      image = "kindest/node:${var.kubernetes_version}"

      kubeadm_config_patches = [
        <<-PATCH
        kind: InitConfiguration
        nodeRegistration:
          kubeletExtraArgs:
            node-labels: "ingress-ready=true"
        PATCH
      ]

      # Port mappings for ingress
      extra_port_mappings {
        container_port = 80
        host_port      = var.http_port
        protocol       = "TCP"
      }

      extra_port_mappings {
        container_port = 443
        host_port      = var.https_port
        protocol       = "TCP"
      }

      extra_port_mappings {
        container_port = 31080
        host_port      = 31080
        protocol       = "TCP"
      }

      extra_port_mappings {
        container_port = 31443
        host_port      = 31443
        protocol       = "TCP"
      }
    }

    # Worker nodes
    dynamic "node" {
      for_each = range(var.worker_nodes)
      content {
        role  = "worker"
        image = "kindest/node:${var.kubernetes_version}"
      }
    }

    # Networking configuration
    networking {
      api_server_port     = var.api_server_port
      disable_default_cni = false
      pod_subnet          = "10.244.0.0/16"
      service_subnet      = "10.96.0.0/12"
    }
  }
}

# =============================================================================
# Namespaces
# =============================================================================

resource "kubernetes_namespace" "production" {
  depends_on = [kind_cluster.dev]

  metadata {
    name = var.namespace
    labels = {
      "istio-injection" = "enabled"
    }
  }
}

resource "kubernetes_namespace" "monitoring" {
  depends_on = [kind_cluster.dev]

  metadata {
    name = var.monitoring_namespace
    labels = {
      "istio-injection" = "enabled"
    }
  }
}

resource "kubernetes_namespace" "istio_system" {
  depends_on = [kind_cluster.dev]

  metadata {
    name = "istio-system"
  }
}
