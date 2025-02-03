resource "aws_cloudwatch_event_rule" "start_up_weekday_rule" {
  name                = "${var.project_name}-${var.env}-start-up-worker-weekday"
  schedule_expression = "cron(00 22 ? * SUN-THU *)" # every MON-FRI 07:00(+09:00)
  tags                = var.common_tags
}

resource "aws_cloudwatch_event_rule" "start_up_weekend_rule" {
  name                = "${var.project_name}-${var.env}-start-up-worker-weekend"
  schedule_expression = "cron(00 22 ? * FRI,SAT *)" # every SAT,SUN 07:00(+09:00)
  tags                = var.common_tags
}

resource "aws_cloudwatch_event_rule" "shut_down_rule" {
  name                = "${var.project_name}-${var.env}-shut-down-worker"
  schedule_expression = "cron(00 15 * * ? *)" # every 24:00(+09:00)
  tags                = var.common_tags
}

resource "aws_cloudwatch_event_rule" "restart_rule" {
  name                = "${var.project_name}-${var.env}-restart-worker"
  schedule_expression = "cron(10 01-14/3 * * ? *)" # 10:10, 13:10, 16:10, 19:10, 22:10 (+09)
  tags                = var.common_tags
}

resource "aws_cloudwatch_event_target" "start_up_weekday_target" {
  rule = aws_cloudwatch_event_rule.start_up_weekday_rule.name
  arn  = aws_lambda_function.ecs_task_scaler.arn
  input = jsonencode({
    "service_scales" : [
      { "service_name" : "${aws_ecs_service.scrape_service.name}", "desired_task_count" : "1" },
      { "service_name" : "${aws_ecs_service.calc_service.name}", "desired_task_count" : "2" }
  ] })
}

resource "aws_cloudwatch_event_target" "start_up_weekend_target" {
  rule = aws_cloudwatch_event_rule.start_up_weekend_rule.name
  arn  = aws_lambda_function.ecs_task_scaler.arn
  input = jsonencode({
    "service_scales" : [
      { "service_name" : "${aws_ecs_service.scrape_service.name}", "desired_task_count" : "1" },
      { "service_name" : "${aws_ecs_service.calc_service.name}", "desired_task_count" : "2" }
  ] })
}

resource "aws_cloudwatch_event_target" "shut_down_target" {
  rule = aws_cloudwatch_event_rule.shut_down_rule.name
  arn  = aws_lambda_function.ecs_task_scaler.arn
  input = jsonencode({
    "service_scales" : [
      { "service_name" : "${aws_ecs_service.scrape_service.name}", "desired_task_count" : "0" },
      { "service_name" : "${aws_ecs_service.calc_service.name}", "desired_task_count" : "0" },
      { "service_name" : "${aws_ecs_service.monitor_service.name}", "desired_task_count" : "0" }
  ] })
}

resource "aws_cloudwatch_event_target" "restart_target" {
  rule = aws_cloudwatch_event_rule.restart_rule.name
  arn  = aws_lambda_function.ecs_task_stopper.arn
}

resource "aws_lambda_permission" "allow_eventbridge_start_up_weekend" {
  statement_id  = "AllowEventBridge-${var.env}-start-up-weekend"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ecs_task_scaler.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.start_up_weekend_rule.arn
}

resource "aws_lambda_permission" "allow_eventbridge_start_up_weekday" {
  statement_id  = "AllowEventBridge-${var.env}-start-up-weekday"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ecs_task_scaler.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.start_up_weekday_rule.arn
}

resource "aws_lambda_permission" "allow_eventbridge_shut_down" {
  statement_id  = "AllowEventBridge-${var.env}-shut-down"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ecs_task_scaler.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.shut_down_rule.arn
}

resource "aws_lambda_permission" "allow_eventbridge_restart" {
  statement_id  = "AllowEventBridge-${var.env}-restart"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ecs_task_stopper.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.restart_rule.arn
}

