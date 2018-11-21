import os
import boto3
import json
import fnmatch
import random
import string
"""
Global Information
"""

lex = boto3.client('lex-models', region_name='eu-west-1')
lambda_client = boto3.client('lambda', region_name='eu-west-1')
rootdir = cwd = os.getcwd()


"""
Add permissions to intents, in order to trigger Lambda functions
"""
def add_permission(function_name):
    response = lambda_client.add_permission(
        FunctionName='arn:aws:lambda:eu-west-1:746022503515:function:' + function_name,
        StatementId='add-invoke-permission_' + ''.join(random.choice(string.hexdigits) for i in range(1, 20)),
        Action='lambda:InvokeFunction',
        Principal='lex.amazonaws.com',
    )
    print('Adding permission to intent')
    print(response)


add_permission('GetCurrentIncident_AWSConnect')
add_permission('Escalate_Incident')



"""
Place Slots
For each .json file in the slots directory, open that file and load the JSON.
Check to see if that slot already exists in AWS, if so set the checksum to enable update.
Write the slot to AWS
"""
os.chdir("%s/slots" %rootdir)
slot_json = fnmatch.filter(os.listdir('.'), '*.json')

for slot in slot_json:
    with open(slot, 'r') as stream:
        try:
            slotdef = json.load(stream)
        except Exception as e:
            print(e)
    try:
        slotdef_aws = lex.get_slot_type(name=slotdef["name"], version="$LATEST")
        slotdef["checksum"] = slotdef_aws["checksum"]
    except Exception as e:
        print(e)
    lex.put_slot_type(**slotdef)



"""
Place Intents

For each .json file in the intent directory, open that file and load the JSON.
Check to see if that intent already exists in AWS, if so set the checksum to enable update.
Write the intent to AWS
"""
os.chdir("%s/intents" %rootdir)
intent_json = fnmatch.filter(os.listdir('.'), '*.json')
for intent in intent_json:
    with open(intent, 'r') as stream:
        try:
            intentdef = json.load(stream)
        except Exception as e:
            print(e)
    try:
        intentdef_aws = lex.get_intent(name=intentdef["name"], version="$LATEST")
        intentdef["checksum"] = intentdef_aws["checksum"]
    except Exception as e:
        print(e)
    lex.put_intent(**intentdef)
    
    

"""
Place Bots

For each .json file in the bot directory, open that file and load the JSON.
Check to see if that bot already exists in AWS, if so set the checksum to enable update.
Write the bot to AWS
"""
os.chdir("%s/bots" %rootdir)
bot_json = fnmatch.filter(os.listdir('.'), '*.json')
for bot in bot_json:
    with open(bot, 'r') as stream:
        try:
            botdef = json.load(stream)
        except Exception as e:
            print(e)
    try:
        botdef_aws = lex.get_bot(name=botdef["name"], versionOrAlias="$LATEST")
        botdef["checksum"] = botdef_aws["checksum"]
    except Exception as e:
        print(e)
    lex.put_bot(**botdef)
    