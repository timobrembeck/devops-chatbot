import json
import boto3
from datetime import datetime
dynamodb = boto3.client('dynamodb')

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

def get_escalation_target():
    response = dynamodb.get_item(
        TableName = 'escalation_target', 
        Key = {
            'responsibility': {
                'S': datetime.now().strftime("%A")
            }
        }
    )
    escalationTarget = {
        'name': response['Item']['escalationTarget']['S'],
        'number': response['Item']['escalationNumber']['S'],
        'team': response['Item']['escalationTeam']['S']
    }
    return escalationTarget

def lambda_handler(event, context):
    event_response = json.dumps(event)

    escalationTarget = get_escalation_target()

    message = 'The responsible person is ' + escalationTarget['name'] + ' with the number: ' + escalationTarget['number']

    print(message)

    # Check if lambda is called from AWS Lex
    if 'bot' in event_response:
        return close(
            {},
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': message
            }
        )
    else:
        response = {
            'statusCode': 200,
            'message': message
        }

        return response