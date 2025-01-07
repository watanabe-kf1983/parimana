```bash
export $(grep -v '^#' env/.env | xargs)
export CODEBUILD_SRC_DIR="$(dirname $(realpath .))"
script/pre_build.sh
script/check.sh
script/build.sh
```