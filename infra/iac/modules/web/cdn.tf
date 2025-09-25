resource "aws_cloudfront_function" "spa_rewrite" {
  name    = "${var.project_name}-${var.env}-spa-rewrite"
  runtime = "cloudfront-js-1.0"
  publish = true
  code    = <<EOF
function handler(event) {
  var req = event.request;
  var uri = req.uri || "/";
  var h   = req.headers || {};
  var m   = req.method || "GET";

  // 非GET/HEAD、/.well-known/*、拡張子ありを素通し
  if (m !== "GET" && m !== "HEAD") return req;
  if (uri.startsWith("/.well-known/")) return req;
  if (/\.[a-zA-Z0-9]+$/.test(uri)) return req;

  // HTMLナビゲーションだけ index.html へ
  var accept = (h.accept && h.accept.value) || "";
  var dest   = (h["sec-fetch-dest"] && h["sec-fetch-dest"].value) || "";
  if (dest === "document" || accept.includes("text/html")) {
    req.uri = "/index.html";
  }
  return req;
}
EOF
}

# SPA (S3) 用 Cache Policy（短TTL・Acceptで分岐）
resource "aws_cloudfront_cache_policy" "spa_cache" {
  name        = "${var.project_name}-${var.env}-spa-cache"
  comment     = "SPA html: short TTL; vary on Accept; no query/cookies"
  default_ttl = 60
  max_ttl     = 300
  min_ttl     = 0
  parameters_in_cache_key_and_forwarded_to_origin {
    enable_accept_encoding_brotli = true
    enable_accept_encoding_gzip   = true
    cookies_config { cookie_behavior = "none" }
    headers_config {
      header_behavior = "whitelist"
      headers { items = ["Accept"] }
    }
    query_strings_config { query_string_behavior = "none" }
  }
}

# SPA (S3) 用 Origin Request Policy（極小転送）
resource "aws_cloudfront_origin_request_policy" "spa_origin_req" {
  name    = "${var.project_name}-${var.env}-spa-origin-req"
  comment = "SPA: minimal forwarding"
  cookies_config { cookie_behavior = "none" }
  headers_config { header_behavior = "none" }
  query_strings_config { query_string_behavior = "none" }
}

data "aws_cloudfront_cache_policy" "managed_caching_disabled" {
  name = "Managed-CachingDisabled"
}

data "aws_cloudfront_origin_request_policy" "managed_all_viewer_except_host" {
  name = "Managed-AllViewerExceptHostHeader"
}


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
    origin_path = "/${var.env}"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_ssl_protocols   = ["TLSv1", "TLSv1.1", "TLSv1.2"]
      origin_protocol_policy = "https-only" # API Gatewayへの通信はHTTPS
    }
  }

  # --- Default (/* → S3 / SPA) ---
  default_cache_behavior {
    target_origin_id       = "S3-${aws_s3_bucket.web.id}"
    viewer_protocol_policy = "redirect-to-https"

    allowed_methods = ["GET", "HEAD"]
    cached_methods  = ["GET", "HEAD"]

    cache_policy_id          = aws_cloudfront_cache_policy.spa_cache.id
    origin_request_policy_id = aws_cloudfront_origin_request_policy.spa_origin_req.id

    # SPA用リクエストリライト
    function_association {
      event_type   = "viewer-request"
      function_arn = aws_cloudfront_function.spa_rewrite.arn
    }
  }

  # --- /api/* (API Gateway) ---
  ordered_cache_behavior {
    path_pattern           = "/api/*"
    target_origin_id       = "APIGatewayOrigin-${var.env}"
    viewer_protocol_policy = "https-only"

    allowed_methods = ["HEAD", "DELETE", "POST", "GET", "OPTIONS", "PUT", "PATCH"]
    cached_methods  = ["GET", "HEAD"]

    cache_policy_id          = data.aws_cloudfront_cache_policy.managed_caching_disabled.id
    origin_request_policy_id = data.aws_cloudfront_origin_request_policy.managed_all_viewer_except_host.id
  }


  default_root_object = "index.html"

  aliases = [var.sub_domain_name]

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
