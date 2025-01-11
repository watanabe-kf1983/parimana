output "web_api_lambda_arn" {
  value = aws_lambda_function.web_api.invoke_arn
}

output "web_api_lambda_name" {
  value = aws_lambda_function.web_api.function_name
}
