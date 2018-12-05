import boto3
import json
import os

def publish_to_connect_sns(payload):
    sns = boto3.client('sns')
    response = sns.publish (
        TargetArn = os.environ['SNS_EIP_NOTIFY_ARN'],
        Message = json.dumps(payload)
    )
    return response

def lambda_handler(event, context):
    print(json.dumps(event))
    
    sns_message = json.loads(event['Records'][0]['Sns']['Message']) 
    
    message = sns_message['message']
    priority = sns_message['priority']

    payload = {
        'message': message,
        'priority': 'high'
    }
 
    print(json.dumps(payload))
    publish_to_connect_sns(payload)

    resultMap = {'escalation':'done'}
    
    return resultMap
