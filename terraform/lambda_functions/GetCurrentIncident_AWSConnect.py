import json
import boto3

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


def lambda_handler(event, context):
    counter = get_key_from_ddb('counter')
    current_key = counter['Item']['message']['S']
    
    dataset = get_key_from_ddb(current_key)
    if dataset['Item']['active']['BOOL']:
        message = dataset['Item']['message']['S']
    else:
        message = 'Currently no active Incident.'
    
    print(json.dumps(message))
    
    resultMap = {"message":message}

    return resultMap