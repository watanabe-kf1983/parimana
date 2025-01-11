#!/bin/bash

set -euo pipefail

AWS_ACCOUNT_ID=$1
AWS_REGION=$2

echo "Pulling Docker image: hello-world"
docker pull hello-world

echo "Logging in to Amazon ECR"
ECR_DOMAIN=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
aws ecr get-login-password --region $AWS_REGION \
  | docker login --username AWS --password-stdin $ECR_DOMAIN

echo "Tagging and pushing Docker image to ECR"
docker tag hello-world $ECR_DOMAIN/hello-world:latest
docker push $ECR_DOMAIN/hello-world:latest

echo "Docker image pushed successfully!"