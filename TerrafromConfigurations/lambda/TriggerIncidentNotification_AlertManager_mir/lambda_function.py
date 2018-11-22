import os
import json
import boto3

def publish_to_connect_sns(payload):
    sns = boto3.client('sns')
    response = sns.publish (
        TargetArn = os.environ['SNS_EIP_NOTIFY_ARN'],
        Message = json.dumps(payload)
    )
    return response

def bearer_custom_authentication(bearer_token, received_token):
    authorized = False

    if bearer_token == received_token:
        authorized = True

    return authorized
    
def set_received_token(event):
    if 'Authorization' not in event['headers']:
        print ('[error] Missing authorization token. Sending 403...')
        return
    else:
        received_token = event['headers']['Authorization']  
        return received_token


def lambda_handler(event, context):
    
    print(event)

    bearer_token = 'Bearer ' + os.environ['BearerToken']
    received_token = set_received_token(event)
    
    status = 403

    if bearer_custom_authentication(bearer_token,received_token):
        http_status = 200
        print('[success] Sending 200 OK')
        
        body = json.loads(event['body'])
        common_annotation_summary = body['commonAnnotations']['summary']
        status = body['status']
        region = os.environ['AWS_REGION']
        
        if status == 'firing':
            message = 'AlertManager status ' + status + ', in ' + region + '. ' + common_annotation_summary + '.'

            payload = {
                'message': message,
                'escalation': 'SOD',
                'priority': 'high'
            }
        
            print(json.dumps(payload))
            publish_to_connect_sns(payload)
        
    response = {
        'statusCode': http_status
    }
    
    return response