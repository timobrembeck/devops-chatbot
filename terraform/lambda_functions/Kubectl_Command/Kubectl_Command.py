import logging, os

from kubernetes import client, config

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

node_list_keys = ('name', 'role', 'status', 'last_message', 'cpu_allocation', 'creation')

v1 = 0
""" --- Helpers to build responses which match the structure of the necessary dialog actions --- """


def get_slots(intent_request):
    return intent_request['currentIntent']['slots']


def close(intent_request, fulfillment_state, message):
    # check if request is from slack bot
    # See https://github.com/timoludwig/devops-chatbot/wiki/AWS-Lambda-Notes

    if intent_request['requestAttributes'] is not None and \
            'x-amz-lex:channel-name' in intent_request['requestAttributes'] and \
            intent_request['requestAttributes']['x-amz-lex:channel-name'] == 'Slack':
        # if message is a list -> transform it into table with slack code escaping
        if (type(message) is list):
            message = "```" + print_table(message) + "```"
    else:
        # if message is a list -> transform it into sentence
        if (type(message) is list):
            message = print_sentence(message, intent_request)

    response = {
        'sessionAttributes': intent_request['sessionAttributes'],
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': {'contentType': 'PlainText',
                        'content': message}
        }
    }

    return response


def print_table(rows):
    # figure out column widths
    widths = [len(max(columns, key=len)) for columns in zip(*rows)]

    # print the header
    header, data = rows[0], rows[1:]
    result = ' | '.join(format(title, "%ds" % width) for width, title in zip(widths, header)) + "\n"

    # print the separator
    result += '-+-'.join('-' * width for width in widths) + "\n"

    # print the data
    for row in data:
        result += " | ".join(format(cdata, "%ds" % width) for width, cdata in zip(widths, row)) + "\n"

    return result


def print_sentence(rows, intent_request):
    get_resource = get_slots(intent_request)["resource"]
    header, data = rows[0], rows[1:]

    message = "There are " + str(len(data)) + " " + get_resource + "s in total. "

    status = {}
    for row in data:

        if row[2] in status:
            status[(row[2])] += 1
        else:
            status[(row[2])] = 1

    for stat, count in status.items():
        message += "There are " + str(count) + " " + get_resource + "s with status " + stat

    return message


""" --- Functions that control the bot's behavior --- """


