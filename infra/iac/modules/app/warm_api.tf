resource "aws_cloudwatch_event_rule" "warm_up_lambda_rule" {
  name                = "${var.project_name}-${var.env}-warm-web-api"
  schedule_expression = "cron(*/10 * * * ? *)" # every 10 minutes
  tags                = var.common_tags
}


resource "aws_cloudwatch_event_target" "warm_up_target_lambda" {
  count = 5
  rule = aws_cloudwatch_event_rule.warm_up_lambda_rule.name
  arn  = aws_lambda_function.web_api.arn
  input = jsonencode({
    "version" : "2.0",
    "requestContext" : {
      "http" : {
        "method" : "GET",
        "path" : "/api/v1/info",
        "sourceIp" : "111.111.111.111"
      }
    }
  })
}

resource "aws_lambda_permission" "allow_eventbridge_warm_up_web_api" {
  statement_id  = "AllowEventBridge-${var.env}-warm-up-web-api"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.web_api.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.warm_up_lambda_rule.arn
}
