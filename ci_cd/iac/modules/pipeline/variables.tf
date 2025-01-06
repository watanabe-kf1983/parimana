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

variable "env" {
  description = "The target env name"
  type        = string
}

variable "source_repository" {
  description = "Source repository for CodePipeline"
  type = object({
    connection_arn     = string
    full_repository_id = string
    branch_name        = string
  })
}

variable "s3_artifact_store" {
  description = "S3 bucket for artifact store"
  type = string
}

variable "s3_tfstate_store" {
  description = "S3 bucket for tfstate store"
  type = string
}

variable "common_tags" {
  description = "Common tags to apply to all resources"
  type        = map(string)
}
