variable "project_name" {
  description = "The CI/CD project name (e.g., myproject-cicd)"
  type        = string
}

variable "env" {
  description = "Enviroment name"
  type        = string
  default     = "dev"
}

variable "aws_region" {
  description = "AWS region"
  type        = string
}

variable "aws_account_id" {
  description = "AWS Account id"
  type        = string
}

variable "vpc_id" {
  description = "Vpc id"
  type        = string
}

variable "private_subnet_ids" {
  description = "List of private subnet IDs"
  type        = list(string)
}

variable "private_subnet_cidrs" {
  description = "List of private subnet CIDRs"
  type        = list(string)
}

variable "common_tags" {
  description = "Common tags to apply to all resources"
  type        = map(string)
}
