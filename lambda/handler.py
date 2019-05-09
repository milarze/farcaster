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
        table_name = os.getenv('TABLE_NAME')

        dynamodb_client = boto3.client('dynamodb')
        dynamodb_client.put_item(
            TableName=table_name,
            Item={
                'request_id': {
                    'S': request_id
                },
                'data': {
                    'S': payload
                }
            }
        )

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
                                'name': 'REQUEST_ID',
                                'value': request_id
                            },
                            {
                                'name': 'TABLE_NAME',
                                'value': table_name
                            },
                            {
                                'name': 'MODEL',
                                'value': 'prophet'
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
