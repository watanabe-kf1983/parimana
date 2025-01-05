
resource "aws_codepipeline" "main_pipeline" {
  name          = "${var.target_project_name}-pipeline"
  role_arn      = aws_iam_role.codepipeline_role.arn
  pipeline_type = "V2"

  artifact_store {
    type     = "S3"
    location = aws_s3_bucket.artifacts.bucket
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
    name = "Build_Infra"

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
  }

  tags = local.common_tags
}


resource "aws_iam_role" "codepipeline_role" {
  name = "${var.project_name}-codepipeline-role"

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
  tags = local.common_tags
}


resource "aws_iam_policy_attachment" "codepipeline_policy" {
  name       = "${var.project_name}-codepipeline-policy-attachment"
  roles      = [aws_iam_role.codepipeline_role.name]
  policy_arn = aws_iam_policy.codepipeline_policy.arn
}


resource "aws_iam_policy" "codepipeline_policy" {
  name        = "${var.project_name}-codepipeline-policy"
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
    ]
  })
}
