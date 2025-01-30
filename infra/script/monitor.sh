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

RUNTIME_ID=$(
    aws ecs describe-tasks --cluster $ECS_CLUSTER --task $TASK_ID \
    | jq -r --arg CONTAINER_NAME $CONTAINER_NAME \
       '.tasks[0].containers[]
        | select(.name == $CONTAINER_NAME).runtimeId'
)

# AWS un-official method
# https://tech.dentsusoken.com/entry/aws__fargat_ecs_exec#start-session-with-AWS-StartPortForwardingSession

SSM_TARGET_ID="ecs:${ECS_CLUSTER}_${TASK_ID}_${RUNTIME_ID}"

aws ssm start-session --target $SSM_TARGET_ID \
    --document-name AWS-StartPortForwardingSession \
    --parameters '{"portNumber":["5555"],"localPortNumber":["5555"]}'

