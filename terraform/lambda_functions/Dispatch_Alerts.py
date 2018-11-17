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
    escalation = sns_message['escalation']

    if escalation == 'test':
        payload = {
            'message': message,
            'destination_phone_number': '+4915160140655'
        }
    elif escalation == "Alex":
        payload = {
            'message': message,
            'destination_phone_number': '+491725342610'
        }  
    elif escalation == "Brad":
        payload = {
            'message': message,
            'destination_phone_number': '+18643266769'
        }  
    elif escalation == "Michael":
        payload = {
            'message': message,
            'destination_phone_number': '+18645017555'
        }
    else:
        payload = {
            'message': message,
            'destination_phone_number': os.environ['sodPhoneNumber']
        }
        
        
    print(json.dumps(payload))
    publish_to_connect_sns(payload)

    resultMap = {'escalation':'done'}
    
    return resultMap
