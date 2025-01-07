#!/bin/sh

set -eux

cd ${CODEBUILD_SRC_DIR}/back

echo Building the Docker image...
docker build -t $IMAGE_REPO_NAME:$IMAGE_TAG .
