resource "aws_iam_role" "lambda_ecs_scaler_role" {
  name = "${var.project_name}-${var.env}-lambda-ecs-scaler-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  tags = var.common_tags
}

resource "aws_iam_policy" "lambda_ecs_scaler_policy" {
  name        = "${var.project_name}-${var.env}-lambda-ecs-scaler-policy"
  description = "Policy to allow Lambda to manage ECS services"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "ecs:UpdateService"
        ],
        Resource = "*",
        Effect   = "Allow"
      },
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Resource = "*",
        Effect   = "Allow"
      }
    ]
  })

  tags = var.common_tags
}

resource "aws_iam_role_policy_attachment" "lambda_ecs_scaler_role_policy_attachment" {
  role       = aws_iam_role.lambda_ecs_scaler_role.name
  policy_arn = aws_iam_policy.lambda_ecs_scaler_policy.arn
}


data "archive_file" "lambda_ecs_scaler_zip" {
  type        = "zip"
  source_file = "${path.module}/scripts/ecs_service_scaler.py"
  output_path = "${path.module}/scripts/ecs_service_scaler.zip"
}

resource "aws_lambda_function" "ecs_task_scaler" {
  function_name = "${var.project_name}-${var.env}-ecs-task-scaler"
  role          = aws_iam_role.lambda_ecs_scaler_role.arn

  filename         = data.archive_file.lambda_ecs_scaler_zip.output_path
  source_code_hash = filebase64sha256(data.archive_file.lambda_ecs_scaler_zip.output_path)
  handler          = "ecs_service_scaler.lambda_handler"
  runtime          = "python3.13"
  memory_size      = 512
  timeout          = 10
  environment {
    variables = {
      CLUSTER_NAME = aws_ecs_cluster.app_cluster.name
    }
  }

  tags = var.common_tags
}
