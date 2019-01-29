import boto3
import os
import json

def update_item_at_Key(incidentId, status):
    ddb = boto3.client('dynamodb', region_name='eu-west-1')
    response = ddb.update_item(
        TableName = 'alert-log',
        Key= {
            'messageID': {
                'S': incidentId
                }
            },
        AttributeUpdates={
            "currentStatus": {
                "Action": "PUT", 
                "Value": {
                    "S": status
                }
            } 
        }
    )
    return response

def get_item_from_ddb(key):
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

    event_response = json.loads(json.dumps(event))

    print(event_response)

    incidentIds = event_response['Details']['ContactData']['Attributes']['incidentIds']
    incidentIds = [x.strip() for x in incidentIds.split(',')]
    message = 'There are ' + str(len(incidentIds)) + " incidents with status to be updated"  + ': \n'
    
    for incidentId in incidentIds :
        item = get_item_from_ddb(str(incidentId))
        doesItemExist = 'Item' in item

        if(doesItemExist): 
                print('Item with id ' + incidentId + ' exist')
                update_item_at_Key(str(incidentId), 'pending')
                message += 'The status of the incident with ID ' + str(incidentId) + ', has been updated to pending'  +'. \n'
        else:
            return {
                    'statusCode': 400,
                    'message': 'Wrong input! Incident with ID ' + str(incidentId) + ' does not exist.'
            }

    print(message)

    response = {
        'statusCode': 200,
        'message': message
    }
    return response