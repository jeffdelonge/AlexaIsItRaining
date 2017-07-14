import urllib.request

RED_CARPET_APPLICATION_ID = "amzn1.ask.skill.9d78870e-6c3b-4ced-9894-412f5d84f25e"

def lambda_handler(event, context):
    # Ensure that the request was intended for our service
    if (event['session']['application']['applicationId'] != RED_CARPET_APPLICATION_ID):
        raise ValueError("Invalid applicationId")

    # Get the request type and call the corresponding request handler
    request_type = event['request']['type']
    if request_type == "LaunchRequest":
        return on_launch(event['request'])
    elif request_type == "IntentRequest":
        return on_intent(event['request'])
    elif request_type == "SessionEndedRequest":
        return on_session_ended(event['request'])



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

    if intent_name == "IsItRainingInLocation":
        return is_it_raining_in_location(intent)
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



# Intent handlers & speech utilities --------------------------------------------------------------------------------------------
def is_it_raining_in_location(intent):
    location = intent['slots']['Location']['value'].replace(' ', '')

    url = "https://isitraining.in/{}".format(location)
    req = urllib.request.Request(
        url, 
        headers={
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3)\
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
        }
    )
    f = urllib.request.urlopen(req)
    html = (f.read().decode('utf-8'))

    index = html.find("<h1 class='result'>")
    if html[index + 19] == 'Y':
        result = 'Yes'
    else:
        result = 'No'

    response_object = build_response_object(result)
    return build_response(None, response_object)


def get_help_response():
    card = build_card_object("Help", "Listen to Alexa for help...")
    help_text = "You can ask Alexa if it's raining in a US city.\
                    You can say things like, Seattle,\
                    Is it raining in New York?\
                    You can also say stop, to quit."
    response_object = build_response_object(help_text, card)
    return build_response(None, response_object)


def get_welcome_response():
    output_text = "Hello! Give me a city to check for rain!"
    response_object = build_response_object(output_text)
    return build_response(None, response_object)



# JSON response utilities -------------------------------------------------------------------------------------------------------
# https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/alexa-skills-kit-interface-reference
def build_response(session_attributes, response_object):
    """Returns a complete response JSON object.
    You should use the other response object builders to construct the response_object parameter.
    https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/alexa-skills-kit-interface-reference#response-format
    """
    return {
        'version': "1.0",
        'sessionAttributes': session_attributes,
        'response': response_object
    }


def build_response_object(output_speech_text, card=None, reprompt_output_speech_text=None, should_end_session=False):
    """Returns a JSON response object with the specified output speech, card, and reprompt speech.
    You should use this to construct the response_object parameter for the build_response function.
    Use build_card_object to construct the card parameter.
    should_end_session: A boolean value with true meaning that the session should end after Alexa speaks
        the response, or false if the session should remain active. If not provided, defaults to true.
    https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/alexa-skills-kit-interface-reference#response-object
    """
    return {
        'outputSpeech': {
            'type': "PlainText",
            'text': output_speech_text
        },
        'card': card,
        'reprompt': {
            'outputSpeech': {
                'type': "PlainText",
                'text': reprompt_output_speech_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_card_object(title, content=None, card_type="Simple", small_image_url=None, large_image_url=None):
    """Returns a JSON card object of the type specified by card_type. Optional arguments small_image_url and
    large_image_url specify image sources when card_type is set to "Standard". Note that content does not apply
    when using the "Standard" card type.
    https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/alexa-skills-kit-interface-reference#card-object
    """
    if (card_type == "Simple"):
        return {
            'type': "Simple",
            'title': title,
            'content': content
        }
    elif (card_type == "Standard"):
        return {
            'type': "Standard",
            'title': title,
            'content': content,
            'image': {
                'smallImageUrl': small_image_url,
                'largeImageUrl': large_image_url
            }
        }
    else:
      raise ValueError("Invalid card_type (or you are using card_type=LinkAccount)")
