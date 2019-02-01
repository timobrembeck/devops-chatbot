import boto3
import os
from botocore.vendored import requests
import json
import sys
from datetime import datetime

class SlackException(Exception):
    def __init__(self, method, error):
        self.method = method
        self.error = error

def slack_api_call(method, payload = {}):
    payload['token'] = os.environ['token']
    response = requests.post('https://slack.com/api/' + method, data=payload).json()
    if not response['ok']:
        raise SlackException(method, response['error'])
    return response

def join_channel(channel_name):
    return slack_api_call('channels.join', {'name': channel_name})['channel']

def get_channels():
    return slack_api_call('channels.list')['channels']

def create_channel(channel_name):
    return slack_api_call('channels.create', {'name': channel_name})['channel']

def unarchive_channel(channel_id):
    return slack_api_call('channels.unarchive', {'channel': channel_id})

def set_channel_topic(channel_id, channel_topic):
    return slack_api_call('channels.setTopic', {'channel': channel_id, 'topic': channel_topic})

def set_channel_purpose(channel_id, channel_purpose):
    return slack_api_call('channels.setPurpose', {'channel': channel_id, 'purpose': channel_purpose})

def invite_to_channel(channel_id, user_id):
    return slack_api_call('channels.invite', {'channel': channel_id, 'user': user_id})['channel']

def post_message(channel_id, text):
    return slack_api_call('chat.postMessage', {'channel': channel_id, 'text': text})['message']

def get_current_incident_from_ddb():
    ddb = boto3.client('dynamodb')
    counter = ddb.get_item(
        TableName = 'alert-log',
        Key = {
            'messageID': {
                'S': 'counter'
            }
        }
    )['Item']['message']['S']
    incident = ddb.get_item(
        TableName = 'alert-log',
        Key = {
            'messageID': {
                'S': counter
            }
        }
    )
    return incident['Item']

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

def result(result_type, content, args):
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
            result['dialogAction']['slots'] = {
                'team': args['team']
            }
            result['dialogAction']['slotToElicit'] = 'team'
        return result


def lambda_handler(event, context):

    team = event['currentIntent']['slots']['team']
    incident = get_current_incident_from_ddb()
    channel_name = 'incident_' + incident['messageID']['S']
    message = ''
    try:
        channel = create_channel(channel_name)
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
                join_channel(channel_name)
        else:
            return result('Close', 'The method "' + e.method + '" failed with error "' + e.error + '"', {'fulfillmentState': 'Failed'})

    users = get_users_from_ddb(team)
    if len(users) == 0:
        return result('ElicitSlot', 'The team "' + team + '" could not be found. Please try another one.', {'team': team})

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
