import json


def triggerOnUploadVideo(event, context):
    print("[triggerOnUploadVideo] File Event :: {}".format(event))
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
