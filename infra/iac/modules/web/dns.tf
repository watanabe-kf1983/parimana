data "aws_route53_zone" "main" {
  name = var.domain_name
}

resource "aws_route53_record" "cloudfront_alias" {
  zone_id = data.aws_route53_zone.main.zone_id
  name    = var.sub_domain_name
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.web_distribution.domain_name
    zone_id                = aws_cloudfront_distribution.web_distribution.hosted_zone_id
    evaluate_target_health = false
  }
}


resource "aws_acm_certificate" "cert" {
  # CloudFront用ACM証明書は us_east_1で作る必要あり
  provider                  = aws.us_east_1
  domain_name               = var.domain_name
  subject_alternative_names = [var.sub_domain_name]
  validation_method         = "DNS"

  tags = merge(var.common_tags, { Name = "${var.project_name}-${var.env}-certificate" })
}

resource "aws_route53_record" "acm_validation" {
  for_each = { for dvo in aws_acm_certificate.cert.domain_validation_options : dvo.domain_name => dvo }
  zone_id  = data.aws_route53_zone.main.zone_id
  name     = each.value.resource_record_name
  type     = each.value.resource_record_type
  records  = [each.value.resource_record_value]
  ttl      = 60
}
