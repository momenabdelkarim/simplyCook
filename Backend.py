from __future__ import print_function
import urllib2
import json

breakfastImageUrl = "eh"
lunchImageUrl = "nah"
dinnerImageUrl = "lolkk"
breakfastID = ""
breakfastName = ""
iterator = 0


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the simplyCook! " \
                    "Tell me you would like me to create a meal plan for you."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Go ahead, ask me to create a meal plan for you."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the simply Cook. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


'''def create_favorite_color_attributes(favorite_color):
    return {"favoriteColor": favorite_color}


def set_color_in_session(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'Color' in intent['slots']:
        favorite_color = intent['slots']['Color']['value']
        session_attributes = create_favorite_color_attributes(favorite_color)
        speech_output = "I now know your favorite color is " + \
                        favorite_color + \
                        ". You can ask me your favorite color by saying, " \
                        "what's my favorite color?"
        reprompt_text = "You can ask me your favorite color by saying, " \
                        "what's my favorite color?"
    else:
        speech_output = "I'm not sure what your favorite color is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your favorite color is. " \
                        "You can tell me your favorite color by saying, " \
                        "my favorite color is red."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_color_from_session(intent, session):
    session_attributes = {}
    reprompt_text = None

    if session.get('attributes', {}) and "favoriteColor" in session.get('attributes', {}):
        favorite_color = session['attributes']['favoriteColor']
        speech_output = "Your favorite color is " + favorite_color + \
                        ". Goodbye."
        should_end_session = True
    else:
        speech_output = "I'm not sure what your favorite color is. " \
                        "You can say, my favorite color is red."
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))'''


# --------------- Events ------------------

