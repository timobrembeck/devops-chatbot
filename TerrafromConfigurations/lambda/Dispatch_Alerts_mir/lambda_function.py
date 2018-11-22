import boto3
import json
import os

def publish_to_connect_sns(payload, topic):
    sns = boto3.client('sns')
    response = sns.publish (
        TargetArn = topic,
        Message = json.dumps(payload)
    )
    return response


def lambda_handler(event, context):
    print(json.dumps(event))
    
    sns_message = json.loads(event['Records'][0]['Sns']['Message']) 
    
    message = sns_message['message']
    priority = sns_message['priority']
    escalation = sns_message['escalation']

    if escalation == 'test':
        payload = {
            'message': message,
            'destination_phone_number': '+49151xxxx'
        }
    elif escalation == "Alex":
        payload = {
            'message': message,
            'destination_phone_number': '+49172xxxx'
        }  
    elif escalation == "Brad":
        payload = {
            'message': message,
            'destination_phone_number': '+1864xxxx'
        }  
    elif escalation == "Michael":
        payload = {
            'message': message,
            'destination_phone_number': '+1864xxxx'
        }
    else:
        payload = {
            'message': message,
            'destination_phone_number': os.environ['sodPhoneNumber']
        }
        
        
    print(json.dumps(payload))
    publish_to_connect_sns(payload, 'arn:aws:sns:eu-central-1:xxxx:alert_to_awsconnect')

    resultMap = {'escalation':'done'}
    
    return resultMap
