terraform {
  required_version = "1.10.3"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.82.2"
    }
  }
  backend "s3" {
    key     = "terraform.tfstate"
    encrypt = true
  }
}

provider "aws" {
  region = var.aws_region
}

locals {
  common_tags = {
    Environment = "ci-cd"
    Project     = var.project_name
    ManagedBy   = "Terraform"
  }
}
