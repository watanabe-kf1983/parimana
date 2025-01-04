output "pipeline_id" {
  value       = aws_codepipeline.main_pipeline.id
  description = "ID of the CI/CD pipeline"
}
