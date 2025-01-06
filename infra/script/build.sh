#!/bin/sh

set -euo pipefail

cd ${CODEBUILD_SRC_DIR}/infra/iac/env/${ENV}

export TF_VAR_aws_region=$AWS_REGION
export TF_VAR_project_name=$PROJECT_NAME
export TF_VAR_env=$ENV

echo "Applying Terraform"
terraform apply -auto-approve