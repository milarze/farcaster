"""
Python Lambda entry point
"""

import datetime
import os
import boto3


def queue_farcaster(event, context):
    """
    Handler function to add a farcaster task
    """
    try:
        payload = event['body']
        request_id = vars(context)['aws_request_id']
        runner = os.getenv('RUNNER')
        subnet = os.getenv('SUBNET')
        s3_bucket = os.getenv('S3_BUCKET')
        cluster = os.getenv('CLUSTER_NAME')

        now = datetime.datetime.now()
        expires = now + datetime.timedelta(hours=2)


        s3_client = boto3.client('s3')
        s3_client.put_object(Body=payload, Expires=expires, Bucket=s3_bucket, Key=request_id + '/input.json')

        ecs_client = boto3.client('ecs')
        ecs_client.run_task(
            cluster=cluster,
            taskDefinition=runner,
            launchType='FARGATE',
            networkConfiguration={
                'awsvpcConfiguration': {
                    'subnets': [subnet],
                    'assignPublicIp': 'ENABLED'
                }
            },
            overrides={
                'containerOverrides': [
                    {
                        'environment': [
                            {
                                'name': 'INPUT_JSON_KEY',
                                'value': request_id + '/input.json'
                            },
                            {
                                'name': 'S3_BUCKET',
                                'value': s3_bucket
                            }
                        ],
                        'name': runner
                    }
                ]
            }
        )

        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"message":"Task queued"}'
        }
    except Exception as err: # pylint: disable=broad-except
        print(str(err))
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"message":"Internal server error"}'
        }
