# =============================================================================
# MetalLB Installation for LoadBalancer Support
# Required for Kind cluster to provide external IPs
# =============================================================================

resource "helm_release" "metallb" {
  count = var.install_metallb ? 1 : 0

  depends_on = [kind_cluster.dev]

  name             = "metallb"
  repository       = "https://metallb.github.io/metallb"
  chart            = "metallb"
  namespace        = "metallb-system"
  create_namespace = true
  version          = "0.13.12"

  wait = true

  set {
    name  = "speaker.frr.enabled"
    value = "false"
  }
}

# Wait for MetalLB to be ready before configuring IP pool
resource "null_resource" "wait_for_metallb" {
  count = var.install_metallb ? 1 : 0

  depends_on = [helm_release.metallb]

  provisioner "local-exec" {
    command     = "Start-Sleep -Seconds 30"
    interpreter = ["PowerShell", "-Command"]
  }
}

# MetalLB IP Address Pool Configuration
resource "kubernetes_manifest" "metallb_ip_pool" {
  count = var.install_metallb ? 1 : 0

  depends_on = [null_resource.wait_for_metallb]

  manifest = {
    apiVersion = "metallb.io/v1beta1"
    kind       = "IPAddressPool"
    metadata = {
      name      = "kind-pool"
      namespace = "metallb-system"
    }
    spec = {
      addresses = [
        var.metallb_ip_range != "" ? var.metallb_ip_range : "172.18.255.200-172.18.255.250"
      ]
    }
  }
}

# MetalLB L2 Advertisement
resource "kubernetes_manifest" "metallb_l2_advertisement" {
  count = var.install_metallb ? 1 : 0

  depends_on = [kubernetes_manifest.metallb_ip_pool]

  manifest = {
    apiVersion = "metallb.io/v1beta1"
    kind       = "L2Advertisement"
    metadata = {
      name      = "kind-l2"
      namespace = "metallb-system"
    }
    spec = {
      ipAddressPools = ["kind-pool"]
    }
  }
}
