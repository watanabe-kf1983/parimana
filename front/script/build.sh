#!/bin/sh

set -eux

cd ${CODEBUILD_SRC_DIR}/front

echo "Build Frontend File"
docker build \
  --target build-stage \
  -t front-build-stage \
  --build-arg BUILD_OPT=${ENV} \
  .
docker create --name temp-front-container front-build-stage
docker cp temp-front-container:/app/dist ./dist
docker rm temp-front-container