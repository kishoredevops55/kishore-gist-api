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
  config_path    = pathexpand("~/.kube/config")
  config_context = "kind-${var.cluster_name}"
}

provider "helm" {
  kubernetes {
    config_path    = pathexpand("~/.kube/config")
    config_context = "kind-${var.cluster_name}"
  }
}
