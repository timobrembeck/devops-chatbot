import boto3
import os

def update_item_at_Key(key):
    ddb = boto3.client('dynamodb', region_name='eu-west-1')
    response = ddb.update_item(
        TableName = 'alert-log',
        Key= {'messageID': {
                'S': key
                }
            },
        AttributeUpdates={
            "status": {
            "Action": "PUT", 
            "Value": {"S":"pending"}
            } 
        }
    )
    return response
    
def get_count_from_ddb():
    ddb = boto3.client('dynamodb', region_name='eu-west-1')
    response = ddb.scan(
        TableName='alert-log'
    )
    return response
    
def lambda_handler(event, context):
    extractedItemsFromDB = get_count_from_ddb()
    totalNumberOfItemsInDB = len(extractedItemsFromDB['Items']) - 1
    print('key retrieved')
    print(totalNumberOfItemsInDB)
    res = update_item_at_Key(str(totalNumberOfItemsInDB))
    print('update success')
    print(res)
    response = {
        'statusCode': 200
    }
    
    return response