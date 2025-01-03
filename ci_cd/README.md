## Set up

.env.example を参考に .envファイルを作成したのち、以下のコマンドを実行

```bash

export $(grep -v '^#' .env | xargs)

echo $AWS_REGION 
echo $PROJECT_NAME

export TFSTATE_BUCKET_NAME="${PROJECT_NAME}-resources-tfstate"
echo $TFSTATE_BUCKET_NAME

# set up tfstate bucket
./setup_tfstate_bucket.sh

```