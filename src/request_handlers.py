from intent_handlers import *

# Request handlers --------------------------------------------------------------------------------------------------------------
def on_launch(launch_request):
    """Your service receives a LaunchRequest when the user invokes the skill with
    the invocation name, but does not provide any command mapping to an intent.
    https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/custom-standard-request-types-reference#launchrequest
    """
    return get_welcome_response()


def on_intent(intent_request):
    """Your service receives an IntentRequest when the user speaks a command that maps to an intent.
    The request object sent to your service includes the specific intent and any defined slot values.
    https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/custom-standard-request-types-reference#intentrequest
    https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/handling-requests-sent-by-alexa#intentrequest

    For standard built-in intents (e.g., AMAZON.HelpIntent), see
        https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/built-in-intent-ref/standard-intents
    """
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    if (intent_name == "IsItRainingInLocation"):
        return is_it_raining_in_location(intent)
    elif (intent_name == "AMAZON.HelpIntent"):
        return get_help_response()
    elif (intent_name == "AMAZON.CancelIntent"):
        return get_goodbye_response()
    elif (intent_name == "AMAZON.StopIntent"):
        return get_goodbye_response()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request):
    """Your service receives a SessionEndedRequest when a currently open session is closed for one of the following reasons:
      1. The user says "exit".
      2. The user does not respond or says something that does not match an intent defined in your
            voice interface while the device is listening for the user's response.
      3. An error occurs.
    Note that setting the shouldEndSession flag to true in your response also ends the session.
    In this case, your service does not receive a SessionEndedRequest.
    Your service cannot send back a response to a SessionEndedRequest.
    https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/custom-standard-request-types-reference#sessionendedrequest
    """
