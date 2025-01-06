variable "project_name" {
  description = "The CI/CD project name (e.g., myproject-cicd)"
  type        = string
}

variable "env" {
  description = "Enviroment name"
  type        = string
  default     = "dev"
}

variable "common_tags" {
  description = "Common tags to apply to all resources"
  type        = map(string)
}
