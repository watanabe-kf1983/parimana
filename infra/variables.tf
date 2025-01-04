variable "env" {
  description = "Enviroment name"
  type        = string
  default     = "dev"
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-northeast-1"
}

variable "project_name" {
  description = "The CI/CD project name (e.g., myproject-cicd)"
  type        = string
}