def i_want_meal_plan():
    jsonfile = urllib2.Request(
        "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/mealplans/generate?diet=vegetarian&exclude=shellfish%2C+olives&targetCalories=2000&timeFrame=day",
        headers={
            "X-Mashape-Key": "p3By8mDNoNmshS3rQti74BtmfPl0p1ea8JLjsncAHuTCL3oDBd",
            "Accept": "application/json"
        }
    )

    response = urllib2.urlopen(jsonfile)
    dictionarymeal = json.load(response)

    global breakfastImageUrl, lunchImageUrl, dinnerImageUrl

    breakfastImageUrl = "https://spoonacular.com/recipeImages/"
    for x in range(0, len(dictionarymeal['meals'][0]['image'])):
        breakfastImageUrl += dictionarymeal['meals'][0]['image'][x]

    lunchImageUrl = "https://spoonacular.com/recipeImages/"
    for x in range(0, len(dictionarymeal['meals'][1]['image'])):
        lunchImageUrl += dictionarymeal['meals'][1]['image'][x]

    dinnerImageUrl = "https://spoonacular.com/recipeImages/"
    for x in range(0, len(dictionarymeal['meals'][2]['image'])):
        dinnerImageUrl += dictionarymeal['meals'][2]['image'][x]

    global breakfastID
    breakfastID = dictionarymeal['meals'][0]['id']

    global breakfastName
    breakfastName = dictionarymeal['meals'][0]['title']

    cooktime = 0
    for x in range(0, 2):
        singletimeneeded = dictionarymeal['meals'][0]['readyInMinutes']
        cooktime = cooktime + singletimeneeded

    speech_output = "You are having " + dictionarymeal['meals'][0]['title'] + " for breakfast. It takes " + str(
        dictionarymeal['meals'][0]['readyInMinutes']) + " minutes to cook. " + \
                    "Then, you are having " + dictionarymeal['meals'][1]['title'] + " for lunch. It takes " + str(
        dictionarymeal['meals'][1]['readyInMinutes']) + " minutes to cook. " + \
                    "Lastly, you are having " + dictionarymeal['meals'][2]['title'] + " for dinner. It takes " + str(
        dictionarymeal['meals'][2]['readyInMinutes']) + " minutes to cook. " + "Overall, it will take you " + str(
        cooktime) + " minutes of your time to cook today."

    session_attributes = {}
    card_title = "Here's your meal plan for today."
    reprompt_text = ""
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def i_want_first_meal():
    global iterator
    global breakfastID

    jsonfile = urllib2.Request(
        "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/mealplans/generate?diet=vegetarian&exclude=shellfish%2C+olives&targetCalories=2000&timeFrame=day",
        headers={
            "X-Mashape-Key": "p3By8mDNoNmshS3rQti74BtmfPl0p1ea8JLjsncAHuTCL3oDBd",
            "Accept": "application/json"
        }
    )

    response = urllib2.urlopen(jsonfile)
    dictionarymeal = json.load(response)

    global breakfastID
    breakfastID = dictionarymeal['meals'][0]['id']

    global breakfastName
    breakfastName = dictionarymeal['meals'][0]['title']

    url1 = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/" + str(
        breakfastID) + "/analyzedInstructions?stepBreakdown=false"

    jsonfile2 = urllib2.Request(url1,
                                headers={
                                    "X-Mashape-Key": "p3By8mDNoNmshS3rQti74BtmfPl0p1ea8JLjsncAHuTCL3oDBd",
                                    "Accept": "application/json"
                                }
                                )

    response2 = urllib2.urlopen(jsonfile2)
    dictionarymeal2 = json.load(response2)

    ingredients = ""

    lensteps = len(dictionarymeal2[0]['steps'])

    # [1]['ingredients']

    stepss = []

    for x in range(0, lensteps):
        lening = len(dictionarymeal2[0]['steps'][x]['ingredients'])
        # stepss[x].append("Step"+str(x))
        # ingredients =ingredients+ "Step"+str(x)+" "
        for y in range(0, lening):
            ingredients += dictionarymeal2[0]['steps'][x]['ingredients'][y]['name'] + ", "

    lensteps = len(dictionarymeal2[0]['steps'])  # [1]['ingredients']

    # print dictionarymeal2[0]['steps'][1]['ingredients'][0]['name']
    stepss = []

    for x in range(0, lensteps):
        lening = len(dictionarymeal2[0]['steps'][x]['ingredients'])
        stepss.append(dictionarymeal2[0]['steps'][x]['step'])

        # tstep = stepss.split("|")




        speech_output = "The ingredients you need for this recipe are: " + ingredients

    session_attributes = {}
    card_title = "Current Step"
    reprompt_text = ""
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def show_steps():
    global iterator
    global breakfastID

    jsonfile = urllib2.Request(
        "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/mealplans/generate?diet=vegetarian&exclude=shellfish%2C+olives&targetCalories=2000&timeFrame=day",
        headers={
            "X-Mashape-Key": "p3By8mDNoNmshS3rQti74BtmfPl0p1ea8JLjsncAHuTCL3oDBd",
            "Accept": "application/json"
        }
    )

    response = urllib2.urlopen(jsonfile)
    dictionarymeal = json.load(response)

    global breakfastID
    breakfastID = dictionarymeal['meals'][0]['id']

    global breakfastName
    breakfastName = dictionarymeal['meals'][0]['title']

    url1 = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/" + str(
        breakfastID) + "/analyzedInstructions?stepBreakdown=false"

    jsonfile2 = urllib2.Request(url1,
                                headers={
                                    "X-Mashape-Key": "p3By8mDNoNmshS3rQti74BtmfPl0p1ea8JLjsncAHuTCL3oDBd",
                                    "Accept": "application/json"
                                }
                                )

    response2 = urllib2.urlopen(jsonfile2)
    dictionarymeal2 = json.load(response2)

    ingredients = ""

    lensteps = len(dictionarymeal2[0]['steps'])

    # [1]['ingredients']

    stepss = []

    for x in range(0, lensteps):
        lening = len(dictionarymeal2[0]['steps'][x]['ingredients'])
        # stepss[x].append("Step"+str(x))
        # ingredients =ingredients+ "Step"+str(x)+" "
        for y in range(0, lening):
            ingredients += dictionarymeal2[0]['steps'][x]['ingredients'][y]['name'] + ", "

    lensteps = len(dictionarymeal2[0]['steps'])  # [1]['ingredients']

    # print dictionarymeal2[0]['steps'][1]['ingredients'][0]['name']
    stepss = []

    for x in range(0, lensteps):
        lening = len(dictionarymeal2[0]['steps'][x]['ingredients'])
        stepss.append(dictionarymeal2[0]['steps'][x]['step'])

        # tstep = stepss.split("|")

    currentStep = stepss[0]

    speech_output = "The next step is to " + currentStep

    session_attributes = {}
    card_title = "Current Step"
    reprompt_text = ""
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


###########s
def i_want_a_joke():
    speech_output = "Why did the hackers eat their programs? Because the teacher said that it was a piece of cake."
    session_attributes = {}
    card_title = "Current Step"
    reprompt_text = ""
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """
    global iterator
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "Hungry":
        return i_want_meal_plan()
    elif intent_name == "FirstMeal":
        return i_want_first_meal()
    elif intent_name == "Humor":
        return i_want_a_joke()
    elif intent_name == "NextStep":
        iterator = 0
        return show_steps()
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'image': {
                'smallImageUrl': breakfastImageUrl,
                'largeImageUrl': breakfastImageUrl
            },
            'type': 'Standard',
            'title': "First up on today's meal plan!",
            'content': "Description - " + output

        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
