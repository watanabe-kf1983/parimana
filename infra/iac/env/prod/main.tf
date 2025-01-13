terraform {
  required_version = "1.10.3"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.82.2"
    }
  }
  backend "s3" {
    key     = "prod/terraform.tfstate"
    encrypt = true
  }
}

provider "aws" {
  region = var.aws_region
}

# 証明書発行用プロバイダ
provider "aws" {
  alias  = "us_east_1"
  region = "us-east-1"
}

module "net" {
  source       = "../../modules/net"
  project_name = var.project_name
  env          = var.env
  aws_region   = var.aws_region
  public_az    = "${var.aws_region}a"
  private_az   = "${var.aws_region}a"
  common_tags  = local.common_tags
}

module "app" {
  source               = "../../modules/app"
  project_name         = var.project_name
  env                  = var.env
  aws_account_id       = var.aws_account_id
  aws_region           = var.aws_region
  vpc_id               = module.net.vpc_id
  private_subnet_ids   = module.net.private_subnet_ids
  private_subnet_cidrs = module.net.private_subnet_cidrs
  common_tags          = local.common_tags
}

module "web" {
  source              = "../../modules/web"
  project_name        = var.project_name
  env                 = var.env
  aws_region          = var.aws_region
  domain_name         = var.domain_name
  sub_domain_name     = var.sub_domain_name
  web_api_lambda_arn  = module.app.web_api_lambda_arn
  web_api_lambda_name = module.app.web_api_lambda_name
  common_tags         = local.common_tags

  providers = {
    aws           = aws
    aws.us_east_1 = aws.us_east_1
  }
}

locals {
  common_tags = {
    Environment = var.env
    Project     = var.project_name
    ManagedBy   = "Terraform"
  }
}
