#!/bin/sh

set -eux

cd ${CODEBUILD_SRC_DIR}/infra/iac/env/${ENV}
echo "Initializing Terraform"
terraform init \
    -backend-config="bucket=${TFSTATE_BUCKET}" \
    -backend-config="region=${AWS_REGION}"
