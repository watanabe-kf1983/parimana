resource "aws_cloudfront_distribution" "web_distribution" {
  enabled = true

  origin {
    domain_name = aws_s3_bucket.web.bucket_regional_domain_name
    origin_id   = "S3-${aws_s3_bucket.web.id}"

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.oai.cloudfront_access_identity_path
    }
  }

  origin {
    domain_name = "${aws_api_gateway_rest_api.web_api.id}.execute-api.${var.aws_region}.amazonaws.com"
    origin_id   = "APIGatewayOrigin-${var.env}"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_ssl_protocols   = ["TLSv1", "TLSv1.1", "TLSv1.2"]
      origin_protocol_policy = "https-only" # API Gatewayへの通信はHTTPS
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

  ordered_cache_behavior {
    path_pattern           = "/${var.env}/api/*"
    target_origin_id       = "APIGatewayOrigin-${var.env}"
    viewer_protocol_policy = "https-only"

    allowed_methods = ["HEAD", "DELETE", "POST", "GET", "OPTIONS", "PUT", "PATCH"]
    cached_methods  = ["GET", "HEAD"]

    forwarded_values {
      query_string = true
      headers      = ["Authorization"]
      cookies {
        forward = "all"
      }
    }

    min_ttl     = 0
    default_ttl = 0
    max_ttl     = 0
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

  # aliases = [var.sub_domain_name]

  viewer_certificate {
    acm_certificate_arn      = aws_acm_certificate.cert.arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2019"
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  logging_config {
    bucket = aws_s3_bucket.logs_web.bucket_regional_domain_name
    prefix = "cloudfront-logs/"
  }

  tags = var.common_tags
}


resource "aws_cloudfront_origin_access_identity" "oai" {
  comment = "OAI for accessing S3 bucket"
}


resource "aws_s3_bucket" "logs_web" {
  bucket        = "${var.project_name}-${var.env}-logs-web"
  force_destroy = true

  tags = var.common_tags
}

resource "aws_s3_bucket_ownership_controls" "logs_web" {
  bucket = aws_s3_bucket.logs_web.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "logs_web" {
  depends_on = [aws_s3_bucket_ownership_controls.logs_web]

  bucket = aws_s3_bucket.logs_web.id
  access_control_policy {
    grant {
      grantee {
        id   = "c4c1ede66af53448b93c283ce9448c4ba468c9432aa01d700d3878632f77d2d0"
        type = "CanonicalUser"
      }
      permission = "FULL_CONTROL"
    }

    owner {
      id = data.aws_canonical_user_id.current.id
    }
  }
}

data "aws_canonical_user_id" "current" {}