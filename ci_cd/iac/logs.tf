resource "aws_cloudwatch_log_group" "codebuild_logs" {
  name              = "/aws/codebuild/${var.cicd_project_name}"
  retention_in_days = 7
}