
resource "aws_ecs_task_definition" "monitor_task" {
  family                   = "${var.project_name}-${var.env}-monitor-task"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = "512"
  memory                   = "1024"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      name      = "${var.project_name}-backend"
      image     = "hello-world"
      cpu       = 512
      memory    = 1024
      essential = true
      command   = ["parimana", "monitor"]
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
          value = "s3://${aws_s3_bucket.app.bucket}/store/"
        },
        {
          name  = "OUTPUT__TYPE"
          value = "s3"
        },
        {
          name  = "OUTPUT__URI"
          value = "s3://${aws_s3_bucket.app.bucket}/out/"
        },
        {
          name  = "AUTO_ANALYSE_MODE"
          value = "True"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = "${aws_cloudwatch_log_group.app_logs.name}"
          awslogs-region        = "${var.aws_region}"
          awslogs-stream-prefix = "ecs/monitor-task"
        }
      }
    }
  ])
  tags = var.common_tags
}

resource "aws_ecs_service" "monitor_service" {
  name            = "${var.project_name}-${var.env}-monitor-service"
  cluster         = aws_ecs_cluster.app_cluster.id
  task_definition = aws_ecs_task_definition.monitor_task.arn
  desired_count   = 0
  enable_execute_command = true
  
  capacity_provider_strategy {
    capacity_provider = "FARGATE_SPOT"
    weight            = 1
  }

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

  tags = merge(var.common_tags, { Name = "${var.project_name}-${var.env}-monitor-service" })
}
