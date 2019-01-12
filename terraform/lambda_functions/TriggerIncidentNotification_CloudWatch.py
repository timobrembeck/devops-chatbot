import json
import os
import boto3


def publish_to_connect_sns(payload):
    sns = boto3.client('sns')
    response = sns.publish (
        TargetArn = os.environ['SNS_EIP_NOTIFY_ARN'],
        Message = json.dumps(payload)
    )
    return response

def lambda_handler(event, context):
    event_msg = json.loads(event['Records'][0]['Sns']['Message'])
    
    print(json.dumps(event_msg))


    description = event_msg['description']
    priority = event_msg['priority']
    region = os.environ['AWS_REGION']

    message = 'CloudWatch Alarm with description: ' + description + ', in ' + region + '.'

    payload = {
        'message': message,
        'priority': priority,
    }
    
    print(json.dumps(payload))
    
    publish_to_connect_sns(payload)

    response = {
        'statusCode': 200
    }
    
    return response
    
    