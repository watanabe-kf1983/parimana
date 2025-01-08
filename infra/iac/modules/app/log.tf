resource "aws_cloudwatch_log_group" "app_logs" {
  name              = "${var.project_name}-${var.env}-app-logs"
  retention_in_days = 7

  tags = merge(var.common_tags, {
    Name = "${var.project_name}-${var.env}-app-logs"
  })
}
