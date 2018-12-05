import logging

from kubernetes import client, config

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

v1 = 0
""" --- Helpers to build responses which match the structure of the necessary dialog actions --- """


def get_slots(intent_request):
    return intent_request['currentIntent']['slots']


def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response


""" --- Functions that control the bot's behavior --- """


def kubectl_get_api_call(intent_request):
    """
    Performs dialog management and fulfillment for ordering flowers.
    Beyond fulfillment, the implementation of this intent demonstrates the use of the elicitSlot dialog action
    in slot validation and re-prompting.
    """
    global v1

    get_resource = get_slots(intent_request)["resource"]
    result = {"message": "error: the server doesn't have a resource type " + get_resource}
    source = intent_request['invocationSource']

    if source == 'DialogCodeHook':
        # Perform basic validation on the supplied input slots.
        # Use the elicitSlot dialog action to re-prompt for the first violation detected.
        slots = get_slots(intent_request)

        # Validate slots here, not needed because it's a get call

    if get_resource == 'node' or get_resource == 'nodes':
        logger.debug("api call list_node")
        result = v1.list_node(pretty='true')
    elif get_resource == 'componentstatus':
        logger.debug("api call list_component_status")
        result = v1.list_component_status()
    elif get_resource == 'configmap' or get_resource == 'configmaps':
        logger.debug("api call list_config_map_for_all_namespaces")
        result = v1.list_config_map_for_all_namespaces()
    elif get_resource == 'deployment' or get_resource == 'deployments':
        logger.warning("api call not in core api v1")
        result = {"message": "error: the core api v1 does not implement the resource " + get_resource + " yet."}

    # Order the flowers, and rely on the goodbye message of the bot to define the message to the end user.
    # In a real bot, this would likely involve a call to a backend service.
    return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'CustomPayload',
                  'content': str(result)})


""" --- Intents --- """


def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    logger.debug(
        'dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'kubectlGet':
        return kubectl_get_api_call(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')


""" --- Setup --- """


def setup_kubernetes():
    # This file has to be bundled with the function.zip (created by kops after cluster ~/.kube/conf)
    global v1
    config.load_kube_config("config")

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
        raise Exception('Failed to initialize Kubernetes API')

    return dispatch(event)


# Offline mock event
demo_event = {
    "messageVersion": "1.0",
    "invocationSource": "DialogCodeHook",
    "userId": "John",
    "sessionAttributes": {},
    "bot": {
        "name": "kubectl",
        "alias": "$LATEST",
        "version": "$LATEST"
    },
    "outputDialogMode": "Text",
    "currentIntent": {
        "name": "kubectlGet",
        "slots": {
            "resource": "node",
        },
        "confirmationStatus": "None"
    }
}

# Offline mock call comment when publish!
# print("init")
# print(lambda_handler(demo_event, ''))
# print("ini2t")
# demo_event['currentIntent']['slots']['resource'] = "componentstatus"
# print(lambda_handler(demo_event, ''))
# print("init3")
# demo_event['currentIntent']['slots']['resource'] = "deployment"
# print(lambda_handler(demo_event, ''))
# print("init4")
# demo_event['currentIntent']['slots']['resource'] = "NonResource"
# print(lambda_handler(demo_event, ''))
