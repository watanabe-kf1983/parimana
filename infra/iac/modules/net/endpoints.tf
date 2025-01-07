resource "aws_vpc_endpoint" "s3" {
  vpc_id       = aws_vpc.main.id
  service_name = "com.amazonaws.${var.aws_region}.s3"
  vpc_endpoint_type = "Gateway"
  route_table_ids = [aws_route_table.public.id]
  tags = merge(var.common_tags, { Name = "${var.project_name}-${var.env}-vpce-s3" })
}

resource "aws_vpc_endpoint" "ecr_dkr" {
  vpc_id            = aws_vpc.main.id
  # "ecr.api"は費用対効果が薄いので作らない
  service_name      = "com.amazonaws.${var.aws_region}.ecr.dkr"
  vpc_endpoint_type = "Interface"
  subnet_ids        = [aws_subnet.private.id]
  security_group_ids = [aws_security_group.vpce_sg.id]
  private_dns_enabled = true
  tags = merge(var.common_tags, { Name = "${var.project_name}-${var.env}-vpce-ecr-dkr" })
}


resource "aws_security_group" "vpce_sg" {
  name   = "${var.project_name}-${var.env}-vpce-sg"
  vpc_id = aws_vpc.main.id

  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = [aws_subnet.private.cidr_block]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.common_tags, { Name = "${var.project_name}-${var.env}-vpce-sg" })
}
