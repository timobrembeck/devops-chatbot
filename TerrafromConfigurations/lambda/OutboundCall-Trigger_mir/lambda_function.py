import boto3
import os
import json

def get_key_from_ddb(key):
    ddb = boto3.client('dynamodb')
    
    response = ddb.get_item(
        TableName = 'alert-log', 
        Key = {
            'message-id': {
                'S': key
            }
        }
    )
    
    return response
    
def put_item_on_ddb(key, item):
    ddb = boto3.client('dynamodb')
    
    response = ddb.put_item(
        TableName = 'alert-log',
        Item = {
            'message-id': {
                'S': key
            },
            'message': {
                'S': item
            },
            'active': {
                'BOOL': True
            }
        }
    )
    
    return response
    
def lambda_handler(event, context):
    
    sns_msg = json.loads(event['Records'][0]['Sns']['Message'])
    print(sns_msg)

    message = sns_msg['message']
    destination_phone_number = sns_msg['destination_phone_number']

    print(message)
    print(destination_phone_number)

    counter = get_key_from_ddb('counter')
    current_key = int(counter['Item']['message']['S'])
    next_key = current_key + 1
    
    print(str(next_key))
    
    print(put_item_on_ddb(str(next_key), message))
    print(put_item_on_ddb('counter', str(next_key)))
    

    connect = boto3.client('connect')
    
    response = connect.start_outbound_voice_contact(
        #Attributes={
        #    'message': message
        #},
        ContactFlowId='xxxxx-xxx-xxx-xxxx-xxxxx',
        DestinationPhoneNumber=destination_phone_number,
        InstanceId='xxxxx-xxx-xxx-xxxx-xxxxx',
        SourcePhoneNumber='+1510xxxx'
    )
    
    print('[info] Phone with number: ' + destination_phone_number + ' has been called with message: "' + message + ' "')