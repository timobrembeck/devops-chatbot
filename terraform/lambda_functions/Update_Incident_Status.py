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

    incidentId = str(event_response['Details']['Parameters']['incidentId'])
    status = event_response['Details']['Parameters']['status']

    item = get_item_from_ddb(incidentId)
    doesItemExist = 'Item' in item

    if(doesItemExist): 
        if( (status == "open") | (status == "pending") | (status == "closed") ):

            update_item_at_Key(incidentId, status)

            message ='If there is incident with ID ' + incidentId + ', the status of the incident has been updated to ' + status

            print(message)

            response = {
                'statusCode': 200,
                'message': message
            }
            return response

        else:
            return {
                'statusCode': 400,
                'message': 'Wrong input! Status of the incident can be either open, pending or closed'
            }
    else:
        return {
                'statusCode': 400,
                'message': 'Wrong input! Incident with ID ' + incidentId + ' does not exist.'
        }