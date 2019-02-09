import json
import boto3

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

def create_response_message(item, number):
    doesItemExist = 'Item' in item
    if(doesItemExist):
        message = 'The incident with id' + number + ' has the message: ' + item['Item']['message']['S'] + ' and has been escalated to: ' + item['Item']['escalationTarget']['S']        
        return message
    else:
        message = 'Sorry, there is no incident with id: ' + number
        return message


def lambda_handler(event, context):
    event_response = json.loads(json.dumps(event))
    print(event_response)

    number = event_response['currentIntent']['slots']['inputNumber']
    item = get_key_from_ddb(number)
    message = create_response_message(item, number)
    print(message)
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