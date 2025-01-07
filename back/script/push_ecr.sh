#!/bin/sh

set -eux

echo Logging in to Amazon ECR...
aws --version
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query 'Account' --output text)
ECR_DOMAIN=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

aws ecr get-login-password --region $AWS_REGION \
  | docker login --username AWS --password-stdin $ECR_DOMAIN

echo Tagging the Docker image...
IMAGE_URI="${ECR_DOMAIN}/${IMAGE_REPO_NAME}:${IMAGE_TAG}"
docker tag $IMAGE_REPO_NAME:$IMAGE_TAG $IMAGE_URI

echo Pushing the Docker image to Amazon ECR...
docker push $IMAGE_URI
echo Docker image pushed successfully.

printf '[{"name":"%s","imageUri":"%s"}]' \
 $IMAGE_REPO_NAME \
 $IMAGE_URI \
 > ${CODEBUILD_SRC_DIR}/back/imagedefinitions.json