def kubectl_get_api_call(intent_request):
    """
    Performs dialog management and fulfillment.
    Beyond fulfillment, the implementation of this intent demonstrates the use of the elicitSlot dialog action
    in slot validation and re-prompting.
    """
    global v1

    get_resource = get_slots(intent_request)["resource"]
    result = "error: the resource is not supported yet or does not exist"
    source = intent_request['invocationSource']

    if source == 'DialogCodeHook':
        # Perform basic validation on the supplied input slots.
        # Use the elicitSlot dialog action to re-prompt for the first violation detected.
        slots = get_slots(intent_request)

        # Validate slots here, not needed because it's a get call
    logger.debug("The resource lex understood: " + get_resource)
    if get_resource == 'node' or get_resource == 'nodes':
        logger.debug("api call list_node")
        result = v1.list_node()
        rows = [node_list_keys]
        for node in result.items:
            # More info on kubectl cpu allocation: https://github.com/kubernetes/kubernetes/issues/17512
            cpu_node = 0
            pod_result = v1.list_pod_for_all_namespaces(field_selector="spec.nodeName=" + node.metadata.name)

            for pod in pod_result.items:
                for container in pod.spec.containers:
                    cpu_node += int(container.resources.requests['cpu'].replace('m', ''))

            row = (node.metadata.name,
                   node.metadata.labels['kubernetes.io/role'],
                   node.status.conditions[-1].type,
                   node.status.conditions[-1].message,
                   str(cpu_node / 10) + "%",
                   node.metadata.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S"))
            rows.append(row)
        result = rows
    elif get_resource == 'componentstatus':
        logger.debug("api call list_component_status")
        result = v1.list_component_status()
    elif get_resource == 'configmap' or get_resource == 'configmaps':
        logger.debug("api call list_config_map_for_all_namespaces")
        result = v1.list_config_map_for_all_namespaces()
    elif get_resource == 'deployment' or get_resource == 'deployments':
        logger.warning("api call not in core api v1")
        result = {"message": "error: the core api v1 does not implement the resource " + get_resource + " yet."}

    return close(intent_request, 'Fulfilled', result)


""" --- Intents --- """


def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    # logger.debug(
    #    'dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'KubernetesIntent':
        return kubectl_get_api_call(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')


""" --- Setup --- """


def setup_kubernetes():
    # This file has to be bundled with the function.zip (created by kops after cluster ~/.kube/conf)
    global v1
    try:
        config.load_kube_config("config")
    except:
        message = "Loading config from package failed"
        logger.error(message)
        return False

    v1 = client.CoreV1Api()

    # Try to get a api call done to check configuration, timeout at 2s because lambda timeout is 3s
    try:
        v1.list_node(limit=1, timeout_seconds=2)
    except:
        message = "No connection possible"
        logger.error(message)
        return False

    return True


""" --- Main handler --- """


def lambda_handler(event, context):
    # print("Received event: " + json.dumps(event, indent=2))
    # logger.debug("Incoming event: " + json.dumps(event))

    if not (setup_kubernetes()):
        logger.error("Kubernetes API config fails.")
        return close(event, 'Fulfilled', "Kubernetes is not properly configured. Please have a look in the logs.")

    result = dispatch(event)
    logger.debug(result)
    return result


# Offline mock event
demo_connect_event = {'messageVersion': '1.0',
                      'invocationSource': 'FulfillmentCodeHook',
                      'userId': 'test',
                      'sessionAttributes': {},
                      'requestAttributes': {'x-amz-lex:accept-content-types': 'PlainText,SSML'},
                      'bot': {'name': 'DevOpsChatBot',
                              'alias': '$LATEST',
                              'version': '$LATEST'},
                      'outputDialogMode': 'Text',
                      'currentIntent': {'name': 'KubernetesIntent',
                                        'slots': {'resource': 'node'},
                                        'slotDetails': {
                                            'resource': {'resolutions': [{'value': 'node'}],
                                                         'originalValue': 'node'}},
                                        'confirmationStatus': 'None',
                                        'sourceLexNLUIntentInterpretation': None},
                      'inputTranscript': 'node'}

demo_chat_event = {'messageVersion': '1.0',
                   'invocationSource': 'FulfillmentCodeHook',
                   'userId': 'test',
                   'sessionAttributes': {},
                   'requestAttributes': None,
                   'bot': {'name': 'DevOpsChatBot',
                           'alias': '$LATEST',
                           'version': '$LATEST'},
                   'outputDialogMode': 'Text',
                   'currentIntent': {'name': 'KubernetesIntent',
                                     'slots': {'resource': 'node'},
                                     'slotDetails': {'resource': {'resolutions': [{'value': 'node'}],
                                                                  'originalValue': 'node'}},
                                     'confirmationStatus': 'None',
                                     'sourceLexNLUIntentInterpretation': None},
                   'inputTranscript': 'node'}

demo_slack_event = {'messageVersion': '1.0',
                    'invocationSource': 'FulfillmentCodeHook',
                    'userId': 'test',
                    'sessionAttributes': {},
                    'requestAttributes': {'x-amz-lex:channel-id': '7cd6cfc4-8356-4e6b-a879-81aae1b89097',
                                          'x-amz-lex:webhook-endpoint-url': 'https://channels.lex.eu-west-1.amazonaws.com/slack/webhook/7cd6cfc4-8356-4e6b-a879-81aae1b89097',
                                          'x-amz-lex:accept-content-types': 'PlainText',
                                          'x-amz-lex:user-id': '465214619063.487654285126',
                                          'x-amz-lex:slack-team-id': 'TDP6AJ71V',
                                          'x-amz-lex:slack-bot-token': os.environ['token'],
                                          'x-amz-lex:channel-name': 'Slack', 'x-amz-lex:channel-type': 'Slack'},
                    'bot': {'name': 'DevOpsChatBot', 'alias': 'DevOpsChatBotAlias', 'version': '10'},
                    'bot': {'name': 'DevOpsChatBot',
                            'alias': '$LATEST',
                            'version': '$LATEST'},
                    'outputDialogMode': 'Text',
                    'currentIntent': {'name': 'KubernetesIntent',
                                      'slots': {'resource': 'node'},
                                      'slotDetails': {'resource': {'resolutions': [{'value': 'node'}],
                                                                   'originalValue': 'node'}},
                                      'confirmationStatus': 'None',
                                      'sourceLexNLUIntentInterpretation': None},
                    'inputTranscript': 'node'}

# Offline mock call comment when publish!
#print("init")
#print(lambda_handler(demo_connect_event, ''))
#print(lambda_handler(demo_chat_event, ''))
#print(lambda_handler(demo_slack_event, ''))