variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-northeast-1"
}

variable "cicd_project_name" {
  description = "The CI/CD project name (e.g., myproject-cicd)"
  type        = string
}

variable "target_project_name" {
  description = "The target project name for backend/frontend resources"
  type        = string
}

variable "source_repository_connection_arn" {
  description = "Source repository connection arn for CodePipeline"
  type = string
}

variable "source_repository_full_repository_id" {
  description = "Source repository full repository id for CodePipeline"
  type = string
}
