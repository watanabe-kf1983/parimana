provider "aws" {
  region = var.aws_region
}

terraform {
  backend "s3" {
    bucket  = "xxxxxxxxxxxxxxxxx"
    key     = "terraform.tfstate"
    region  = "xxxxxxxxxxxxxxxxx"
    encrypt = true
  }
}

locals {
  common_tags = {
    Environment = "ci-cd"
    Project     = var.project_name
    ManagedBy   = "Terraform"
  }
}
