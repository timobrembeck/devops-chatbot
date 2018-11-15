import boto3
import json


def publish_to_connect_sns(payload, topic):
    sns = boto3.client('sns')
    response = sns.publish (
        TargetArn = topic,
        Message = json.dumps(payload)
    )
    return response


def lambda_handler(event, context):
    #sns_message = json.loads(event['Records'][0]['Sns']['Message']) 
    
    print(json.dumps(event))
    
    escalation_target = event['Details']['Parameters']['escalationTarget']
    message = event['Details']['Parameters']['message']
    
    print(json.dumps(escalation_target))
    
    payload = {
        'message': message,
        'priority': 'high',
        'escalation': escalation_target
    }        
    
    publish_to_connect_sns(payload, 'arn:aws:sns:eu-central-1:583726959404:alert_dispatcher')
        
    print(json.dumps(payload))
    
    
    resultMap = {'escalation':'done'}
    
    return resultMap
