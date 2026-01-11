# =============================================================================
# Istio Service Mesh Installation
# =============================================================================

resource "helm_release" "istio_base" {
  count = var.install_istio ? 1 : 0

  depends_on = [kubernetes_namespace.istio_system]

  name       = "istio-base"
  repository = "https://istio-release.storage.googleapis.com/charts"
  chart      = "base"
  namespace  = "istio-system"
  version    = var.istio_version

  wait = true
}

resource "helm_release" "istiod" {
  count = var.install_istio ? 1 : 0

  depends_on = [helm_release.istio_base]

  name       = "istiod"
  repository = "https://istio-release.storage.googleapis.com/charts"
  chart      = "istiod"
  namespace  = "istio-system"
  version    = var.istio_version

  wait = true

  set {
    name  = "global.proxy.accessLogFile"
    value = "/dev/stdout"
  }

  set {
    name  = "meshConfig.enableTracing"
    value = "true"
  }

  set {
    name  = "meshConfig.defaultConfig.tracing.zipkin.address"
    value = "tempo.monitoring.svc.cluster.local:9411"
  }

  set {
    name  = "pilot.traceSampling"
    value = "100"
  }
}

resource "helm_release" "istio_ingress" {
  count = var.install_istio ? 1 : 0

  depends_on = [helm_release.istiod]

  name       = "istio-ingress"
  repository = "https://istio-release.storage.googleapis.com/charts"
  chart      = "gateway"
  namespace  = "istio-system"
  version    = var.istio_version

  wait = true

  set {
    name  = "service.type"
    value = "LoadBalancer"
  }
}

# Wait for Istio to be fully ready
resource "null_resource" "wait_for_istio" {
  count = var.install_istio ? 1 : 0

  depends_on = [helm_release.istio_ingress]

  provisioner "local-exec" {
    command     = "kubectl wait --for=condition=ready pod -l app=istiod -n istio-system --timeout=120s"
    interpreter = ["PowerShell", "-Command"]
  }
}
