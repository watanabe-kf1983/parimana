resource "aws_s3_bucket" "web" {
  bucket        = "${var.project_name}-${var.env}-web"
  force_destroy = true

  tags = var.common_tags
}


resource "aws_s3_bucket_policy" "web_policy" {
  bucket = aws_s3_bucket.web.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = "*"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ]
        Resource = [
          "${aws_s3_bucket.web.arn}/*", # バケット内のオブジェクト
          "${aws_s3_bucket.web.arn}"    # バケット自体
        ]
      }
    ]
  })
}
