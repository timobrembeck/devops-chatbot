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

def create_response_message(item, number):
    doesItemExist = 'Item' in item
    if(doesItemExist):
        message = 'The incident with id: ' + item['Item']['messageID']['S'] + ' is of ' + item['Item']['priority']['S'] + ' priority, has the status: ' + item['Item']['currentStatus']['S'] +  ' and the message: "' + item['Item']['message'][
        'S'] + '". Responsible specialist on duty is: ' + item['Item']['escalationTarget']['S']      
        return message
    else:
        message = 'Sorry, there is no incident with id ' + number
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
        return close(message)
    else:
        response = {
            'statusCode': 200,
            'message':message
        }

        return response