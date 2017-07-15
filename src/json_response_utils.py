# JSON response utilities -------------------------------------------------------------------------------------------------------
# https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/alexa-skills-kit-interface-reference
def build_response(output_speech_text, reprompt_speech_text=None, should_end_session=False):
    """Returns a complete response JSON object with the specified output speech and reprompt speech.
    should_end_session: A boolean value with true meaning that the session should end after Alexa speaks
        the response, or false if the session should remain active. If not provided, defaults to false.
    https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/alexa-skills-kit-interface-reference#response-format
    """
    return {
        'version': "1.0",
        'response': {
            'outputSpeech': {
                'type': "PlainText",
                'text': output_speech_text
            },
            'reprompt': {
                'outputSpeech': {
                    'type': "PlainText",
                    'text': reprompt_speech_text
                }
            },
            'shouldEndSession': should_end_session
        }
    }
