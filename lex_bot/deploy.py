#!/usr/bin/python3

import boto3, fnmatch, json, os, sys, time

"""
|--------------------------------------------------------------------------
| Config
|--------------------------------------------------------------------------
|
| slot_types_dir: The directory which contains the slot type files
| intents_dir:    The directory which contains the intent files
| bots_dir:       The directory which contains the bot files
| version:        The version of all bots, intents and slot types
|
"""
slot_types_dir = "./slots/"
intents_dir    = "./intents/"
bots_dir       = "./bots/"
version        = "1"
latest_version        = "$LATEST"

"""
|--------------------------------------------------------------------------
| AWS Clients
|--------------------------------------------------------------------------
|
| lex:            A client representing Amazon Lex Model Building Service
| lambda_client:  A client representing AWS Lambda
| aws_account_id: The AWS account id retrieved from the aws cli config
|
"""
lex            = boto3.client("lex-models", region_name="eu-west-1")
lambda_client  = boto3.client("lambda",     region_name="eu-west-1")
aws_account_id = boto3.client('sts').get_caller_identity()['Account']

"""
|--------------------------------------------------------------------------
| Get Slot Types
|--------------------------------------------------------------------------
|
| For each .json file in the slots directory, open that file and load the JSON.
| Check to see if that slot type already exists in AWS,
| if so set the checksum to enable update.
| Return a list of all slot types.
|
"""
def get_slot_types():
    slot_type_files = fnmatch.filter(os.listdir(slot_types_dir), "*.json")
    slot_types = []
    for slot_type_file in slot_type_files:
        with open(slot_types_dir + slot_type_file, "r") as stream:
            slot_type = json.load(stream)
        try:
            slot_type_aws = lex.get_slot_type(name=slot_type["name"], version=latest_version)
            slot_type["checksum"] = slot_type_aws["checksum"]
        except lex.exceptions.NotFoundException:
            pass
        slot_types.append(slot_type)
    return slot_types

"""
|--------------------------------------------------------------------------
| Put Slot Types
|--------------------------------------------------------------------------
|
| Upload each slot type to AWS.
| If the checksum is set, the existing slot type will be updated.
|
"""
def put_slot_types():
    slot_types = get_slot_types()
    for slot_type in slot_types:
        try:
            lex.put_slot_type(**slot_type)
        except lex.exceptions.ConflictException as e:
            print(e)
        if "checksum" in slot_type:
            action = "Updated"
        else:
            action = "Created"
        print(action + " Slot Type '" + slot_type["name"] + "'")

"""
|--------------------------------------------------------------------------
| Delete Slot Types
|--------------------------------------------------------------------------
|
| Delete each slot type from AWS.
|
"""
def delete_slot_types():
    slot_types = get_slot_types()
    for slot_type in slot_types:
        delete(lex.delete_slot_type, {"name": slot_type["name"]}, "Deleted Slot Type '" + slot_type["name"] + "'")

"""
|--------------------------------------------------------------------------
| Add Permission
|--------------------------------------------------------------------------
|
| If an intent has a lambda function as fulfillmentActivity,
| it needs the permission to invoke this specific lambda function.
| We have to specify the SourceArn to ensure that no other accounts
| can invoke the lambda function if they hook to the correct ARN.
|
"""
def add_permission(intent):
    function = intent["fulfillmentActivity"]["codeHook"]["uri"].split(":")[-1]
    permission = {
        "FunctionName": "arn:aws:lambda:eu-west-1:" + aws_account_id + ":function:" + function,
        "StatementId":  "statement-id-" + function,
        "Action":       "lambda:InvokeFunction",
        "Principal":    "lex.amazonaws.com",
        "SourceArn":    "arn:aws:lex:eu-west-1:" + aws_account_id + ":intent:" + intent["name"] + ":*"
    }
    lambda_client.add_permission(**permission)

"""
|--------------------------------------------------------------------------
| Get Intents
|--------------------------------------------------------------------------
|
| For each .json file in the intents directory, open that file and load the JSON.
| Check to see if that intent already exists in AWS,
| if so set the checksum to enable update.
| Return a list of all intents.
|
"""
def get_intents():
    intent_files = fnmatch.filter(os.listdir(intents_dir), "*.json")
    intents = []
    for intent_file in intent_files:
        with open(intents_dir + intent_file, "r") as stream:
            intent = json.load(stream)
        try:
            intent_aws = lex.get_intent(name=intent["name"], version=latest_version)
            intent["checksum"] = intent_aws["checksum"]
        except lex.exceptions.NotFoundException:
            pass
        intents.append(intent)
    return intents

"""
|--------------------------------------------------------------------------
| Put Intents
|--------------------------------------------------------------------------
|
| Upload each intent to AWS.
| If the fulfillmentActivity is of type CodeHook, we set the required permission
| so that the intent can access the corresponding lambda function.
| If the checksum is set, the existing intent will be updated.
|
"""
def put_intents():
    intents = get_intents()
    for intent in intents:
        if "checksum" in intent:
            action = "Updated"
        else:
            action = "Created"
            if intent["fulfillmentActivity"]["type"] == "CodeHook":
                try:
                    add_permission(intent)
                    print("Added Lambda Permission To Intent '" + intent["name"] + "'")
                except lambda_client.exceptions.ResourceConflictException:
                    pass
        lex.put_intent(**intent)
        print(action + " Intent '" + intent["name"] + "'")

"""
|--------------------------------------------------------------------------
| Delete Intents
|--------------------------------------------------------------------------
|
| Delete each intent from AWS.
|
"""
def delete_intents():
    intents = get_intents()
    for intent in intents:
        delete(lex.delete_intent, {"name": intent["name"]}, "Deleted Intent '" + intent["name"] + "'")

