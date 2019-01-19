import boto3
import os
import json
from boto3.dynamodb.conditions import Attr

# -- Function to query the db by the priority property --
def get_incidents_by_priority(priority):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('alert-log')

    result = table.scan(
        FilterExpression=Attr('priority').eq(priority),
        ProjectionExpression="messageID, message, escalationTarget, currentStatus"
    )
    items = result['Items']
    return items
    
# -- Function to create the repsonse message --
def create_response_message(priority, incidents):
    message = 'There are ' + str(len(incidents)) + " incidents with priority " + priority + ': \n'
    
    for counter, incident in enumerate(incidents):
        message += 'Result ' + str(counter+1) + " is the incident with ID: " + incident['messageID'] + " and message " + incident['message'] + " which has been escalated to " + incident['escalationTarget'] + " and has the status " + incident['currentStatus'] + ' \n'

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

        priority = event_response['currentIntent']['slots']['priority']

        incidents = get_incidents_by_priority(priority)

        message = create_response_message(priority, incidents)

        return close(
            {}, 
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': message
            }
        )

    else:
        priority = event_response['Details']['Parameters']['priority']
    
        incidents = get_incidents_by_priority(priority)

        message = create_response_message(priority, incidents)    

        response = {
            'statusCode': 200,
            'message': message
        }
        return response
