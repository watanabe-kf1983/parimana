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
  depends_on    = [aws_api_gateway_account.api_gateway_account]
  rest_api_id   = aws_api_gateway_rest_api.web_api.id
  deployment_id = aws_api_gateway_deployment.web_api_deployment.id
  stage_name    = var.env

  tags = merge(var.common_tags, { Name = "${var.project_name}-${var.env}-api-stage" })

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gateway_logs.arn
    format = jsonencode({
      requestId        = "$context.requestId",
      ip               = "$context.identity.sourceIp",
      caller           = "$context.identity.caller",
      user             = "$context.identity.user",
      requestTime      = "$context.requestTime",
      httpMethod       = "$context.httpMethod",
      resourcePath     = "$context.resourcePath",
      status           = "$context.status",
      protocol         = "$context.protocol",
      responseLength   = "$context.responseLength"
      errorMessage     = "$context.error.message",
      integrationError = "$context.integration.error"
    })
  }

  variables = {
    logging_level   = "INFO"
    metrics_enabled = "true"
  }
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
        Effect    = "Allow",
        Principal = "*",
        Action    = "execute-api:Invoke",
        Resource  = "*",
      }
    ]
  })
}

resource "aws_cloudwatch_log_group" "api_gateway_logs" {
  name              = "/aws/api-gateway/${var.project_name}-${var.env}"
  retention_in_days = 7
  tags              = merge(var.common_tags, { Name = "API Gateway Logs" })
}

resource "aws_iam_role" "api_gateway_logging_role" {
  name = "${var.project_name}-${var.env}-api-gateway-logging-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "apigateway.amazonaws.com"
        }
      }
    ]
  })

  tags = merge(var.common_tags, { Name = "API Gateway Logging Role" })
}

resource "aws_iam_role_policy" "api_gateway_logging_policy" {
  role = aws_iam_role.api_gateway_logging_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        # AmazonAPIGatewayPushToCloudWatchLogs
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:DescribeLogGroups",
          "logs:DescribeLogStreams",
          "logs:PutLogEvents",
          "logs:GetLogEvents",
          "logs:FilterLogEvents"
        ],
        Effect   = "Allow",
        Resource = "*"
      }
    ]
  })
}

resource "aws_api_gateway_account" "api_gateway_account" {
  cloudwatch_role_arn = aws_iam_role.api_gateway_logging_role.arn
}
