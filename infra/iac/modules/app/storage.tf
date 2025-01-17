resource "aws_s3_bucket" "app" {
  bucket        = "${var.project_name}-${var.env}-app"
  force_destroy = true

  tags = merge(var.common_tags, { Name = "${var.project_name}-${var.env}-app" })
}

resource "aws_elasticache_subnet_group" "redis_subnet_group" {
  name       = "${var.project_name}-${var.env}-redis-subnet-group"
  subnet_ids = var.private_subnet_ids
  tags       = merge(var.common_tags, { Name = "${var.project_name}-${var.env}-redis-subnet-group" })
}

resource "aws_elasticache_replication_group" "redis" {
  description                = "Redis replication group for ${var.project_name}-${var.env}"
  replication_group_id       = "${var.project_name}-${var.env}-redis-rg"
  engine                     = "redis"
  engine_version             = "7.1"
  node_type                  = "cache.t3.small"
  num_cache_clusters         = 1
  automatic_failover_enabled = false
  parameter_group_name       = "default.redis7"
  security_group_ids         = [aws_security_group.redis_sg.id]
  subnet_group_name          = aws_elasticache_subnet_group.redis_subnet_group.name

  tags = merge(var.common_tags, { Name = "${var.project_name}-${var.env}-redis-replication-group" })
}

resource "aws_security_group" "redis_sg" {
  name   = "${var.project_name}-${var.env}-redis-sg"
  vpc_id = var.vpc_id

  ingress {
    from_port   = 6379
    to_port     = 6379
    protocol    = "tcp"
    cidr_blocks = var.private_subnet_cidrs
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.common_tags, { Name = "${var.project_name}-${var.env}-redis-sg" })
}
