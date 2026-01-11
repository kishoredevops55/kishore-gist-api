# =============================================================================
# GitHub Gists API - Terraform Configuration for Kind Cluster
# Local Kubernetes Development Environment on Windows
# =============================================================================

terraform {
  required_version = ">= 1.0.0"

  required_providers {
    kind = {
      source  = "tehcyx/kind"
      version = "~> 0.2.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.23.0"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.11.0"
    }
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2.0"
    }
  }

  # Optional: Use local backend for state
  backend "local" {
    path = "terraform.tfstate"
  }
}

# =============================================================================
# Providers Configuration
# =============================================================================

provider "kind" {}

provider "kubernetes" {
  host                   = kind_cluster.dev.endpoint
  client_certificate     = kind_cluster.dev.client_certificate
  client_key             = kind_cluster.dev.client_key
  cluster_ca_certificate = kind_cluster.dev.cluster_ca_certificate
}

provider "helm" {
  kubernetes {
    host                   = kind_cluster.dev.endpoint
    client_certificate     = kind_cluster.dev.client_certificate
    client_key             = kind_cluster.dev.client_key
    cluster_ca_certificate = kind_cluster.dev.cluster_ca_certificate
  }
}
