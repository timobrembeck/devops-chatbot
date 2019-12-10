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
| latest_version: The version of all bots, intents and slot types
| lex_region:     The region in which AWS Lex should be deployed
| lambda_region:  The region in which AWS Lambda should be deployed
|
"""
slot_types_dir = "./slots/"
intents_dir    = "./intents/"
bots_dir       = "./bots/"
latest_version = "$LATEST"
lex_region     = "eu-west-1"
lambda_region  = "eu-west-1"

"""
|--------------------------------------------------------------------------
| AWS Clients
|--------------------------------------------------------------------------
|
| aws_account_id: The AWS account id retrieved from the aws cli config
| lex:            A client representing Amazon Lex Model Building Service
| lex_arn:        The AWS Lex ARN derived from region and account id
| lambda_client:  A client representing AWS Lambda
| lambda_arn:     The AWS Lambda ARN derived from region and account id
|
"""
aws_account_id = boto3.client('sts').get_caller_identity()['Account']
lex            = boto3.client("lex-models", region_name=lex_region)
lex_arn        = "arn:aws:lex:" + lex_region + ":" + aws_account_id + ":intent:"
lambda_client  = boto3.client("lambda",     region_name=lambda_region)
lambda_arn     = "arn:aws:lambda:" + lambda_region + ":" + aws_account_id + ":function:"


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
        new_slot_type = lex.put_slot_type(**slot_type)
        if "checksum" not in slot_type:
            print("Created Slot Type '" + slot_type["name"] + "'")
        elif slot_type["checksum"] != new_slot_type["checksum"]:
            print("Updated Slot Type '" + slot_type["name"] + "'")

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
def add_permission(intent, lambda_function):
    permission = {
        "FunctionName": lambda_arn + lambda_function,
        "StatementId":  "statement-id-" + lambda_function,
        "Action":       "lambda:InvokeFunction",
        "Principal":    "lex.amazonaws.com",
        "SourceArn":    lex_arn + intent["name"] + ":*"
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
        slots = []
        for slot in intent["slots"]:
            if slot["slotType"][:7] != "AMAZON.":
                slot_type_versions = lex.get_slot_type_versions(name=slot["slotType"], maxResults=50)
                slot["slotTypeVersion"] = slot_type_versions["slotTypes"][-1]["version"]
            slots.append(slot)
        intent["slots"] = slots
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
        if intent["fulfillmentActivity"]["type"] == "CodeHook":
            lambda_function = intent["fulfillmentActivity"]["codeHook"]["uri"].split(":")[-1]
            intent["fulfillmentActivity"]["codeHook"]["uri"] = lambda_arn + lambda_function
        new_intent = lex.put_intent(**intent)
        if "checksum" not in intent:
            print("Created Intent '" + intent["name"] + "'")
            if intent["fulfillmentActivity"]["type"] == "CodeHook":
                add_permission(intent, lambda_function)
                print("Added Permission for Lambda function " + lambda_function + " to Intent '" + intent["name"] + "'")
        elif intent["checksum"] != new_intent["checksum"]:
            print("Updated Intent '" + intent["name"] + "'")

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
        intents = []
        for intent in bot["intents"]:
            intent_versions = lex.get_intent_versions(name=intent["intentName"], maxResults=50)
            intent["intentVersion"] = intent_versions["intents"][-1]["version"]
            intents.append(intent)
        bot["intents"] = intents
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
        new_bot = lex.put_bot(**bot)
        if "checksum" not in bot:
            print("Created Bot '" + bot["name"] + "'")
        elif bot["checksum"] != new_bot["checksum"]:
            print("Updated Bot '" + bot["name"] + "'")
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
        "botName":     bot["name"]
    }
    bot_versions = lex.get_bot_versions(name=bot_alias["botName"], maxResults=50)
    bot_alias["botVersion"] = bot_versions["bots"][-1]["version"]
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
    new_bot_alias = lex.put_bot_alias(**bot_alias)
    if "checksum" not in bot_alias:
        print("Created Bot Alias '" + bot_alias["name"] + "'")
    elif bot_alias["checksum"] != new_bot_alias["checksum"]:
        print("Updated Bot Alias '" + bot_alias["name"] + "'")

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
        print("Successfully created AWS Lex infrastructure")
    elif len(args) == 2 and args[1] == "destroy":
        delete_bots()
        delete_intents()
        delete_slot_types()
        print("Successfully deleted AWS Lex infrastructure")
    else:
        print("Usage: " + args[0] + " {create|destroy}")

if __name__ == "__main__":
    main(sys.argv)
