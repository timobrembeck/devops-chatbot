import boto3
import json
from boto3.dynamodb.conditions import Attr
from Slack_Lambda_Layer import *

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
        ProjectionExpression="messageID, currentStatus"
    )
    if result['Items'] and len(result['Items'])==1:
        return result['Items'][0]
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
    if not incident:
        message = 'There is not incident with id ' + str(incidentId)
        return close(message)

    if status not in ["open", "pending", "closed"]:
        message = 'The status of the incident has to be open, pending or closed. ' + status + ' is not correct.'
        return close(message)

    if incident['currentStatus'] == status:
        message = 'The status of the incident with id ' + str(incidentId) + ' is already ' + status
        return close(message)

    update_item_at_Key(str(incidentId), status)
    message = 'The status of the incident with id ' + str(incidentId) + ' has been updated to ' + status
    print(message)

    if 'closed' in [incident['currentStatus'], status]:
        channel = [c for c in get_channels() if c['name'] == 'incident_' + str(incidentId)][0]
        try:
            if status == 'closed':
                post_message(channel['id'], 'Well done! :clap::clap::clap: The incident with the id: ' + str(incidentId) + ' is resolved. :tada:\n\nThere is no need for this channel anymore, so I will archive it.')
                archive_channel(channel['id'])
            else:
                unarchive_channel(channel['id'])
                post_message(channel['id'], 'The incident with the id: ' + str(incidentId) + ' has been re-opened, so I unarchived this channel for you.')
        except SlackException as e:
            if e.error in ['channel_not_found', 'already_archived', 'not_archived']:
                pass
            else:
                return close('The method "' + e.method + '" failed with error "' + e.error + '"')

    return close(message)
           

