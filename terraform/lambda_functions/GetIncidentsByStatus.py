import boto3
import os
import json
from boto3.dynamodb.conditions import Attr

# -- Function to query the db by the status property --
def get_incidents_by_status(status):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('alert-log')

    result = table.scan(
        FilterExpression=Attr('currentStatus').eq(status),
        ProjectionExpression="messageID, message, escalationTarget, priority"
    )
    items = result['Items']
    return items

# -- Function to create the response message --
def create_response_message(status, incidents):
    if len(incidents)==0:
        message = 'There are no incidents with status ' + status
        return message

    elif len(incidents)>6:
        message = 'There are ' + str(len(incidents)) + " incidents with status " + status + '. The IDs of the incidents are the following.'

        for counter, incident in enumerate(incidents):
            message += incident['messageID'] + ', '

        message += 'In order to get more information about an incident, say get incident with id and then the id of the incident.'
        return message

    elif len(incidents)>30:
        message = 'There are ' + str(len(incidents)) + " incidents with status " + status + '. In order to get more information about an incident, say get incident with id and then the id of the incident.'
        return message

    else:
        message = 'There are ' + str(len(incidents)) + " incidents with status " + status + '. '

        for counter, incident in enumerate(incidents):
            message += 'Result ' + str(counter+1) + " is the incident with ID: " + incident['messageID'] + " and message " + incident['message'] + " which has been escalated to " + incident['escalationTarget'] +  " and has a priority " + incident['priority'] + '. '

        return message

# -- AWS Lex Bot Intent response --
def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response

def lambda_handler(event, context):
    
    event_response = json.loads(json.dumps(event))

    print(event_response)

    if 'bot' in event_response:

        status = event_response['currentIntent']['slots']['status']

        incidents = get_incidents_by_status(status)

        message = create_response_message(status, incidents)

        return close(
            {}, 
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': message
            }
        )

    else:
        status = event_response['Details']['Parameters']['status']
    
        incidents = get_incidents_by_status(status)

        message = create_response_message(status, incidents)    

        response = {
            'statusCode': 200,
            'message': message
        }
        return response
