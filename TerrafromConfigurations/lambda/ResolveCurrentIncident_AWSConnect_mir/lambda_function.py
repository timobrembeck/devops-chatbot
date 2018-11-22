import json
import boto3

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

def make_inactive(key):
    ddb = boto3.client('dynamodb')
    
    response = ddb.update_item(
        TableName = 'alert-log',
        Key = {
            'message-id': {
                'S': key
            }
        },
        AttributeUpdates = {
            'active': {
                'Value': {
                    'BOOL': False
                },
                'Action': 'PUT'
            }
        }
    )

    return response


def lambda_handler(event, context):
    counter = get_key_from_ddb('counter')
    current_key = counter['Item']['message']['S']

    make_inactive(current_key)
    
    resultMap = {'incident':'resolved'}
    
    
    return resultMap