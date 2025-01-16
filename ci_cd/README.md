# Parimana CI/CDリソース

AWSに Parimanaソフトウェアを自動デプロイするための資材。  
構築にはAWSアカウントが必要で、運用にはAWS料金がかかります。

## あらまし
Terraformで以下の内容が定義されています

* ソフトウェアアーティファクト保存用リソース
  * S3バケット
  * ECR

* CI/CDパイプライン
  * CodePipeline
    * ソースアクション
      * Codestar Connectionソースアクション
    * ビルドアクション
      * Infra, Front, Back - CodeBuildアクション
    * デプロイアクション
      * Front  - S3デプロイアクション
      * Worker - ECSデプロイアクション
      * WebAPI - Lambda呼び出しアクション
  * CodeBuildプロジェクト
    * Infra - AWSインフラのビルド
    * Front - Web資材のビルド
    * Back - バックエンドコンテナイメージのビルド

## 構築準備
### 必要ソフトウェア
* Terraform
* AWS CLI

../.devcontainer/infra の Docker Fileも参考にしてください

### AWSアカウント/IAM Role
* なんでもできる IAM Role

### 事前設定
* env/.envファイル  
env/.env.example を参考に作成します

* iac/terraform.tfvarsファイル  
iac/terraform.tfvars.template を参考に作成します

## 構築
以下のコマンドを実行します

```bash

# 設定を読み込む
export $(grep -v '^#' env/.env | xargs)
export CICD_TFSTATE_BUCKET_NAME="${CICD_PROJECT_NAME}-infra-resources-tfstate"

# 設定が読み込まれたことを確認
echo $AWS_REGION 
echo $CICD_PROJECT_NAME
echo $CICD_TFSTATE_BUCKET_NAME

# CICD環境構築用 tfstate bucket を作成
setup/setup_tfstate_bucket.sh

# Terraform準備 
cd iac
terraform init \
  -backend-config="bucket=${CICD_TFSTATE_BUCKET_NAME}" \
  -backend-config="region=${AWS_REGION}"

# Terraformによる構築実行
terraform plan
terraform apply
```