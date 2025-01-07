resource "aws_s3_bucket" "app" {
  bucket        = "${var.project_name}-${var.env}-app"
  force_destroy = true

  tags = merge(var.common_tags, { Name = "${var.project_name}-${var.env}-app" })
}
