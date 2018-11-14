#!/usr/bin/python3

import boto3
import json


# from botocore.exceptions import PreconditionFailedException
# from botocore.exceptions import BadRequestException


def put_slot_type(slot_type_file):
    slot_type_string = open('resources/' + slot_type_file, 'r').read()
    slot_type = json.loads(slot_type_string)
    print ('Putting slot type')
    try:
        # TODO Throws PreconditionFailedException on version update or BadRequestException on value error,
        # but how to catch and handle these?
        response = client.put_slot_type(**slot_type)
    except Exception as e:
        print (e)
        print ('Setting checksum to $LATEST to replace current version!')
        response = client.get_slot_type(name=slot_type['name'], version='$LATEST')
        slot_type['checksum'] = response['checksum']
        response = client.put_slot_type(**slot_type)

    print ('Putting slot type done')
    print (response)

    response = client.get_slot_types()
    print ('Currently ' + str(len(response['slotTypes'])) + ' slot types.')


def put_intent(intent_file):
    intent_string = open('resources/' + intent_file, 'r').read()
    intent = json.loads(intent_string)
    print ('Putting intent')
    try:
        # TODO Throws PreconditionFailedException on version update or BadRequestException on value error,
        # but how to catch and handle these?
        response = client.put_intent(**intent)
    except Exception as e:
        print (e)
        print ('Setting checksum to $LATEST to replace current version!')
        response = client.get_intent(name=intent['name'], version='$LATEST')
        intent['checksum'] = response['checksum']
        response = client.put_intent(**intent)

    print ('Putting intent done')
    print (response)

    response = client.get_intents()
    print ('Currently ' + str(len(response['intents'])) + ' intents.')


def put_bot(bot_file):
    bot_string = open('resources/' + bot_file, 'r').read()
    bot = json.loads(bot_string)
    print ('Putting bot')
    try:
        # TODO Throws PreconditionFailedException on version update or BadRequestException on value error,
        # but how to catch and handle these?
        response = client.put_bot(**bot)
    except Exception as e:
        print (e)
        print ('Setting checksum to $LATEST to replace current version!')
        print (bot['name'])
        response = client.get_bot(name=bot['name'], versionOrAlias='$LATEST')
        print (bot['name'])
        print (response)
        bot['checksum'] = response['checksum']
        response = client.put_bot(**bot)

    print ('Putting bot done')
    print (response)

    response = client.get_bots()
    print ('Currently ' + str(len(response['bots'])) + ' bots.')


slot_type_file = 'example_slot_types.json'
intent_file = 'example_intent.json'
bot_file = 'example_bot.json'

client = boto3.client('lex-models', region_name='eu-west-1')

put_slot_type(slot_type_file)
put_intent(intent_file)
put_bot(bot_file)
