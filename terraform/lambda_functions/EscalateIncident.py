import boto3
import json
from boto3.dynamodb.conditions import Attr
dynamodb = boto3.resource('dynamodb')

def get_escalation_target(escalationTargetName):
    table = dynamodb.Table('escalation_target')

    result = table.scan(
        FilterExpression=Attr('escalationTarget').eq(escalationTargetName),
        ProjectionExpression="escalationNumber, escalationTarget, escalationTeam"
    )

    if result['Items'] and len(result['Items'])==1:
        escalationTarget = {
            'name': result['Items'][0]['escalationTarget'],
            'number': result['Items'][0]['escalationNumber'],
            'team': result['Items'][0]['escalationTeam']
        }
        return escalationTarget
    return False

def get_incident(incidentId):
    table = dynamodb.Table('alert-log')

    result = table.scan(
        FilterExpression=Attr('messageID').eq(incidentId),
        ProjectionExpression="messageID, message"
    )

    if result['Items'] and len(result['Items'])==1:
        incident = {
            'id': result['Items'][0]['messageID'],
            'message': result['Items'][0]['message']
        }
        return incident
    return False

def contact_escalation_target(escalationTarget, incident):
    lambda_client = boto3.client('lambda')
    response = lambda_client.invoke(
        FunctionName='arn:aws:lambda:eu-west-1:746022503515:function:Contact_Escalation_Target',
        InvocationType='Event',
        Payload=bytes(json.dumps({
            'escalationTarget': escalationTarget,
            'incident': incident
        }), "utf-8")
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

def lambda_handler(event, context):
    
    event_response = json.loads(json.dumps(event))
    print(event_response)
   
    incidentId = event_response['currentIntent']['slots']['incidentId']
    escalationTargetName = event_response['currentIntent']['slots']['escalationTarget']

    incident = get_incident(incidentId)
    escalationTarget = get_escalation_target(escalationTargetName)

    if incident is False:
        message = 'There is not incident with id ' + incidentId
        return close(message)
    
    if escalationTarget is False:
        message = 'There is not escalation target with name ' + escalationTargetName
        return close(message)

    print(escalationTarget)
    print(incident)
    contact_escalation_target(escalationTarget, incident)

    message = 'The incident with id ' + str(incidentId) + ' has been escalated to ' + escalationTarget['name']
    return close(message)


    

