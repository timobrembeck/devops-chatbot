import boto3
import json
from boto3.dynamodb.conditions import Attr

def get_incidents_by_status(status):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('alert-log')

    result = table.scan(
        FilterExpression=Attr('currentStatus').eq(status),
        ProjectionExpression="messageID, message, escalationTarget, priority"
    )
    items = result['Items']
    return items


# -- Function to group all incidents by escalation target --
def groupBy_escalationTarget(incidents):
    result = {}
    for incident in incidents:
        if(incident['escalationTarget'] in result):
            result[incident['escalationTarget']].append(incident)
        else:
            result[incident['escalationTarget']] = [incident]
    return result

# -- Function to create the repsonse message --
def create_response_message(escalationTarget):
    message = 'There are ' + str(len(escalationTarget)) + " incidents with status open"  + ': \n'
    incidentIds = []
    for counter, incident in enumerate(escalationTarget):
        message += 'Result ' + str(counter+1) + " is the incident with ID: " + incident['messageID'] + " and message " + incident['message'] + " which has been escalated to " + incident['escalationTarget'] +  " and has a priority " + incident['priority'] +'. \n'
        incidentIds.append(incident['messageID'])
    return message, incidentIds


def get_escalation_target_from_ddb(escalationTargetName):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('escalation_target')

    result = table.scan(
        FilterExpression=Attr('escalationTarget').eq(escalationTargetName),
        ProjectionExpression="escalationNumber"
    )
    escalationNumber = result['Items'][0]['escalationNumber']
    return escalationNumber



def lambda_handler(event, context):
    
    incidents = get_incidents_by_status('open')
    grouppedByEscTarget = groupBy_escalationTarget(incidents)

    connect = boto3.client('connect', region_name='eu-central-1')

    for escalationTarget in grouppedByEscTarget:
        escalationNumber = get_escalation_target_from_ddb(escalationTarget)
        message, incidentIds = create_response_message(grouppedByEscTarget[escalationTarget])
        incidentIds = ', '.join(str(e) for e in incidentIds)
        connect_response = connect.start_outbound_voice_contact(
            InstanceId='736d65e0-6ce5-4210-9d44-55c366ea9a16',
            ContactFlowId='c1a120ab-98fd-4f52-911d-484c442e1a42',
            DestinationPhoneNumber=escalationNumber,
            SourcePhoneNumber='+448081649919',
            Attributes={
                'message': message,
                'incidentIds': incidentIds
            },
        )

        print('The Call to ' + escalationNumber + ' has the message ' + message)

    response = {
        'statusCode': 200
    }
    
    return response