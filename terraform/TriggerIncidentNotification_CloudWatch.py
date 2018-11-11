import json
import os
import boto3


def publish_to_connect_sns(payload):
    sns = boto3.client('sns')
    response = sns.publish (
        TargetArn = os.environ['SNS_EIP_NOTIFY_ARN'],
        Message = json.dumps(payload)
    )
    return response

def lambda_handler(event, context):
    event_msg = json.loads(event['Records'][0]['Sns']['Message'])
    
    print(json.dumps(event_msg))

    state_value = event_msg['NewStateValue']
    region = event_msg['Region']
    metric_name = event_msg['Trigger']['MetricName']
    comparison_operator = event_msg['Trigger']['ComparisonOperator']
    threshold = event_msg['Trigger']['Threshold']
    datapoints = event_msg['Trigger']['EvaluationPeriods']
    period = event_msg['Trigger']['Period']
    description = event_msg['AlarmDescription']
    
    if description is None:
        description = ''

    message = 'CloudWatch Alarm in ' + region + '.;;;; Alarm description: ;;' + description + '. ;; Details: ' + metric_name + ' ' + comparison_operator + ' '+ str(threshold) + ' for ' + str(int(datapoints)) + ' data points, within ' + str(int(datapoints*period/60)) + ' minutes.</speak>'
    destination_phone_number = os.environ['destinationPhoneNumber']
    
    payload = {
        'message': message,
        'destination_phone_number': destination_phone_number
    }
    
    print(json.dumps(payload))
    
    publish_to_connect_sns(payload)
    
    