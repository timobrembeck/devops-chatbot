import json
import requests
import os

def get_server_status(server):
    response = requests.get(server)
    print('res', response)
    json_res = response.json()
    message = "Status of: "
    if json_res['status'] == 'success':
        for i in json_res['data']['result']:
            message = message + i['metric']['instance'] +' is '
            print('------>',  i['value'][1])
            if int(i['value'][1]) == 1:
                message = message + 'up; '
            else:
                message = message + 'down; '
    else:
        message = 'The status could not be queried'
    return message

def lambda_handler(event, context):
    event_json = json.dumps(event)
    message = get_server_status(os.environ['porm_server'])
    print(message)
    return   {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "PlainText",
                "content": str(message)
            }
            
        }
        
    }

