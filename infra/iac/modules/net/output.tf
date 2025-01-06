output "vpc_id" {
  value = aws_vpc.main.id
}

output "private_subnet_ids" {
  value = [aws_subnet.private.id]
}

output "private_subnet_cidrs" {
  value = [aws_subnet.private.cidr_block]
}
