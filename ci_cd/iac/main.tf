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


module "prod-pipeline" {
  source              = "./modules/pipeline"
  aws_region          = var.aws_region
  aws_account_id      = var.aws_account_id
  cicd_project_name   = var.cicd_project_name
  target_project_name = var.target_project_name
  env                 = "prod"
  s3_artifact_store   = aws_s3_bucket.artifacts.bucket
  s3_tfstate_store    = aws_s3_bucket.infra_tfstate.bucket
  common_tags         = local.common_tags
  source_repository = {
    connection_arn     = var.source_repository_connection_arn
    full_repository_id = var.source_repository_full_repository_id
    branch_name        = "main"
  }
}

locals {
  common_tags = {
    Environment = "ci-cd"
    Project     = var.cicd_project_name
    ManagedBy   = "Terraform"
  }
}
