import json
import boto3
from boto3.dynamodb.conditions import Key, Attr


def get_key_from_ddb(key):
    ddb = boto3.client('dynamodb')

    response = ddb.get_item(
        TableName='alert-log',
        Key={
            'messageID': {
                'S': key
            }
        }
    )

    return response


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
    table = dynamodb.Table('alert-log')

    result = table.scan(
        FilterExpression=Attr('status').eq('Open'),
        ProjectionExpression="escalationTarget, message"
    )

    message = 'All open incidents: \n'

    for x in result['Items']:
        message += 'Responsible Person: ' + x['escalationTarget'] + '; Message: ' + x['message'] + ' \n'

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