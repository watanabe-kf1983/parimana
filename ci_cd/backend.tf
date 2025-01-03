terraform {
  backend "s3" {
    bucket         = "myproject-cicd-resources-tfstate"  # S3バケット名
    key            = "terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
  }
}
