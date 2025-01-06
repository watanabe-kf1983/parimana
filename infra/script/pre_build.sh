#!/bin/bash

set -euo pipefail

cd infra/iac/${ENV}
echo "Initializing Terraform"
terraform init \
    -backend-config="bucket=${TFSTATE_BUCKET}" \
    -backend-config="region=${AWS_REGION}"
