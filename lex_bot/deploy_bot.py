#!/usr/bin/python3

import os
import boto3
import json
import fnmatch
import random
import string
import sys

"""
Global Information
"""

lex = boto3.client('lex-models', region_name='eu-west-1')
lambda_client = boto3.client('lambda', region_name='eu-west-1')
rootdir = cwd = os.getcwd()

"""
Global Functions
"""

def print_heading(heading):
    print('#' * (len(heading) + 4))
    print("# " + heading + " #")
    print('#' * (len(heading) + 4) + '\n')

def print_response(response):
	# make datetime object to string so it can be printed as json
    if 'lastUpdatedDate' in response:
        response['lastUpdatedDate'] = response['lastUpdatedDate'].ctime()
    if 'createdDate' in response:
        response['createdDate'] = response['createdDate'].ctime()
    print(json.dumps(response, indent=4) + "\n")


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
        # If intent has a code hook as fulfillmentActivity, add permission of needed lambda function 
        if intentdef["fulfillmentActivity"]["type"] == "CodeHook":
            print_heading("Add Permission To Intent '" + intentdef["name"] + "'")
            permissiondef = {
                "FunctionName": intentdef["fulfillmentActivity"]["codeHook"]["uri"],
                "StatementId": 'add-invoke-permission_' + ''.join(random.choice(string.hexdigits) for i in range(1, 20)),
                "Action": 'lambda:InvokeFunction',
                "Principal": 'lex.amazonaws.com'
            }
            intent_permission_aws_response = lambda_client.add_permission(**permissiondef)
            if len(sys.argv) > 1 and sys.argv[1] == '--debug':
                print_response(intent_permission_aws_response)
    except Exception as e:
        print(e)
    try:
		# Get intent to check if it already existists in aws
        intentdef_aws = lex.get_intent(name=intentdef["name"], version="1")
        intentdef["checksum"] = intentdef_aws["checksum"]
    except lex.exceptions.NotFoundException:
		# Just ignore if intent is not found and let checksum unset
        pass
    except Exception as e:
        print(e)
    try:
        print_heading("Create Intent '" + intentdef["name"] + "'")
        intent_aws_response = lex.put_intent(**intentdef)
        if len(sys.argv) > 1 and sys.argv[1] == '--debug':
            print_response(intent_aws_response)
    except Exception as e:
        print(e)
    
    

"""
Place Bots

For each .json file in the bot directory, open that file and load the JSON.
Check to see if that bot already exists in AWS, if so set the checksum to enable update.
Write the bot to AWS
"""
os.chdir("%s/bots" %rootdir)
bot_json = fnmatch.filter(os.listdir('.'), '*.json')
for bot in bot_json:
	# Open bot file
    with open(bot, 'r') as stream:
        try:
            botdef = json.load(stream)
        except Exception as e:
            print(e)
    print_heading("Create Bot '" + botdef["name"] + "'")
    try:
		# Get bot to check if it already existists in aws
        botdef_aws = lex.get_bot(name=botdef["name"], versionOrAlias="1")
        botdef["checksum"] = botdef_aws["checksum"]
    except lex.exceptions.NotFoundException:
		# Just ignore if bot is not found and let checksum unset
        pass
    except Exception as e:
        print(e)
    try:
        bot_aws_response = lex.put_bot(**botdef)
        if len(sys.argv) > 1 and sys.argv[1] == '--debug':
            print_response(bot_aws_response)
    except Exception as e:
        print(e)
    print_heading("Create Bot Alias '" + botdef["name"] + "Alias'")
    botaliasdef = {
        "name": botdef["name"] + "Alias",
        "description": 'Description',
        "botVersion": '1',
        "botName": botdef["name"]
    }
    try:
		# Get bot alias to check if it already existists in aws
        botaliasdef_aws = lex.get_bot_alias(name=botaliasdef["name"], botName=botaliasdef["botName"])
        botaliasdef["checksum"] = botaliasdef_aws["checksum"]
    except lex.exceptions.NotFoundException:
		# Just ignore if bot alias is not found and let checksum unset
        pass
    except Exception as e:
        print(e)
    try:
		# put alias to publish the bot and enable slack integration
        bot_alias_aws_response = lex.put_bot_alias(**botaliasdef)
        if len(sys.argv) > 1 and sys.argv[1] == '--debug':
            print_response(bot_alias_aws_response)
    except Exception as e:
        print(e)
    
