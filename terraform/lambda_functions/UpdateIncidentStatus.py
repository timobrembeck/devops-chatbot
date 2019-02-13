import boto3
import json
from boto3.dynamodb.conditions import Attr

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

def get_incident(incidentId):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('alert-log')
    result = table.scan(
        FilterExpression=Attr('messageID').eq(incidentId),
        ProjectionExpression="messageID, message"
    )
    if result['Items'] and len(result['Items'])==1:
        return True
    return False


# -- AWS Lex Bot Intent response --
def close(message):
    response = {
        'sessionAttributes': {},
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': 'Fulfilled',
            'message': {
                'contentType': 'PlainText',
                'content': message
            }
        }
    }
    return response
    
def lambda_handler(event, context):

    event_response = json.loads(json.dumps(event))

    print(event_response)

    incidentId = event_response['currentIntent']['slots']['incidentId']
    status = ''

    if 'CloseIncidentIntent' in event_response['currentIntent']['name'] :
        status = 'closed'
    else:
        status = event_response['currentIntent']['slots']['status']

    incident = get_incident(incidentId)
    if incident is False:
        message = 'There is not incident with id ' + incidentId
        return close(message)

    if status not in ["open", "pending", "closed"]:
        message = 'The status of the incident has to be open, pending or closed. ' + status + ' is not correct.'
        return close(message)
        
    update_item_at_Key(str(incidentId), status)
    message = 'The status of the incident with id ' + str(incidentId) + ' has been updated to ' + status
    print(message)
    return close(message)
           