"""
|--------------------------------------------------------------------------
| Get Bots
|--------------------------------------------------------------------------
|
| For each .json file in the bots directory, open that file and load the JSON.
| Check to see if that intent already exists in AWS,
| if so set the checksum to enable update.
| Return a list of all bots.
|
"""
def get_bots():
    bot_files =  fnmatch.filter(os.listdir(bots_dir), "*.json")
    bots = []
    for bot_file in bot_files:
        with open(bots_dir + bot_file, "r") as stream:
            bot = json.load(stream)
        try:
            bot_aws = lex.get_bot(name=bot["name"], versionOrAlias=latest_version)
            bot["checksum"] = bot_aws["checksum"]
        except lex.exceptions.NotFoundException:
            pass
        bots.append(bot)
    return bots

"""
|--------------------------------------------------------------------------
| Put Bots
|--------------------------------------------------------------------------
|
| Upload each bot to AWS.
| If the checksum is set, the existing bot will be updated.
| After the each bot is created, call the put_bot_alias method.
|
"""
def put_bots():
    bots = get_bots()
    for bot in bots:
        try:
            lex.put_bot(**bot)
        except lex.exceptions.ConflictException as e:
            print(e)
        if "checksum" in bot:
            action = "Updated"
        else:
            action = "Created"
        print(action + " Bot '" + bot["name"] + "'")
        put_bot_alias(bot)

"""
|--------------------------------------------------------------------------
| Delete Bots
|--------------------------------------------------------------------------
|
| For every bot, delete the bot alias and then the bot itself from AWS.
|
"""
def delete_bots():
    bots = get_bots()
    for bot in bots:
        bot_alias = get_bot_alias(bot)
        delete_bot_alias(bot_alias)
        delete(lex.delete_bot, {"name": bot["name"]}, "Deleted Bot '" + bot["name"] + "'")

"""
|--------------------------------------------------------------------------
| Get Bot Alias
|--------------------------------------------------------------------------
|
| Get the bot alias of a bot.
| Check to see if that alias already exists in AWS,
| if so set the checksum to enable update.
| Return the bot alias.
|
"""
def get_bot_alias(bot):
    bot_alias = {
        "name":        bot["name"] + "Alias",
        "description": "Alias of " + bot["name"],
        "botVersion":  version,
        "botName":     bot["name"]
    }
    try:
        bot_alias_aws = lex.get_bot_alias(name=bot_alias["name"], botName=bot_alias["botName"])
        bot_alias["checksum"] = bot_alias_aws["checksum"]
    except lex.exceptions.NotFoundException:
        pass
    return bot_alias

"""
|--------------------------------------------------------------------------
| Put Bot Alias
|--------------------------------------------------------------------------
|
| Upload the alias of the given bot to AWS.
| If the checksum is set, the existing bot will be updated.
| In order to publish a bot and establish a connection to a channel,
| the bot needs an alias which is tied to a specific version of the bot.
|
"""
def put_bot_alias(bot):
    bot_alias = get_bot_alias(bot)
    lex.put_bot_alias(**bot_alias)
    if "checksum" in bot_alias:
        action = "Updated"
    else:
        action = "Created"
    print(action + " Bot Alias '" + bot["name"] + "Alias'")

"""
|--------------------------------------------------------------------------
| Delete Bot Alias
|--------------------------------------------------------------------------
|
| Delete the alias of the given bot and all its channel associations from AWS.
|
"""
def delete_bot_alias(bot_alias):
    bot_channel_associations = lex.get_bot_channel_associations(botName=bot_alias["botName"], botAlias=bot_alias["name"])["botChannelAssociations"]
    for bot_channel_association in bot_channel_associations:
        arguments = {
            "name":     bot_channel_association["name"],
            "botName":  bot_channel_association["botName"],
            "botAlias": bot_channel_association["botAlias"]
        }
        delete(
            lex.delete_bot_channel_association, arguments, "Deleted Bot Channel Association '" + bot_channel_association["name"] + "'"
        )
    arguments = {
        "name":    bot_alias["name"],
        "botName": bot_alias["botName"]
    }
    delete(lex.delete_bot_alias, arguments, "Deleted Bot Alias '" + bot_alias["name"] + "'")

"""
|--------------------------------------------------------------------------
| Delete
|--------------------------------------------------------------------------
|
| Delete something from AWS.
| We need the while loop because the delete function is asynchronous and
| multiple delete operations can not be executed in parallel which may
| result in a ConflictException. In this case, we want to retry until
| the operation is successful.
|
"""
def delete(function_name, arguments, message):
    while True:
        try:
            function_name(**arguments)
            print(message)
        except lex.exceptions.NotFoundException:
            pass
        except lex.exceptions.ConflictException:
            time.sleep(1)
            continue
        break

"""
|--------------------------------------------------------------------------
| Main method
|--------------------------------------------------------------------------
|
| When executing the script, it checks for the first command line argument.
| Depending on the argument, we create or destroy the whole lex infrastructure.
| If none of the arguments match, we print the usage.
| We use a main method to enable including this file as a seperate module.
|
"""
def main(args):
    if len(args) == 2 and args[1] == "create":
        put_slot_types()
        put_intents()
        put_bots()
    elif len(args) == 2 and args[1] == "destroy":
        delete_bots()
        delete_intents()
        delete_slot_types()
    else:
        print("Usage: " + args[0] + " {create|destroy}")

if __name__ == "__main__":
    main(sys.argv)
