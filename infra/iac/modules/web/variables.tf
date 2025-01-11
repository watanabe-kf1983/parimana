variable "project_name" {
  description = "The CI/CD project name (e.g., myproject-cicd)"
  type        = string
}

variable "env" {
  description = "Enviroment name"
  type        = string
  default     = "dev"
}

variable "web_api_lambda_arn" {
  description = "Web api lambda invoke arn"
  type        = string
}

variable "web_api_lambda_name" {
  description = "Web api lambda function name"
  type        = string
}

variable "common_tags" {
  description = "Common tags to apply to all resources"
  type        = map(string)
}
