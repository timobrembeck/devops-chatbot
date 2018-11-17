import boto3
import os
import json


def publish_to_connect_sns(payload):
    sns = boto3.client('sns')
    response = sns.publish (
        TargetArn = os.environ['SNS_EIP_NOTIFY_ARN'],
        Message = json.dumps(payload)
    )
    return response


def lambda_handler(event, context):
    
    print(json.dumps(event))
    
    escalation_target = event['Details']['Parameters']['escalationTarget']
    message = event['Details']['Parameters']['message']
    
    print(json.dumps(escalation_target))
    
    payload = {
        'message': message,
        'priority': 'high',
        'escalation': escalation_target
    }        
    
    publish_to_connect_sns(payload)
        
    print(json.dumps(payload))
    
    
    resultMap = {'escalation':'done'}
    
    return resultMap
