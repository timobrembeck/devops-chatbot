import boto3
import os
import json
from datetime import datetime

def get_key_from_ddb(key):
    ddb = boto3.client('dynamodb')
    
    response = ddb.get_item(
        TableName = 'alert-log', 
        Key = {
            'messageID': {
                'S': key
            }
        }
    )
    
    return response

def get_escalation_target_from_ddb(dayToday):
    ddb = boto3.client('dynamodb')

    response = ddb.get_item(
        TableName = 'escalation_target', 
        Key = {
            'dayName': {
                'S': dayToday
            }
        }
    )
    
    return response
    
def put_item_on_ddb(key, item, priority, timestamp, target):
    ddb = boto3.client('dynamodb')
    
    response = ddb.put_item(
        TableName = 'alert-log',
        Item = {
            'messageID': {
                'S': key
            },
            'message': {
                'S': item
            },
            'priority': {
                'S': priority
            },
            'status': {
                'S': 'Open'
            },
            'timestamp': {
                'S': timestamp
            },
            'escalationTarget': {
                'S': target
            }
        }
    )
    
    return response


    
def increase_counter_on_ddb(key, item):
    ddb = boto3.client('dynamodb')
    
    response = ddb.put_item(
        TableName = 'alert-log',
        Item = {
            'messageID': {
                'S': key
            },
            'message': {
                'S': item
            }
        }
    )
    
    return response
    
def lambda_handler(event, context):
    
    sns_msg = json.loads(event['Records'][0]['Sns']['Message'])
    print(sns_msg)

    message = sns_msg['message']
    priority = sns_msg['priority']
    timestamp = str(datetime.now().timestamp())

    counter = get_key_from_ddb('counter')
    current_key = int(counter['Item']['message']['S'])
    next_key = current_key + 1

    dayToday = datetime.now().strftime("%A")
    escalation = get_escalation_target_from_ddb(dayToday)
    escalationTarget = escalation['Item']['escalationTarget']['S']
    escalationNumber = escalation['Item']['escalationNumber']['S']

    put_item_on_ddb(str(next_key), message, priority, timestamp, escalationTarget)
    increase_counter_on_ddb('counter', str(next_key))

    connect = boto3.client('connect', region_name='eu-central-1')
    connect_response = connect.start_outbound_voice_contact(
        InstanceId='736d65e0-6ce5-4210-9d44-55c366ea9a16',
        ContactFlowId='c1a120ab-98fd-4f52-911d-484c442e1a42',
        DestinationPhoneNumber=escalationNumber,
        SourcePhoneNumber='+448081649919',
        Attributes={
           'message': message
        },
    )

    print('[info] Escalation target ' +  escalationTarget + ' with phone number: ' + escalationNumber + ' has been called with message: "' + message + ' "')

    response = {
        'statusCode': 200
    }
    
    return response