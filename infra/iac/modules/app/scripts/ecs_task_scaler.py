import os

import boto3


def lambda_handler(event, context):

    cluster_name = os.environ['CLUSTER_NAME']
    service_name = os.environ['SERVICE_NAME']

    if event.get("desired_task_count") is not None:
        desired_count = int(event["desired_task_count"])
    else:
        raise ValueError("Event must include 'desired_task_count'")

    ecs = boto3.client('ecs')
    response = ecs.update_service(
        cluster=cluster_name,
        service=service_name,
        desiredCount=desired_count
    )
    return response
