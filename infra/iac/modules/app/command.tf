resource "aws_lambda_function" "command" {
  function_name = "${var.project_name}-${var.env}-command"
  role          = aws_iam_role.web_api_role.arn
  package_type  = "Image"
  image_uri     = "${var.aws_account_id}.dkr.ecr.ap-northeast-1.amazonaws.com/hello-world:latest"
  memory_size   = 2048
  timeout       = 30
  vpc_config {
    subnet_ids         = var.private_subnet_ids
    security_group_ids = [aws_security_group.lambda_sg.id]
  }
  image_config {
    entry_point = ["python", "-m", "awslambdaric"]
    command     = ["parimana.interfaces.aws_lambda.command.handler"]
  }
  environment {
    variables = {
      STORAGE__TYPE     = "s3"
      STORAGE__URI      = "s3://${aws_s3_bucket.app.bucket}/store/"
      OUTPUT__TYPE     = "s3"
      OUTPUT__URI      = "s3://${aws_s3_bucket.app.bucket}/out/"
      REDIS_ENDPOINT    = aws_elasticache_replication_group.redis.primary_endpoint_address
      AUTO_ANALYSE_MODE = "False"
    }
  }
  lifecycle {
    ignore_changes = [
      image_uri
    ]
  }

  tags = merge(var.common_tags, { Name = "${var.project_name}-${var.env}-command" })
}
