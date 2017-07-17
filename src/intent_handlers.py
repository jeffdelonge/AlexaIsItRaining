from json_response_utils import build_response
import urllib.request

# Intent handlers & speech utilities --------------------------------------------------------------------------------------------
WELCOME_TEXT = "Hello! Give me a city to check for rain."
HELP_TEXT = "You can say things like, New York. Or, is it raining in Sydney Australia? When you're ready, give me a city to check for rain."
GOODBYE_TEXT = "Goodbye."
UNRECOGNIZED_CITY_TEXT = "Sorry, I didn't recognize that city. Please try again. Or say, help, for assistance."
HTTP_ERROR_TEXT = "Oops, an error occured. Please try again. Or say, exit, to quit."
STANDARD_REPROMPT = "Give me a city to check for rain. Or say, exit, to quit."

def is_it_raining_in_location(intent):
    try:
        city = intent['slots']['City']['value'].replace(' ', '-')
        location = city
    except KeyError:
        return build_response(UNRECOGNIZED_CITY_TEXT, reprompt_speech_text=STANDARD_REPROMPT)
    try:
        state = intent['slots']['State']['value'].replace(' ', '-')
        location += '-' + state
    except KeyError:
        pass
    try:
        country = intent['slots']['Country']['value'].replace(' ', '-')
        location += '-' + country
    except KeyError:
        pass

    url = "https://isitraining.in/{}".format(location)

    try:
        req = urllib.request.Request(
            url, 
            headers={
                'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3)\
                    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
            }
        )
        f = urllib.request.urlopen(req)
        html = (f.read().decode('utf-8'))

        loc_start_index = html.find("<strong>") + 8
        loc_end_index = html.find("</strong>")
        location_result = html[loc_start_index : loc_end_index]

        index = html.find("class='result'") + 15
        result = html[index]
        if (result == 'Y'):
            result = 'Yes. It is raining in {}'.format(location_result)
        else:
            result = 'No. It is not raining in {}'.format(location_result)
        return build_response(result, should_end_session=True)
    except urllib.error.HTTPError as e:
        if (e.code == 404):
            result = UNRECOGNIZED_CITY_TEXT
        else:
            result = HTTP_ERROR_TEXT
        return build_response(result, reprompt_speech_text=STANDARD_REPROMPT)


def get_help_response():
    return build_response(HELP_TEXT, reprompt_speech_text=STANDARD_REPROMPT)


def get_goodbye_response():
    return build_response(GOODBYE_TEXT, should_end_session=True)


def get_welcome_response():
    return build_response(WELCOME_TEXT, reprompt_speech_text=STANDARD_REPROMPT)
