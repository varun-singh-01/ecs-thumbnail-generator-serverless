import os
import json
import boto3

BASE_URL = 'https://s3.amazonaws.com/'

ecs_client = boto3.client('ecs')


def triggerOnUploadVideo(event, context):
    print("[triggerOnUploadVideo] File Event :: {}".format(event))

    # Process Event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Log the event processing
    print("[triggerOnUploadVideo][Object:Created] New video file {} is recieved for processing...".format(key))

    # Prepare processing details
    s3_video_url = '{}{}'.format(BASE_URL, key)
    thumbnail_file_name = '{}.png'.format(key.split('.')[0])
    frame_pos = '00:02'

    # run an ECS Fargate task
    response = ecs_client.run_task(cluster=os.environ['ECS_CLUSTER_NAME'],
                                   launchType='FARGATE',
                                   taskDefinition=os.environ['ECS_TASK_DEFINITION'],
                                   count=1,
                                   platformVersion='LATEST',
                                   networkConfiguration={
        'awsvpcConfiguration': {
            'subnets': [
                os.environ['ECS_TASK_VPC_SUBNET_1'],
                os.environ['ECS_TASK_VPC_SUBNET_2']
            ],
            'assignPublicIp': 'ENABLED'
        }
    }, overrides={
        'containerOverrides': [
            {
                'name': 'ffmpeg-engine',
                'environment': [
                        {
                            'name': 'INPUT_VIDEO_FILE_URL',
                            'value': s3_video_url
                        },
                    {
                            'name': 'OUTPUT_THUMBS_FILE_NAME',
                            'value': thumbnail_file_name
                    },
                    {
                            'name': 'POSITION_TIME_DURATION',
                            'value': frame_pos
                    },
                    {
                            'name': 'OUTPUT_S3_PATH',
                            'value': os.environ['OUTPUT_S3_PATH']
                    },
                    {
                            'name': 'AWS_REGION',
                            'value': os.environ['OUTPUT_S3_AWS_REGION']
                    }
                ]
            }
        ]
    })

    print("[triggerOnUploadVideo] ECS Task submitted successfully :: {}".format(response))
