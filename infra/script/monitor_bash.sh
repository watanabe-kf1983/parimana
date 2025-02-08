#!/bin/bash

set -eux

ECS_CLUSTER="${PROJECT_NAME}-${ENV}-cluster"
FLOWER_SERVICE="${PROJECT_NAME}-${ENV}-monitor-service"
CONTAINER_NAME="${PROJECT_NAME}-backend"

TASK_ARN=$(
    aws ecs list-tasks \
    --cluster $ECS_CLUSTER \
    --service-name $FLOWER_SERVICE \
    --query 'taskArns[0]' \
    --output text
)

TASK_ID=$(echo ${TASK_ARN} | sed -E 's/.+task\/.+\///g' )

aws ecs execute-command --cluster ${ECS_CLUSTER} \
    --task ${TASK_ID} \
    --container ${CONTAINER_NAME} \
    --interactive \
    --command "/bin/sh"