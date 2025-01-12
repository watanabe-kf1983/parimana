resource "aws_lambda_function" "web_api" {
  function_name = "${var.project_name}-${var.env}-web-api"
  role          = aws_iam_role.web_api_role.arn
  package_type  = "Image"
  image_uri     = "${var.aws_account_id}.dkr.ecr.ap-northeast-1.amazonaws.com/hello-world:latest"
  memory_size   = 2048
  timeout       = 30
  vpc_config {
    subnet_ids         = var.private_subnet_ids
    security_group_ids = [aws_security_group.lambda_sg.id]
  }
  image_config {
    entry_point = ["python", "-m", "awslambdaric"]
    command     = ["parimana.ui.web.lambda_handler"]
  }
  environment {
    variables = {
      STORAGE__TYPE      = "s3"
      STORAGE__URI       = "s3://${aws_s3_bucket.app.bucket}/"
      REDIS_ENDPOINT     = aws_elasticache_replication_group.redis.primary_endpoint_address
      OTHER_ENV_VARIABLE = "value"
    }
  }
  lifecycle {
    ignore_changes = [
      image_uri
    ]
  }

  tags = merge(var.common_tags, { Name = "${var.project_name}-${var.env}-web-api" })
}

resource "aws_iam_role" "web_api_role" {
  name = "${var.project_name}-${var.env}-web-api-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy" "web_api_policy" {
  name = "${var.project_name}-${var.env}-web-api-policy"
  role = aws_iam_role.web_api_role.id
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      # If you don’t have the s3:ListBucket permission, Amazon S3 returns an HTTP status code 403 Forbidden error.
      # https://docs.aws.amazon.com/ja_jp/AmazonS3/latest/API/API_HeadObject.html
      {
        Effect = "Allow",
        Action = [
          "s3:ListBucket",
        ],
        Resource = "arn:aws:s3:::${aws_s3_bucket.app.bucket}"
      },
      {
        Effect = "Allow",
        Action = [
          "s3:GetObject",
          "s3:PutObject"
        ],
        Resource = "arn:aws:s3:::${aws_s3_bucket.app.bucket}/*"
      },
      {
        Effect   = "Allow",
        Action   = "elasticache:*",
        Resource = "*"
      },
      #AWSLambdaVPCAccessExecutionRole
      {
        Effect = "Allow",
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
          "ec2:CreateNetworkInterface",
          "ec2:DescribeNetworkInterfaces",
          "ec2:DescribeSubnets",
          "ec2:DeleteNetworkInterface",
          "ec2:AssignPrivateIpAddresses",
          "ec2:UnassignPrivateIpAddresses"
        ],
        Resource = "*"
      }
    ]
  })
}

resource "aws_security_group" "lambda_sg" {
  name   = "${var.project_name}-${var.env}-lambda-sg"
  vpc_id = var.vpc_id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.common_tags, { Name = "${var.project_name}-${var.env}-lambda-sg" })
}
