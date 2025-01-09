```bash
export $(grep -v '^#' env/.env | xargs)
export CODEBUILD_SRC_DIR="$(dirname $(realpath .))"
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query 'Account' --output text)
script/pre_build.sh
script/check.sh
script/build.sh
```