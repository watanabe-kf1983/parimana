import os

import boto3


def lambda_handler(event, context):

    cluster_name = os.environ["CLUSTER_NAME"]
    service_name = os.environ["SERVICE_NAME"]

    ecs = boto3.client("ecs")
    listed_tasks = ecs.list_tasks(
        cluster=cluster_name,
        serviceName=service_name
    )
    task_arns = listed_tasks.get("taskArns", [])
    for task_arn in task_arns:
        ecs.stop_task(
            cluster=cluster_name, task=task_arn, reason="Periodic task restart"
        )

    return {"statusCode": 200, "body": f"Stopped tasks: {task_arns}"}
