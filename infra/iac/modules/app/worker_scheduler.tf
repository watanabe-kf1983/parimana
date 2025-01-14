resource "aws_cloudwatch_event_rule" "scale_up_rule" {
  name                = "${var.project_name}-${var.env}-scale-up-worker"
  schedule_expression = "cron(20 23 * * ? *)" # every 08:20(+09:00)

  tags = var.common_tags
}

resource "aws_cloudwatch_event_rule" "scale_down_rule" {
  name                = "${var.project_name}-${var.env}-scale-down-worker"
  schedule_expression = "cron(50 14 * * ? *)" # every 23:50(+09:00)

  tags = var.common_tags
}

resource "aws_cloudwatch_event_rule" "restart_rule" {
  name                = "${var.project_name}-${var.env}-restart-worker"
  schedule_expression = "cron(0 01-14/3 * * ? *)" # 10, 13, 16, 19, 22 (+09)

  tags = var.common_tags
}

resource "aws_cloudwatch_event_target" "scale_up_target" {
  rule  = aws_cloudwatch_event_rule.scale_up_rule.name
  arn   = aws_lambda_function.ecs_task_scaler.arn
  input = jsonencode({ "desired_task_count" : "1" })
}

resource "aws_cloudwatch_event_target" "scale_down_target" {
  rule  = aws_cloudwatch_event_rule.scale_down_rule.name
  arn   = aws_lambda_function.ecs_task_scaler.arn
  input = jsonencode({ "desired_task_count" : "0" })
}

resource "aws_cloudwatch_event_target" "restart_target" {
  rule  = aws_cloudwatch_event_rule.restart_rule.name
  arn   = aws_lambda_function.ecs_task_stopper.arn
}

resource "aws_lambda_permission" "allow_eventbridge_scale_up" {
  statement_id  = "AllowEventBridge-${var.env}-scale-up"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ecs_task_scaler.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.scale_up_rule.arn
}

resource "aws_lambda_permission" "allow_eventbridge_scale_down" {
  statement_id  = "AllowEventBridge-${var.env}-scale-down"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ecs_task_scaler.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.scale_down_rule.arn
}

resource "aws_lambda_permission" "allow_eventbridge_restart" {
  statement_id  = "AllowEventBridge-${var.env}-restart"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ecs_task_stopper.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.restart_rule.arn
}

