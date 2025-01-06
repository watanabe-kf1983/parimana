terraform {
  required_version = "1.10.3"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.82.2"
    }
  }
  backend "s3" {
    key     = "dev/terraform.tfstate"
    encrypt = true
  }
}

provider "aws" {
  region = var.aws_region
}


module "net" {
  source              = "../../modules/net"
  project_name        = var.project_name
  env                 = var.env
  public_az           = "${var.aws_region}a"
  private_az          = "${var.aws_region}a"
  common_tags         = local.common_tags
}


module "app" {
  source       = "../../modules/app"
  project_name = var.project_name
  env          = var.env
  common_tags  = local.common_tags
}

module "web" {
  source       = "../../modules/web"
  project_name = var.project_name
  env          = var.env
  common_tags  = local.common_tags
}


locals {
  common_tags = {
    Environment = var.env
    Project     = var.project_name
    ManagedBy   = "Terraform"
  }
}
