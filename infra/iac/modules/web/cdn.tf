resource "aws_cloudfront_distribution" "web_distribution" {
  enabled = true

  origin {
    domain_name = aws_s3_bucket.web.bucket_regional_domain_name
    origin_id   = "S3-${aws_s3_bucket.web.id}"

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.oai.cloudfront_access_identity_path
    }
  }

  default_cache_behavior {
    target_origin_id       = "S3-${aws_s3_bucket.web.id}"
    viewer_protocol_policy = "redirect-to-https"

    allowed_methods = ["GET", "HEAD"]
    cached_methods  = ["GET", "HEAD"]

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }
  }

  custom_error_response {
    error_code            = 403
    response_page_path    = "/"
    response_code         = 200
    error_caching_min_ttl = 0 
  }

  custom_error_response {
    error_code            = 404
    response_page_path    = "/"
    response_code         = 200
    error_caching_min_ttl = 0 
  }

  default_root_object = "index.html"


  viewer_certificate {
    cloudfront_default_certificate = true # デフォルトのCloudFront SSL証明書を使用
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  tags = var.common_tags
}


resource "aws_cloudfront_origin_access_identity" "oai" {
  comment = "OAI for accessing S3 bucket"
}

