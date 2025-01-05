## Set up

.env.example を参考に .envファイルを作成したのち、以下のコマンドを実行

```bash

export $(grep -v '^#' env/.env | xargs)

echo $AWS_REGION 
echo $PROJECT_NAME

export TFSTATE_BUCKET_NAME="${PROJECT_NAME}-infra-resources-tfstate"
echo $TFSTATE_BUCKET_NAME

# set up tfstate bucket
setup/setup_tfstate_bucket.sh

# set up terraform 
cd iac
terraform init \
  -backend-config="bucket=${TFSTATE_BUCKET_NAME}" \
  -backend-config="region=${AWS_REGION}"

```