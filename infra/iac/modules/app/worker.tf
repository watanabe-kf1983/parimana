resource "aws_ecs_cluster" "app_cluster" {
  name = "${var.project_name}-${var.env}-cluster"

  tags = merge(var.common_tags, { Name = "${var.project_name}-${var.env}-cluster" })
}

resource "aws_iam_role" "ecs_task_execution_role" {
  name = "${var.project_name}-${var.env}-ecs-task-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect    = "Allow"
        Principal = { Service = "ecs-tasks.amazonaws.com" }
        Action    = "sts:AssumeRole"
      }
    ]
  })
  tags = var.common_tags
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_attachment" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = aws_iam_policy.ecs_task_execution_policy.arn
}

resource "aws_iam_policy" "ecs_task_execution_policy" {
  name        = "AmazonECSTaskExecutionRolePolicy-${var.env}"
  description = "Custom policy for build infra of ${var.project_name}"
  policy = jsonencode({
    Version = "2012-10-17"
    "Statement" : [
      {
        "Effect" : "Allow",
        "Action" : [
          "ecr:GetAuthorizationToken",
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        "Resource" : "*"
      }
    ]
  })
  tags = var.common_tags
}

resource "aws_iam_role" "ecs_task_role" {
  name = "${var.project_name}-${var.env}-ecs-task-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect    = "Allow"
        Principal = { Service = "ecs-tasks.amazonaws.com" }
        Action    = "sts:AssumeRole"
      }
    ]
  })
  tags = var.common_tags
}

resource "aws_iam_role_policy" "ecs_task_policy" {
  name = "${var.project_name}-${var.env}-ecs-task-policy"
  role = aws_iam_role.ecs_task_role.id
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
      }
    ]
  })
}


resource "aws_ecs_task_definition" "app_task" {
  family                   = "${var.project_name}-${var.env}-task"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = "2048"
  memory                   = "4096"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      name      = "${var.project_name}-backend"
      image     = "hello-world"
      cpu       = 2048
      memory    = 4096
      essential = true
      command   = ["parimana", "service"]
      environment = [
        {
          name  = "REDIS_ENDPOINT"
          value = "${aws_elasticache_replication_group.redis.primary_endpoint_address}"
        },
        {
          name  = "STORAGE__TYPE"
          value = "s3"
        },
        {
          name  = "STORAGE__URI"
          value = "s3://${aws_s3_bucket.app.bucket}/"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = "${aws_cloudwatch_log_group.app_logs.name}"
          awslogs-region        = "${var.aws_region}"
          awslogs-stream-prefix = "ecs/app_task"
        }
      }
    }
  ])
  tags = var.common_tags
}

resource "aws_ecs_service" "app_service" {
  name            = "${var.project_name}-${var.env}-service"
  cluster         = aws_ecs_cluster.app_cluster.id
  task_definition = aws_ecs_task_definition.app_task.arn
  desired_count   = 0
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = var.private_subnet_ids
    security_groups  = [aws_security_group.ecs_sg.id]
    assign_public_ip = false
  }

  lifecycle {
    ignore_changes = [
      task_definition,
      desired_count
    ]
  }

  tags = merge(var.common_tags, { Name = "${var.project_name}-${var.env}-service" })
}

resource "aws_security_group" "ecs_sg" {
  name   = "${var.project_name}-${var.env}-ecs-sg"
  vpc_id = var.vpc_id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.common_tags, { Name = "${var.project_name}-${var.env}-ecs-sg" })
}

