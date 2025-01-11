resource "aws_iam_role" "lambda_deploy_lambda" {
  name = "${var.cicd_project_name}-${var.env}-lambda-deploy-lambda-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
  tags = var.common_tags
}

resource "aws_iam_role_policy_attachment" "update_lambda_policy" {
  role       = aws_iam_role.lambda_deploy_lambda.name
  policy_arn = aws_iam_policy.update_lambda_policy.arn
}

resource "aws_iam_policy" "update_lambda_policy" {
  name        = "${var.cicd_project_name}-${var.env}-update-lambda-policy"
  description = "IAM policy for CodePipeline"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      # AWSLambdaBasicExecutionRole
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "*"
      },
      # Read artifact
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:ListBucket",
        ]
        Resource = "arn:aws:s3::*:codepipeline-*"
      },
      # Update Lambda
      {
        "Effect" : "Allow",
        "Action" : [
          "lambda:UpdateFunctionCode",
        ],
        "Resource" : "*"
      },
      # Codebuild PutJobResult
      {
        "Effect" : "Allow",
        "Action" : [
          "codepipeline:PutJobFailureResult",
          "codepipeline:PutJobSuccessResult"
        ],
        "Resource" : "*"
      }
    ]
  })
}


data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/scripts/deploy_lambda.py"
  output_path = "${path.module}/scripts/deploy_lambda.zip"
}

resource "aws_lambda_function" "deploy_image_as_lambda" {
  function_name = "${var.cicd_project_name}-${var.env}-deploy-image-as-webapi"
  runtime       = "python3.13"
  handler       = "deploy_lambda.lambda_handler"

  role = aws_iam_role.lambda_deploy_lambda.arn

  filename = data.archive_file.lambda_zip.output_path

  environment {
    variables = {
      UPDATE_FUNCTION_NAME = "${var.target_project_name}-${var.env}-webapi"
    }
  }

  tags = var.common_tags
}
