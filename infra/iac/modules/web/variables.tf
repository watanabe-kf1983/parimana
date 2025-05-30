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


variable "web_api_lambda_arn" {
  description = "Web api lambda invoke arn"
  type        = string
}

variable "web_api_lambda_name" {
  description = "Web api lambda function name"
  type        = string
}

variable "domain_name" {
  description = "Domain name"
  type        = string
}

variable "sub_domain_name" {
  description = "Sub domain name"
  type        = string
}

variable "common_tags" {
  description = "Common tags to apply to all resources"
  type        = map(string)
}
