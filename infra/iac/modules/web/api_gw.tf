resource "aws_api_gateway_rest_api" "web_api" {
  name        = "${var.project_name}-${var.env}-api"
  description = "API Gateway for Web API in ${var.env} environment"

  tags = merge(var.common_tags, { Name = "${var.project_name}-${var.env}-api" })
}

resource "aws_api_gateway_resource" "proxy" {
  rest_api_id = aws_api_gateway_rest_api.web_api.id
  parent_id   = aws_api_gateway_rest_api.web_api.root_resource_id
  path_part   = "{proxy+}"
}

resource "aws_api_gateway_method" "proxy_method" {
  rest_api_id   = aws_api_gateway_rest_api.web_api.id
  resource_id   = aws_api_gateway_resource.proxy.id
  http_method   = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda_integration" {
  rest_api_id             = aws_api_gateway_rest_api.web_api.id
  resource_id             = aws_api_gateway_resource.proxy.id
  http_method             = aws_api_gateway_method.proxy_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = var.web_api_lambda_arn
}

resource "aws_api_gateway_deployment" "web_api_deployment" {
  rest_api_id = aws_api_gateway_rest_api.web_api.id

  lifecycle {
    create_before_destroy = true
  }

  depends_on = [aws_api_gateway_integration.lambda_integration]
}

resource "aws_api_gateway_stage" "web_api_stage" {
  rest_api_id  = aws_api_gateway_rest_api.web_api.id
  deployment_id = aws_api_gateway_deployment.web_api_deployment.id
  stage_name   = var.env

  tags = merge(var.common_tags, { Name = "${var.project_name}-${var.env}-api-stage" })
}

resource "aws_lambda_permission" "allow_api_gateway" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = var.web_api_lambda_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.web_api.execution_arn}/*"
}

resource "aws_api_gateway_rest_api_policy" "web_api_policy" {
  rest_api_id = aws_api_gateway_rest_api.web_api.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = "*",
        Action = "execute-api:Invoke",
        Resource = "*",
        Condition = {
          StringEquals = {
            "aws:SourceArn" = "${aws_cloudfront_distribution.web_distribution.arn}"
          }
        }
      }
    ]
  })
}