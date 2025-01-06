```bash
export $(grep -v '^#' env/.env | xargs)
export CODEBUILD_SRC_DIR="$(dirname $(realpath .))"
script/pre_build.sh
script/build.sh
```