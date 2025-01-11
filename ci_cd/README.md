## Set up

.env.example を参考に .envファイルを作成したのち、以下のコマンドを実行

```bash

export $(grep -v '^#' env/.env | xargs)
export CICD_TFSTATE_BUCKET_NAME="${CICD_PROJECT_NAME}-infra-resources-tfstate"

echo $AWS_REGION 
echo $CICD_PROJECT_NAME
echo $CICD_TFSTATE_BUCKET_NAME

# set up tfstate bucket
setup/setup_tfstate_bucket.sh

# set up terraform 
cd iac
terraform init \
  -backend-config="bucket=${CICD_TFSTATE_BUCKET_NAME}" \
  -backend-config="region=${AWS_REGION}"

# create resource
terraform plan
terraform apply
```