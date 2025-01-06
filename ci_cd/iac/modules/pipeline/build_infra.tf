
resource "aws_codebuild_project" "infra" {
  name         = "${var.target_project_name}-${var.env}-infra"
  description  = "CodeBuild project for building infra of ${var.target_project_name}-${var.env}"
  service_role = aws_iam_role.build_infra_role.arn

  artifacts {
    type = "CODEPIPELINE"
  }

  environment {
    compute_type = "BUILD_GENERAL1_SMALL"
    image        = "public.ecr.aws/hashicorp/terraform:1.10.3"
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
      name  = "TFSTATE_BUCKET"
      value = var.s3_tfstate_store
    }

    environment_variable {
      name  = "ENV"
      value = var.env
    }
  }


  source {
    type      = "CODEPIPELINE"
    buildspec = "infra/buildspec.yml"
  }

  cache {
    type  = "LOCAL"
    modes = ["LOCAL_SOURCE_CACHE", "LOCAL_DOCKER_LAYER_CACHE"]
  }

  logs_config {
    cloudwatch_logs {
      status      = "ENABLED"
      group_name  = "/aws/codebuild/${var.cicd_project_name}"
      stream_name = "${var.env}.infra"
    }
  }

  tags = var.common_tags
}

resource "aws_iam_role" "build_infra_role" {
  name = "${var.cicd_project_name}-build-${var.env}-infra-role"

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

resource "aws_iam_role_policy_attachment" "build_infra_policy" {
  role       = aws_iam_role.build_infra_role.name
  policy_arn = aws_iam_policy.build_infra_policy.arn
}

resource "aws_iam_policy" "build_infra_policy" {
  name        = "BuildInfraPolicyAccess-${var.env}"
  description = "Custom policy for build infra of ${var.target_project_name}"
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


