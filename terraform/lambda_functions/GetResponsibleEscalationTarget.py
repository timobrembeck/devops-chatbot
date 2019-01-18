import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
import datetime
from datetime import date

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
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('escalation_target')

    weekday = datetime.datetime.today().strftime('%A')

    result = table.scan(
        FilterExpression=Attr('dayName').eq(weekday),
        ProjectionExpression="escalationNumber, escalationTarget"
    )

    message = 'The responsible persons are: \n'

    for x in result['Items']:
        message += 'Responsible Person: ' + x['escalationTarget'] + ' with the number: ' + x['escalationNumber'] + ' \n'

    print(message)



    event_response = json.dumps(event)

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