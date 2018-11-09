import boto3
import json
#from botocore.exceptions import PreconditionFailedException
#from botocore.exceptions import BadRequestException

client = boto3.client('lex-models', region_name='eu-west-1')


slot_type_string = open("resources/example_slot_types.json", "r").read()
slot_type = json.loads(slot_type_string)

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
print 'Currently ' + str(len(response['slotTypes'])) + ' slot types.'

