import boto3
import time
from Slack_Lambda_Layer import *
dynamodb = boto3.client('dynamodb')
bot_user_id = 'TDP6AJ71V'

def trigger_outbound_call(escalation_target, incident):
    connect = boto3.client('connect', region_name='eu-central-1')
    response = connect.start_outbound_voice_contact(
        InstanceId = '736d65e0-6ce5-4210-9d44-55c366ea9a16',
        ContactFlowId = 'c1a120ab-98fd-4f52-911d-484c442e1a42',
        DestinationPhoneNumber = escalation_target['number'],
        SourcePhoneNumber = '+448081649919',
        Attributes = {
            'message': incident['message'],
            'escalationTargetName': escalation_target['name'],
            'incidentIds': incident['id']
        },
    )
    return response

def get_users_from_ddb(team):
    users = dynamodb.scan(
        TableName = 'user',
        ScanFilter = {
            'teams': {
                'AttributeValueList': [{'S': team.lower()}],
                'ComparisonOperator': 'CONTAINS'
            }
        }
    )
    return users['Items']

def get_incident_status(id):
    response = dynamodb.get_item(
        TableName = 'alert-log',
        Key = {
            'messageID': {
                'S': id
            }
        }
    )
    return response['Item']['currentStatus']['S']

def get_backup_escalation_target_from_ddb(responsibility):
    response = dynamodb.get_item(
        TableName = 'escalation_target', 
        Key = {
            'responsibility': {
                'S': responsibility
            }
        }
    )
    backupEscalationTarget = {
        'name': response['Item']['escalationTarget']['S'],
        'number': response['Item']['escalationNumber']['S'],
        'team': response['Item']['escalationTeam']['S']
    }
    return backupEscalationTarget

def lambda_handler(event, context):
    escalationTarget = event['escalationTarget']
    incident = event['incident']

    # first contact attempt (phone)
    trigger_outbound_call(escalationTarget, incident)
    time.sleep(60)

    # second contact attempt (phone)
    if get_incident_status(incident['id']) == 'open':
        backupEscalationTarget = get_backup_escalation_target_from_ddb('IncidentManager')
        trigger_outbound_call(backupEscalationTarget, incident)
        time.sleep(60)

        # third contact attempt (slack)
        if get_incident_status(incident['id']) == 'open':
            channel_name = 'incident_' + incident['id']
            try:
                channel = create_channel(channel_name)
                try:
                    invite_to_channel(channel['id'], bot_user_id)
                except SlackException as e:
                    if e.error in ['already_in_channel', 'user_not_found', 'cant_invite_self']:
                        pass
                    else:
                        return result('Failed', 'The method "' + e.method + '" failed with error "' + e.error + '"')
                set_channel_topic(channel['id'], 'Incident message: ' + incident['message'])
                set_channel_purpose(channel['id'], 'Resolving incident with message: ' + incident['message'])
                post_message(channel['id'], 'I created this channel for you to handle the incident with the message: "' + incident['message'] + '".\n\nLet\'s resolve this issue as fast as possible! :rocket:')
            except SlackException as e:
                if e.error == 'name_taken':
                    channel = [c for c in get_channels() if c['name'] == channel_name][0]
                    if channel['is_archived']:
                        unarchive_channel(channel['id'])
                        try:
                            invite_to_channel(channel['id'], bot_user_id)
                        except SlackException as e:
                            if e.error in ['already_in_channel', 'user_not_found', 'cant_invite_self']:
                                pass
                            else:
                                return result('Failed', 'The method "' + e.method + '" failed with error "' + e.error + '"')
                    join_channel(channel_name)
            users = get_users_from_ddb(escalationTarget['team'])
            if len(users) == 0:
                return { 'statusCode': 500 }
            for user in users:
                try:
                    invite_to_channel(channel['id'], user['slackUserID']['S'])
                except SlackException as e:
                    if e.error in ['already_in_channel', 'user_not_found', 'cant_invite_self']:
                        pass
                    else:
                        return {'statusCode': 500, 'error': 'The method "' + e.method + '" failed with error "' + e.error + '"'}
            post_message(channel['id'], 'Welcome, team ' + escalationTarget['team'] + '! :wave:')

    return { 'statusCode': 200 }