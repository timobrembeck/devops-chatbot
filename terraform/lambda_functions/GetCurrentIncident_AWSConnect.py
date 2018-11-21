import json
import boto3

def get_key_from_ddb(key):
    ddb = boto3.client('dynamodb')
    
    response = ddb.get_item(
        TableName = 'alert-log', 
        Key = {
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
    counter = get_key_from_ddb('counter')
    current_key = counter['Item']['message']['S']
    
    dataset = get_key_from_ddb(current_key)
    if dataset['Item']['active']['BOOL']:
        message = dataset['Item']['message']['S']
    else:
        message = 'Currently no active Incident.'
    
    print(json.dumps(message))

    event_response = json.dumps(event)

    #Check if lambda is called from AWS Lex
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
            'message':message
        }

        return response
