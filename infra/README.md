# Parimana AWSインフラ

AWSでParimanaを動かすためのリソース定義です。
概略は `docs/aws-resources.drawio` に書かれた構成図を参照してください。

構築・運用にはAWS料金がかかります。  
また、構築には `../ci_cd` ディレクトリの資材によるCI/CDパイプラインを用いるとラクです。

### CI/CDパイプラインを用いず構築するには

#### 必要ソフトウェア
* Terraform
* AWS CLI

#### 事前設定
* env/.envファイル  
env/.env.example を参考に作成します

#### 構築実行

```bash
# 設定を読み込む
export $(grep -v '^#' env/.env | xargs)
export CODEBUILD_SRC_DIR="$(dirname $(realpath .))"
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query 'Account' --output text)

# Terraform準備 
script/pre_build.sh

# Terraformによる構築実行
script/check.sh
script/build.sh

```

#### 全部消すには

```bash
script/destroy.sh
```

#### インフラ構築のあと
サービスを動かすにはさらに以下の対応が必要です。

* Web資材のビルド
* バックエンドイメージのビルド
* ECSタスク定義の更新
* Lambda関数の更新
* Web資材の更新

 `../ci_cd` ディレクトリにはこれらを行うCI/CDパイプラインが定義されているので、これを使うとラクです
