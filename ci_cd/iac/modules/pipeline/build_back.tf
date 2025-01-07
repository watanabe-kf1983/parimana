
resource "aws_codebuild_project" "back" {
  name         = "${var.target_project_name}-back"
  description  = "CodeBuild project for building back of ${var.target_project_name}"
  service_role = aws_iam_role.build_back_role.arn

  artifacts {
    type = "CODEPIPELINE"
  }

  environment {
    compute_type = "BUILD_GENERAL1_SMALL"
    image        = "aws/codebuild/standard:7.0"
    type         = "LINUX_CONTAINER"

    environment_variable {
      name  = "AWS_REGION"
      value = var.aws_region
    }

    environment_variable {
      name  = "PROJECT_NAME"
      value = var.target_project_name
    }

    environment_variable {
      name  = "ENV"
      value = var.env
    }
  }

  source {
    type      = "CODEPIPELINE"
    buildspec = "back/buildspec.yml"
  }

  cache {
    type  = "LOCAL"
    modes = ["LOCAL_SOURCE_CACHE", "LOCAL_DOCKER_LAYER_CACHE"]
  }

  logs_config {
    cloudwatch_logs {
      status      = "ENABLED"
      group_name  = "/aws/codebuild/${var.cicd_project_name}"
      stream_name = "${var.env}.back"
    }
  }

  tags = var.common_tags
}

resource "aws_iam_role" "build_back_role" {
  name = "${var.cicd_project_name}-build-${var.env}-back-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "codebuild.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
  tags = var.common_tags
}

resource "aws_iam_role_policy_attachment" "build_back_policy" {
  role       = aws_iam_role.build_back_role.name
  policy_arn = aws_iam_policy.build_back_policy.arn
}

resource "aws_iam_policy" "build_back_policy" {
  name        = "BuildbackPolicyAccess-${var.env}"
  description = "Custom policy for build back of ${var.target_project_name}"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        "Effect" : "Allow",
        "Action" : [
          "ecr:GetAuthorizationToken",
          "ecr:BatchCheckLayerAvailability",
          "ecr:CompleteLayerUpload",
          "ecr:DescribeRepositories",
          "ecr:GetDownloadUrlForLayer",
          "ecr:InitiateLayerUpload",
          "ecr:PutImage",
          "ecr:UploadLayerPart"
        ],
        "Resource" : "*"
      },
      {
        "Effect" : "Allow",
        "Action" : [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        "Resource" : "*"
      },
      {
        "Effect" : "Allow",
        "Action" : [
          "s3:GetObject",
          "s3:PutObject",
          "s3:GetObjectVersion"
        ],
        "Resource" : "*"
      }
    ]
  })
}
