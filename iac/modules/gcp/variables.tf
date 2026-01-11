variable "cluster_name" {
  description = "Name of the GKE cluster"
  type        = string
}

variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

variable "node_machine_type" {
  description = "Machine type for worker nodes"
  type        = string
  default     = "e2-medium"
}

variable "initial_node_count" {
  description = "Initial number of worker nodes per zone"
  type        = number
  default     = 1
}

variable "min_node_count" {
  description = "Minimum number of nodes in the cluster"
  type        = number
  default     = 1
}

variable "max_node_count" {
  description = "Maximum number of nodes in the cluster"
  type        = number
  default     = 5
}
