#!/bin/bash

set -euo pipefail

# 環境変数の確認（デバッグ用）
echo "AWS_REGION=${AWS_REGION}"
echo "CICD_TFSTATE_BUCKET_NAME=${CICD_TFSTATE_BUCKET_NAME}"

# 環境変数の検証
if [ -z "$AWS_REGION" ] || [ -z "$CICD_TFSTATE_BUCKET_NAME" ]; then
    echo "Missing required environment variables. Please check .env file."
    exit 1
fi

# S3バケットを作成
if aws s3api head-bucket --bucket "$CICD_TFSTATE_BUCKET_NAME" 2>/dev/null; then
    echo "Bucket $CICD_TFSTATE_BUCKET_NAME already exists. Skipping creation."
else
    echo "Creating S3 bucket: $CICD_TFSTATE_BUCKET_NAME"
    aws s3api create-bucket --bucket "$CICD_TFSTATE_BUCKET_NAME" --region "$AWS_REGION" \
      --create-bucket-configuration LocationConstraint="$AWS_REGION"
fi

# バージョニングを有効化
echo "Enabling versioning on bucket: $CICD_TFSTATE_BUCKET_NAME"
aws s3api put-bucket-versioning --bucket $CICD_TFSTATE_BUCKET_NAME --versioning-configuration Status=Enabled

echo "S3 bucket setup complete!"
