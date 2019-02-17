import boto3
from Slack_Lambda_Layer import *

bot_user_id = 'UECS2J05D'

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
    if 'Item' in response:
        return response['Item']
    return False

def get_users_from_ddb(team):
    ddb = boto3.client('dynamodb')
    users = ddb.scan(
        TableName = 'user',
        ScanFilter = {
            'teams': {
                'AttributeValueList': [{'S': team.lower()}],
                'ComparisonOperator': 'CONTAINS'
            }
        }
    )
    return users['Items']

def result(result_type, content, args = {}):
        result = {
            'sessionAttributes': {},
            'dialogAction': {
                'type': result_type,
                'message': {
                    'contentType': 'PlainText',
                    'content': content
                }
            }
        }
        if result_type == 'Close':
            result['dialogAction']['fulfillmentState'] = args['fulfillmentState']
        elif result_type == 'ElicitSlot':
            result['dialogAction']['intentName'] = 'CreateSlackChannelIntent'
            result['dialogAction']['slots'] = args['slots']
            result['dialogAction']['slotToElicit'] = args['slotToElicit']
        return result


def lambda_handler(event, context):

    team = event['currentIntent']['slots']['team']
    incidentId = event['currentIntent']['slots']['incidentId']
    incident = get_key_from_ddb(incidentId)
    if not incident:
        return result('ElicitSlot', 'There is no incident with id "' + str(incidentId) + '". Please try another one.', {'slots': {'team': team, 'incidentId': incidentId}, 'slotToElicit': 'incidentId'})
    channel_name = 'incident_' + incident['messageID']['S']
    message = ''
    try:
        channel = create_channel(channel_name)
        try:
            invite_to_channel(channel['id'], bot_user_id)
        except SlackException as e:
            if e.error in ['already_in_channel', 'user_not_found', 'cant_invite_self']:
                pass
            else:
                return result('Failed', 'The method "' + e.method + '" failed with error "' + e.error + '"')
        set_channel_topic(channel['id'], 'Incident message: ' + incident['message']['S'])
        set_channel_purpose(channel['id'], 'Resolving incident with message: ' + incident['message']['S'])
        post_message(channel['id'], 'I created this channel for you to handle the incident with the message: "' + incident['message']['S'] + '".\n\nLet\'s resolve this issue as fast as possible! :rocket:')
        message += 'The Slack channel "' + channel_name + '" has been created. '
    except SlackException as e:
        if e.error == 'name_taken':
            channel = [c for c in get_channels() if c['name'] == channel_name][0]
            if channel['is_archived']:
                unarchive_channel(channel['id'])
                message += 'The Slack channel "' + channel_name + '" has been unarchived. '
                try:
                    invite_to_channel(channel['id'], bot_user_id)
                except SlackException as e:
                    if e.error in ['already_in_channel', 'user_not_found', 'cant_invite_self']:
                        pass
                    else:
                        return result('Failed', 'The method "' + e.method + '" failed with error "' + e.error + '"')
            join_channel(channel_name)
        else:
            return result('Close', 'The method "' + e.method + '" failed with error "' + e.error + '"', {'fulfillmentState': 'Failed'})

    users = get_users_from_ddb(team)
    if len(users) == 0:
        return result('ElicitSlot', 'The team "' + team + '" could not be found. Please try another one.', {'slots': {'team': team, 'incidentId': incidentId}, 'slotToElicit': 'team'})

    for user in users:
        try:
            invite_to_channel(channel['id'], user['slackUserID']['S'])
        except SlackException as e:
            if e.error in ['already_in_channel', 'user_not_found', 'cant_invite_self']:
                pass
            else:
                return result('Failed', 'The method "' + e.method + '" failed with error "' + e.error + '"')
    message += 'The team "' + team + '" has been invited to the channel. '
    post_message(channel['id'], 'Welcome, team ' + team + '! :wave:')
    if 'bot' in event:
        return result('Close', message, {'fulfillmentState': 'Fulfilled'})
    else:
        return {'channel_creation': message}
