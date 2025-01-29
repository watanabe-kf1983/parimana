import os

import boto3


def lambda_handler(event, context):

    cluster_name = os.environ['CLUSTER_NAME']
    result = scale_services(cluster_name, event.get("service_scales"))
    return {"result": scale_services}


def scale_services(cluster_name, service_scales):

    ecs = boto3.client("ecs")
    return [
        ecs.update_service(
            cluster=cluster_name,
            service=service_scale["service_name"],
            desiredCount=int(service_scale["desired_count"]),
        )
        for service_scale in service_scales
    ]
