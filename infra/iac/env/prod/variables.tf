variable "project_name" {
  description = "The CI/CD project name (e.g., myproject-cicd)"
  type        = string
}

variable "env" {
  description = "Enviroment name"
  type        = string
  default     = "dev"
}

variable "aws_account_id" {
  description = "AWS Account id"
  type        = string
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-northeast-1"
}

variable "domain_name" {
  description = "Domain name"
  type        = string
}

variable "sub_domain_name" {
  description = "Sub domain name"
  type        = string
}
