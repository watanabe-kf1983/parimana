
resource "aws_codepipeline" "main_pipeline" {
  name          = "${var.target_project_name}-${var.env}-pipeline"
  role_arn      = aws_iam_role.codepipeline_role.arn
  pipeline_type = "V2"

  artifact_store {
    type     = "S3"
    location = var.s3_artifact_store
  }

  stage {
    name = "Source"

    action {
      name             = "Source"
      category         = "Source"
      owner            = "AWS"
      provider         = "CodeStarSourceConnection"
      version          = "1"
      output_artifacts = ["source_output"]

      configuration = {
        ConnectionArn    = var.source_repository.connection_arn
        FullRepositoryId = var.source_repository.full_repository_id
        BranchName       = var.source_repository.branch_name
        DetectChanges    = "true"
      }
    }
  }

  stage {
    name = "Build"

    action {
      name             = "Build_Infra"
      category         = "Build"
      owner            = "AWS"
      provider         = "CodeBuild"
      version          = "1"
      input_artifacts  = ["source_output"]
      output_artifacts = ["build_infra_output"]

      configuration = {
        ProjectName = aws_codebuild_project.infra.name
      }
    }

    action {
      name             = "Build_Front"
      category         = "Build"
      owner            = "AWS"
      provider         = "CodeBuild"
      version          = "1"
      input_artifacts  = ["source_output"]
      output_artifacts = ["build_front_output"]

      configuration = {
        ProjectName = aws_codebuild_project.front.name
      }
    }

    action {
      name             = "Build_Back"
      category         = "Build"
      owner            = "AWS"
      provider         = "CodeBuild"
      version          = "1"
      input_artifacts  = ["source_output"]
      output_artifacts = ["build_back_output"]

      configuration = {
        ProjectName = aws_codebuild_project.back.name
      }
    }

  }

  stage {
    name = "Deploy"

    action {
      name            = "Deploy_Front"
      category        = "Deploy"
      owner           = "AWS"
      provider        = "S3"
      version         = "1"
      input_artifacts = ["build_front_output"]

      configuration = {
        BucketName = "${var.target_project_name}-${var.env}-web"
        Extract    = "true"
      }
    }

    action {
      name            = "Deploy_Worker"
      category        = "Deploy"
      owner           = "AWS"
      provider        = "ECS"
      version         = "1"
      input_artifacts = ["build_back_output"]

      configuration = {
        ClusterName = "${var.target_project_name}-${var.env}-cluster"
        ServiceName = "${var.target_project_name}-${var.env}-service"
      }
    }

  }

  tags = var.common_tags
}


resource "aws_iam_role" "codepipeline_role" {
  name = "${var.cicd_project_name}-codepipeline-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "codepipeline.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
  tags = var.common_tags
}


resource "aws_iam_policy_attachment" "codepipeline_policy" {
  name       = "${var.cicd_project_name}-codepipeline-policy-attachment"
  roles      = [aws_iam_role.codepipeline_role.name]
  policy_arn = aws_iam_policy.codepipeline_policy.arn
}


resource "aws_iam_policy" "codepipeline_policy" {
  name        = "${var.cicd_project_name}-codepipeline-policy"
  description = "Minimal IAM policy for CodePipeline"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      # S3: Artifact storage
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ]
        Resource = "*"
      },
      # CodeBuild: Trigger builds
      {
        Effect = "Allow"
        Action = [
          "codebuild:StartBuild",
          "codebuild:BatchGetBuilds"
        ]
        Resource = "*"
      },
      # CodeStar Connections
      {
        "Effect" : "Allow",
        "Action" : [
          "codestar:*",
          "codestar-connections:*",
        ],
        "Resource" : "*"
      },
      # ECS Deploy
      {
        "Effect" : "Allow",
        "Action" : [
          "ecs:*",
        ],
        "Resource" : "*"
      },
      {
        "Action" : "iam:PassRole",
        "Effect" : "Allow",
        "Resource" : ["arn:aws:iam::${var.aws_account_id}:role/${var.target_project_name}-${var.env}-ecs-task-role",
                      "arn:aws:iam::${var.aws_account_id}:role/${var.target_project_name}-${var.env}-ecs-task-execution-role"],
        "Condition" : {
          "StringEqualsIfExists" : {
            "iam:PassedToService" : [
              "ecs-tasks.amazonaws.com"
            ]
          }
        }
      }
    ]
  })
}

resource "aws_cloudwatch_log_group" "codebuild_logs" {
  name              = "/aws/codebuild/${var.cicd_project_name}"
  retention_in_days = 7
}
