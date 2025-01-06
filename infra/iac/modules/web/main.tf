resource "aws_s3_bucket" "web" {
  bucket        = "${var.project_name}-${var.env}-web"
  force_destroy = true

  tags = var.common_tags
}
