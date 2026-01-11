# =============================================================================
# Outputs
# =============================================================================

output "cluster_name" {
  description = "Name of the Kind cluster"
  value       = kind_cluster.dev.name
}

output "kubeconfig_path" {
  description = "Path to kubeconfig file"
  value       = kind_cluster.dev.kubeconfig_path
}

output "cluster_endpoint" {
  description = "Kubernetes API server endpoint"
  value       = kind_cluster.dev.endpoint
}

output "kubectl_context" {
  description = "kubectl context name"
  value       = "kind-${var.cluster_name}"
}

output "production_namespace" {
  description = "Production namespace"
  value       = kubernetes_namespace.production.metadata[0].name
}

output "monitoring_namespace" {
  description = "Monitoring namespace"
  value       = kubernetes_namespace.monitoring.metadata[0].name
}

output "istio_installed" {
  description = "Whether Istio was installed"
  value       = var.install_istio
}

output "metallb_installed" {
  description = "Whether MetalLB was installed"
  value       = var.install_metallb
}

output "access_urls" {
  description = "Application access URLs"
  value = {
    api_health = "https://${var.custom_dns}/health"
    api_gists  = "https://${var.custom_dns}/{username}"
    grafana    = "https://${var.grafana_dns}"
  }
}

output "hosts_file_entries" {
  description = "Required hosts file entries"
  value       = <<-EOT
    Add these entries to C:\Windows\System32\drivers\etc\hosts:
    127.0.0.1    ${var.custom_dns}
    127.0.0.1    gists.local
    127.0.0.1    ${var.grafana_dns}
    127.0.0.1    rum.kishore.local
  EOT
}

output "next_steps" {
  description = "Next steps after cluster creation"
  value       = <<-EOT
    
    ============================================================
    KIND CLUSTER CREATED SUCCESSFULLY!
    ============================================================
    
    Next Steps:
    
    1. Set kubectl context:
       kubectl config use-context kind-${var.cluster_name}
    
    2. Build and load your application image:
       docker build -t github-gists-api:latest .
       kind load docker-image github-gists-api:latest --name ${var.cluster_name}
    
    3. Deploy using Helm:
       helm upgrade --install gists-api ./helm -n production
    
    4. Or deploy using raw manifests:
       kubectl apply -f k8s/deployment.yaml
       kubectl apply -f k8s/istio-gateway.yaml
    
    5. Deploy monitoring stack:
       kubectl apply -f monitoring/
    
    ============================================================
  EOT
}
