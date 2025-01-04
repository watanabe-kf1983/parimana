output "pipeline_id" {
  value       = aws_codepipeline.main_pipeline.id
  description = "ID of the CI/CD pipeline"
}

output "codebuild_project_name" {
  value       = aws_codebuild_project.main_project.name
  description = "Name of the CodeBuild project"
}
