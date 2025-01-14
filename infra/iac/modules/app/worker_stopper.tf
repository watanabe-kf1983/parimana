resource "aws_iam_role" "lambda_ecs_stopper_role" {
  name = "${var.project_name}-${var.env}-lambda-ecs-stopper-role"

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

resource "aws_iam_policy" "lambda_ecs_stopper_policy" {
  name        = "${var.project_name}-${var.env}-lambda-ecs-stopper-policy"
  description = "Policy to allow Lambda to manage ECS services"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "ecs:ListTasks",
          "ecs:StopTask"
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

resource "aws_iam_role_policy_attachment" "lambda_ecs_stopper_role_policy_attachment" {
  role       = aws_iam_role.lambda_ecs_stopper_role.name
  policy_arn = aws_iam_policy.lambda_ecs_stopper_policy.arn
}


data "archive_file" "lambda_ecs_stopper_zip" {
  type        = "zip"
  source_file = "${path.module}/scripts/ecs_task_stopper.py"
  output_path = "${path.module}/scripts/ecs_task_stopper.zip"
}

resource "aws_lambda_function" "ecs_task_stopper" {
  function_name = "${var.project_name}-${var.env}-ecs-task-stopper"
  role          = aws_iam_role.lambda_ecs_stopper_role.arn

  filename         = data.archive_file.lambda_ecs_stopper_zip.output_path
  source_code_hash = filebase64sha256(data.archive_file.lambda_ecs_stopper_zip.output_path)
  handler          = "ecs_task_stopper.lambda_handler"
  runtime          = "python3.13"
  memory_size      = 512
  timeout          = 10
  environment {
    variables = {
      CLUSTER_NAME = aws_ecs_cluster.app_cluster.name
      SERVICE_NAME = aws_ecs_service.app_service.name
    }
  }

  tags = var.common_tags
}
