# =============================================================================
# Variables for Kind Cluster Configuration
# Matching existing cd-local.yml settings
# =============================================================================

variable "cluster_name" {
  description = "Name of the Kind cluster"
  type        = string
  default     = "kind-dev"
}

variable "kubernetes_version" {
  description = "Kubernetes version for the Kind cluster"
  type        = string
  default     = "v1.28.0"
}

variable "api_server_port" {
  description = "Port for Kubernetes API server"
  type        = number
  default     = 6443
}

variable "http_port" {
  description = "Host port mapping for HTTP (80)"
  type        = number
  default     = 80
}

variable "https_port" {
  description = "Host port mapping for HTTPS (443)"
  type        = number
  default     = 443
}

variable "worker_nodes" {
  description = "Number of worker nodes"
  type        = number
  default     = 2
}

variable "install_istio" {
  description = "Whether to install Istio service mesh"
  type        = bool
  default     = true
}

variable "istio_version" {
  description = "Istio version to install"
  type        = string
  default     = "1.20.0"
}

variable "install_metallb" {
  description = "Whether to install MetalLB for LoadBalancer support"
  type        = bool
  default     = true
}

variable "metallb_ip_range" {
  description = "IP range for MetalLB (auto-detected from Docker network if empty)"
  type        = string
  default     = ""
}

variable "namespace" {
  description = "Namespace for application deployment"
  type        = string
  default     = "production"
}

variable "monitoring_namespace" {
  description = "Namespace for monitoring stack"
  type        = string
  default     = "monitoring"
}

variable "custom_dns" {
  description = "Custom DNS for the application"
  type        = string
  default     = "gists.kishore.local"
}

variable "grafana_dns" {
  description = "Custom DNS for Grafana"
  type        = string
  default     = "kishoregrafana.local"
}
