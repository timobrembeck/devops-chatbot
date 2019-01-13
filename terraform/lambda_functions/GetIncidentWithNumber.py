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
    event_response = json.loads(json.dumps(event))
    print(event_response)

    counter = get_key_from_ddb('counter')
    current_key = counter['Item']['message']['S']

    message = ""
    if event_response['currentIntent']['slots']['inputNumber'] == None:
        message = 'Total number of esclated incidents are' + current_key
    else:
        inputNumber = event_response['currentIntent']['slots']['inputNumber']
        dataset = get_key_from_ddb(inputNumber)
        containsItem = len(list(dataset))
        if containsItem > 1:
            message = 'The incident with message: ' + dataset['Item']['message']['S'] + ' was escalated to: ' + dataset['Item']['escalationTarget']['S'] + 'and has a status: ' + dataset['Item']['status']['S']
        else:
            message = 'Sorry we could not find any esclated incident for input: ' + inputNumber
            
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