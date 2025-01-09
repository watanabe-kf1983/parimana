## Set up

.env.example を参考に .envファイルを作成したのち、以下のコマンドを実行

```bash

export $(grep -v '^#' env/.env | xargs)

echo $AWS_REGION 
echo $CICD_PROJECT_NAME

export CICD_TFSTATE_BUCKET_NAME="${CICD_PROJECT_NAME}-infra-resources-tfstate"
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

# push hello-world image
aws ecr create-repository --repository-name hello-world
docker pull hello-world
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query 'Account' --output text)
ECR_DOMAIN=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
aws ecr get-login-password --region $AWS_REGION \
  | docker login --username AWS --password-stdin $ECR_DOMAIN
docker tag hello-world $ECR_DOMAIN/hello-world:latast
docker push $ECR_DOMAIN/hello-world:latast
```