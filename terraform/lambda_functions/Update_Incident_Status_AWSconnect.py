import boto3
import os

def update_item_at_Key(key):
    ddb = boto3.client('dynamodb', region_name='eu-west-1')
    response = ddb.update_item(
        TableName = 'alert-log',
        Key= {
            'messageID': {
                'S': key
                }
            },
        AttributeUpdates={
            "currentStatus": {
                "Action": "PUT", 
                "Value": {
                    "S":"pending"
                }
            } 
        }
    )
    return response
    

def get_key_from_ddb(key):
    ddb = boto3.client('dynamodb', region_name='eu-west-1')
    response = ddb.get_item(
        TableName = 'alert-log', 
        Key = {
            'messageID': {
                'S': key
            }
        }
    )
    return response
    
def lambda_handler(event, context):
    counter = get_key_from_ddb('counter')
    current_key = counter['Item']['message']['S']
    updateResponse = update_item_at_Key(current_key)
    print('The status of the item with ID ' + current_key + ' has been updated to Pending')
    response = {
        'statusCode': 200
    }
    return response