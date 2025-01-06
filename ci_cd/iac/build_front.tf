
resource "aws_codebuild_project" "front" {
  name         = "${var.target_project_name}-front"
  description  = "CodeBuild project for building front of ${var.target_project_name}"
  service_role = aws_iam_role.build_front_role.arn

  artifacts {
    type = "CODEPIPELINE"
  }

  environment {
    compute_type = "BUILD_GENERAL1_SMALL"
    image        = "aws/codebuild/standard:7.0"
    type         = "LINUX_CONTAINER"

    environment_variable {
      name  = "ENV"
      value = "prod"
    }
  }

  source {
    type      = "CODEPIPELINE"
    buildspec = "front/buildspec.yml"
  }

  cache {
    type  = "LOCAL"
    modes = ["LOCAL_SOURCE_CACHE", "LOCAL_DOCKER_LAYER_CACHE"]
  }

  logs_config {
    cloudwatch_logs {
      status      = "ENABLED"
      group_name  = "/aws/codebuild/${var.cicd_project_name}"
      stream_name = "front"
    }
  }

  tags = local.common_tags
}

resource "aws_iam_role" "build_front_role" {
  name = "${var.cicd_project_name}-build-front-role"

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
  tags = local.common_tags
}

resource "aws_iam_role_policy_attachment" "build_front_policy" {
  role       = aws_iam_role.build_front_role.name
  policy_arn = aws_iam_policy.build_front_policy.arn
}

resource "aws_iam_policy" "build_front_policy" {
  name        = "BuildfrontPolicyAccess"
  description = "Custom policy for build front of ${var.target_project_name}"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = "*"
        Resource = "*"
      }
    ]
  })
}
