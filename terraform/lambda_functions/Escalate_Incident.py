import boto3
import os
import json
from datetime import datetime

def publish_to_connect_sns(payload):
    sns = boto3.client('sns')
    response = sns.publish (
        TargetArn = os.environ['SNS_EIP_NOTIFY_ARN'],
        Message = json.dumps(payload)
    )
    return response


def get_escalation_target_from_ddb(dayToday):
    ddb = boto3.client('dynamodb')

    response = ddb.get_item(
        TableName = 'escalation_target', 
        Key = {
            'dayName': {
                'S': dayToday
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

    dayToday = datetime.now().strftime("%A")
    escalation = get_escalation_target_from_ddb(dayToday)
    escalationTarget = escalation['Item']['escalationTarget']['S']
    escalationNumber = escalation['Item']['escalationNumber']['S']

    print(escalation)

    if 'bot' in event_response:

        message = event_response['currentIntent']['slots']['message']

        payload = {
            'message': message,
            'priority': 'high',
        }        

        publish_to_connect_sns(payload)
            
        print(json.dumps(payload))

        return close(
            {}, 
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': 'The incident with message ' + message + ' has been escalated to ' + escalationTarget
            }
        )

    else:
        message = event_response['Details']['Parameters']['message']
    
        payload = {
            'message': message,
            'priority': 'high',
        }        

        publish_to_connect_sns(payload)
            
        print(json.dumps(payload))

        resultMap = {'escalation': 'The incident with message ' + message + ' has been escalated to ' + escalationTarget + ' with phone number: ' + escalationNumber }

        return resultMap
