import boto3
import json
from datetime import datetime

dynamodb = boto3.client('dynamodb')

def get_counter():
    response = dynamodb.get_item(
        TableName = 'alert-log', 
        Key = {
            'messageID': {
                'S': 'counter'
            }
        }
    )
    return int(response['Item']['message']['S'])

def set_counter(counter):
    response = dynamodb.put_item(
        TableName = 'alert-log',
        Item = {
            'messageID': {
                'S': 'counter'
            },
            'message': {
                'S': counter
            }
        }
    )
    return response

def get_escalation_target():
    response = dynamodb.get_item(
        TableName = 'escalation_target', 
        Key = {
            'responsibility': {
                'S': datetime.now().strftime("%A")
            }
        }
    )
    escalationTarget = {
        'name': response['Item']['escalationTarget']['S'],
        'number': response['Item']['escalationNumber']['S'],
        'team': response['Item']['escalationTeam']['S']
    }
    return escalationTarget
    
def save_incident(incident):
    response = dynamodb.put_item(
        TableName = 'alert-log',
        Item = {
            'messageID': {
                'S': incident['id']
            },
            'message': {
                'S': incident['message']
            },
            'priority': {
                'S': incident['priority']
            },
            'currentStatus': {
                'S': 'open'
            },
            'timestamp': {
                'S': incident['timestamp']
            },
            'escalationTarget': {
                'S': incident['escalationTarget']
            }
        }
    )
    return response

def contact_escalation_target(escalationTarget, incident):
    lambda_client = boto3.client('lambda')
    response = lambda_client.invoke(
        FunctionName='arn:aws:lambda:eu-west-1:746022503515:function:Contact_Escalation_Target',
        InvocationType='Event',
        Payload=bytes(json.dumps({
            'escalationTarget': escalationTarget,
            'incident': incident
        }), "utf-8")
    )
    return response

def lambda_handler(event, context):
    
    sns_msg = json.loads(event['Records'][0]['Sns']['Message'])
    print(sns_msg)

    new_counter = str(get_counter() + 1)

    escalationTarget = get_escalation_target()

    incident = {
        'id': new_counter,
        'timestamp': str(datetime.now().timestamp()),
        'priority': sns_msg['priority'],
        'message': sns_msg['message'],
        'escalationTarget': escalationTarget['name']
    }

    save_incident(incident)
    set_counter(new_counter)

    contact_escalation_target(escalationTarget, incident)

    print('[info] Escalation target ' +  escalationTarget['name'] + ' with phone number: ' + escalationTarget['number'] + ' has been called with message: "' + incident['message'] + ' "')

    return { 'statusCode': 200 }