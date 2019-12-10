import os
from botocore.vendored import requests

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

def archive_channel(channel_id):
    return slack_api_call('channels.archive', {'channel': channel_id})

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