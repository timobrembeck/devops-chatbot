import boto3
import os
import json


def publish_to_connect_sns(payload):
    sns = boto3.client('sns')
    response = sns.publish (
        TargetArn = os.environ['SNS_EIP_NOTIFY_ARN'],
        Message = json.dumps(payload)
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
    
    event_response = json.dumps(event)

    print(event_response)

    if 'bot' in event_response:

        parsed_event = json.loads(event_response)

        escalation_target = parsed_event['currentIntent']['slotDetails']['escalationTarget']['originalValue']
        message = parsed_event['currentIntent']['slotDetails']['message']['originalValue']

        payload = {
            'message': message,
            'priority': 'high',
            'escalation': escalation_target
        }        

        publish_to_connect_sns(payload)
            
        print(json.dumps(payload))

        return close(
            {}, 
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': 'The incident with message ' + message + ' has been escalated to ' + escalation_target
            }
        )

    else:
        escalation_target = event_response['Details']['Parameters']['escalationTarget']
        message = event_response['Details']['Parameters']['message']
    
        payload = {
            'message': message,
            'priority': 'high',
            'escalation': escalation_target
        }        

        publish_to_connect_sns(payload)
            
        print(json.dumps(payload))

        resultMap = {'escalation':'done'}

        return resultMap
