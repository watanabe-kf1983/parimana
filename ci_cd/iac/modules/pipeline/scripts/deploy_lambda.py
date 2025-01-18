import io
import os
import json
import zipfile
from contextlib import contextmanager

import boto3


def lambda_handler(event, context):
    
    with codepipeline_job(event):
        image_uri = get_image_uri(get_input_from_event(event))
        function_name = get_function_name(event)
        update_lambda(function_name, image_uri)

    return {
        'statusCode': 200,
        'body': 'Lambda function updated successfully!'
    }


def update_lambda(function_name, image_uri):
    lambda_client = boto3.client('lambda')
    lambda_client.update_function_code(
        FunctionName=function_name,
        ImageUri=image_uri
    )


def get_function_name(event):
    return event['CodePipeline.job']['data']['actionConfiguration']['configuration']['UserParameters']


def get_input_from_event(event):
    s3_bucket = event['CodePipeline.job']['data']['inputArtifacts'][0]['location']['s3Location']['bucketName']
    s3_key = event['CodePipeline.job']['data']['inputArtifacts'][0]['location']['s3Location']['objectKey']

    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=s3_bucket, Key=s3_key)
    zip_content = response['Body'].read()

    with zipfile.ZipFile(io.BytesIO(zip_content)) as z:

        if 'imagedefinitions.json' in z.namelist():
            with z.open('imagedefinitions.json') as f:
                return f.read()
        else:
            raise FileNotFoundError("imagedefinitions.json not found in artifact.")


def get_image_uri(json_file):
    image_details = json.loads(json_file)
    return image_details[0]['imageUri']


@contextmanager
def codepipeline_job(event):
    job_id = event['CodePipeline.job']['id']
    client = boto3.client('codepipeline')
    try:
        yield
        client.put_job_success_result(jobId=job_id)

    except Exception as e:
        client.put_job_failure_result(
            jobId=job_id,
            failureDetails={
                'type': 'JobFailed',
                'message': str(e)
            }
        )
        raise
