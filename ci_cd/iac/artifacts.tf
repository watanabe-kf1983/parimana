# S3 for artifacts
resource "aws_s3_bucket" "artifacts" {
  bucket = "${var.target_project_name}-artifacts"
  force_destroy = true
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
  force_destroy = true

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


resource "aws_ecr_repository" "hello-world" {
  name = "hello-world"
  force_delete = true

  image_scanning_configuration {
    scan_on_push = true
  }
  provisioner "local-exec" {
    command = "./scripts/push_hello.sh ${var.aws_account_id} ${var.aws_region}"
  }
  tags = local.common_tags
}
