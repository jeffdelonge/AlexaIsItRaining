import constants
from request_handlers import *

def lambda_handler(event, context):
    # Ensure that the request was intended for our service
    if (event['session']['application']['applicationId'] != constants.IS_IT_RAINING_APPLICATION_ID):
        raise ValueError("Invalid applicationId")

    # Get the request type and call the corresponding request handler
    request_type = event['request']['type']
    if (request_type == "LaunchRequest"):
        return on_launch(event['request'])
    elif (request_type == "IntentRequest"):
        return on_intent(event['request'])
    elif (request_type == "SessionEndedRequest"):
        return on_session_ended(event['request'])
