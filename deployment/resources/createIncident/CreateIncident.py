import time
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# -- Intent responses --
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

# --- Helper Functions ---
def try_ex(func):
    """
    Call passed in function in try block. If KeyError is encountered return None.
    This function is intended to be used to safely access dictionary.

    Note that this function would have negative impact on performance.
    """

    try:
        return func()
    except KeyError:
        return None

# --- Intents ---
def answer_pill(intent_request):
    pill = try_ex(lambda: intent_request['currentIntent']['slots']['PillType'])

    if pill == 'red':
        answer = 'You get knowledge, freedom, uncertainty and the brutal truths of reality.'
    elif pill == 'blue':
        answer = 'You get security, happiness, beauty, and the blissful ignorance of illusion.'
    else:
        answer = 'You fool!'
    return close({}, 'Fulfilled',
                 {
                     'contentType': 'PlainText',
                     'content': answer
                 })