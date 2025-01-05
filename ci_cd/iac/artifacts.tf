# S3 for artifacts
resource "aws_s3_bucket" "artifacts" {
  bucket = "${var.target_project_name}-artifacts"

  tags = local.common_tags
}

resource "aws_s3_bucket_versioning" "artifacts_bucket_versioning" {
  bucket = aws_s3_bucket.artifacts.id

  versioning_configuration {
    status = "Enabled"
  }

}

# S3 for infra-tfstate
resource "aws_s3_bucket" "infra_tfstate" {
  bucket = "${var.target_project_name}-infra-resources-tfstate"

  tags = local.common_tags
}

resource "aws_s3_bucket_versioning" "infra_tfstate_bucket_versioning" {
  bucket = aws_s3_bucket.infra_tfstate.id

  versioning_configuration {
    status = "Enabled"
  }

}

# ECR
resource "aws_ecr_repository" "backend" {
  name = "${var.target_project_name}-backend"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = local.common_tags
}
