from __future__ import print_function
import json
import random

# --------------------------- Global variables ---------------------------------

totalQues = 10
quesInOneSession = 5
maxScore = quesInOneSession

score = 0
currQues = -1
askedQuesCount = 0
askedQues = []
session_attributes = {}
rulecount = 0

quesAnswered = True

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
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


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Wildlife Guru. " \
                    "Tell me your choice " \
                    "One Products "  \
                    "Two Animals " \
                    "Three NGO names "\
                    "Four Wildlife Quiz "\
                    "Five Wildlife Sanctuary Details "\
                    "Six Wildlife Facts "\
                    "Seven Wildlife Movie Suggestion "\
                    "you can tell me your choice by saying, " \
                    "my choice is one or two or three that is your choice number " \
                    "If you want to know about Wildlife Guru or need any help, you can get by saying " \
                    "help wildlife guru "
    reprompt_text = "Please tell me your choice by saying, " \
                    "my choice is one."
    
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for using Wildlife Guru. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def set_option(intent, session):

    card_title = "Menu Option"
    session_attributes = {}
    should_end_session = False

    if 'opt' in intent['slots']:
        user_choice = intent['slots']['opt']['value']
        if user_choice == "1":
            speech_output = "You can ask me about general product by saying, general product" \
                            " If you want to ask about specific product then say my product is necklace."
            reprompt_text = "You can ask me about specific product by saying, " \
                            "product is product name?"
        elif user_choice == "2":
            speech_output = "May I know about which wildlife Animal you want to know? "  \
                            "You can ask me about animal by saying, " \
                            "tell me about animal name?"
            reprompt_text = "You can ask me about animal by saying, " \
                            "tell me about animal name?"
        elif user_choice == "3":
            speech_output = "You can ask me about the NGOs related to wildlife in countries. " \
                            "You just need to say, " \
                            "tell me NGO in country name?"
            reprompt_text = "You can ask me about ngos by saying, " \
                            "tell me NGO in country name?"
        elif user_choice == "4":
            speech_output = "Hi! This is a wildlife quiz! For rules of the game, just say rules! " \
                            "Shall we find out how well you know wildlife? Say start quiz to begin" 
                    
            reprompt_text = "Hey! I am waiting! " \
                            "Shall we get started? Say begin to get started!"
        elif user_choice == "5":
            speech_output = "You can ask me about the Wildlife Sanctuaries located in various states of India." \
                            "You just need to say, " \
                            "Wildlife sanctuaries in state name"
            reprompt_text = "You can ask me about parks by saying, " \
                            "Wildlife sanctuaries in state name?"
        elif user_choice == "6":
            speech_output = "I know a lot of interesting facts about wildlife. " \
                            "You can ask me about facts by saying, " \
                            "tell me a wildlife fact?"
            reprompt_text = "You can ask me about facts by saying, " \
                            "tell me wildlife fact?"
        elif user_choice == "7":
            speech_output = "Hi, Are you a movie geek and want a suggestion about wildlife related movie." \
                            "Then You can ask me about movies by saying, " \
                            "give me a movie suggestion?"
            reprompt_text = "You can ask me about movies by saying, " \
                            "give me a movie suggestion?"
        else:
            speech_output = "I'm not sure what your choice is. "+ \
                            user_choice +" Please try again."
            reprompt_text = "I'm not sure what your choice is. " \
                            "You can tell me your choice by saying, " \
                            "my choice is one."
    else:
        speech_output = "I'm not sure what your choice is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your choice is. " \
                            "You can tell me your choice by saying, " \
                            "my option is one."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

########## ----------------     GAME CODE -------------------     ######################
def result():
    
    init = "Yay! You completed the quiz! " + " You got " + str(score) + " out of " + str(quesInOneSession) + " correct. "
    if score == quesInOneSession:
        init = init + " Perfect score! You really know wildlife! I am impressed! "
    elif score >= (quesInOneSession/1.5)+1:
        init = init + " Great score! Keep playing, keep getting better! "
    elif score >= (quesInOneSession/2.5)+1:
        init = init + " Good effort! You can do better, I believe in you! "
    else:
        init = init + " You can do better! Play again, get better!  "

    init = init + "  Wanna play again? Just say, Replay!"
    
    return (init)

def ret_question():

    q = ques[currQues] + " . "
    return (q)

def ret_options():

    o3 = ""
    o4 = ""
    
    o1 = "Option 1 . " + opA[currQues] + ". "
    o2 = "Option 2 . " + opB[currQues] + ". "

    if opC[currQues] != "":
        o3 = "Option 3 . " + opC[currQues] + ". "
        o4 = "Option 4 . " + opD[currQues] + ". "

    o = o1+o2+o3+o4
    return (o)
    

def quiz(intent, session):

    global askedQuesCount
    global currQues
    global askedQues
    global quesAnswered

    card_title = "Quiz"

    if askedQuesCount == 0:
        init = "Alright! Let us begin. "
    else:
        init = ""

    speech_output = ""
    reprompt_text = ""
    
    if askedQuesCount == quesInOneSession:
         
                speech_output = result()
                reprompt_text = " Hey! Let's play again! Say Replay to play again. Or Exit to stop playing "
                should_end_session = False

                return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))
            
    if quesAnswered == False:
        card_title = "Alert!"

        speech_output = "Hey! Answer the last question I asked you."
        reprompt_text = "Hey! I am waiting for your answer. If you missed the question, say repeat question."

        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))
             
    
    askedQuesCount = askedQuesCount+1   
    quesNo = askedQuesCount
    x =  random.randint(0,totalQues-1)
    while x in askedQues:
            x =  random.randint(0,totalQues-1)
        
    askedQues.append(x);
    currQues = x
    
    question = "Question " + str(quesNo) + ".  " + ret_question() 
    options = "Your options are. " + ret_options()
    
    session_attributes['question'] = ques[x]
    session_attributes['options']= options
    
    quesAnswered = False
    
    speech_output = init + question + options
    reprompt_text = "Hey! I am waiting for your answer. If you missed the question, say repeat question."

    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))    
    #print(b['response']['outputSpeech']['text'])
    

def convert(val):

    if val == '1':
        val = "A"
    elif val == '2':
        val = "B"
    elif val == '3':
        val = "C"
    elif val == '4':
        val = "D"
    else:
        val = "E"

    return val    
    
def convertRev(val):

    if val == "A":
        val = "1"
    elif val == "B":
        val = "2"
    elif val == "C":
        val = "3"
    else:
        val = "4"

    return val    

def get_answer(intent, session):

    global score
    global quesAnswered

    card_title = "Answer"

    if quesAnswered == True:
        speech_output = "Hey! What you trying to pull buddy? You answered the question already."
        reprompt_text = "You can know more about this question's answer by saying, tell me more, or, you can move to the next question by saying, next question."

        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))    

        
    correctAns = ans[currQues]

    if 'value' not in intent['slots']['option']:
        speech_output = "You need to select an option! Select an option."
        reprompt_text = "If you missed the options, say repeat options."

        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))
        
    ans_input = intent['slots']['option']['value']
    ans_input = convert(ans_input)

    if ans_input == "E":
        speech_output = "You need to select a valid option! Select a valid option."
        reprompt_text = "If you missed the options, say repeat options."

        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

    if ans_input == correctAns:
        speak = "That is the correct answer!" + " Say next for the next question."
        score = score + 1
    else:
        speak = "That answer is incorrect. The correct answer is option " + convertRev(correctAns) + " . Say tell me more to know about the correct answer. " 

    session_attributes['score'] = score
    
    quesAnswered = True
    speech_output = speak 
    reprompt_text = "You can know more about this question's answer by saying, tell me more. "
    
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))    


def get_next_question(intent, session):

    if quesAnswered == False:
        card_title = "Alert!"

        speech_output = "Hey! You haven't answered the question yet. You can't move to the next question."
        reprompt_text = "Hey! I am waiting for your answer. If you missed the question, say repeat question."

        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))
        
    return quiz(intent,session)

def repeat_question(intent, session):

    card_title = "Question"

    if currQues == -1:
        speech_output = "The quiz has not started yet! Say begin to start the quiz"
        reprompt_text = "Say begin to start the quiz"
        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))    
    
    if quesAnswered == True:
        speak = "Your question was. "
        re = "Say, next question, to move to the next question!"
    else:
        speak = "Your question is. "
        re = "Hey, there! I am waiting for your answer."

    speech_output = speak + ret_question() + " . Options.  " + ret_options()
    reprompt_text = re
    
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))    
    

def repeat_options(intent, session):

    card_title = "Option"

    if currQues == -1:
        speech_output = "The quiz has not started yet! Say begin to start the quiz"
        reprompt_text = "Say begin to start the quiz"
        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))    
    
    
    if quesAnswered == True:
        speak = "Your options were. "
        re = "Say, next question, to move to the next question!"
    else:
        speak = "Your options are. "
        re = "Hey, there! I am waiting for your answer."

    speech_output =  speak + ret_options()
    reprompt_text = re

    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))    

    
def current_score(intent, session):

    card_title = "Score"

    sc = str(score)
    if askedQuesCount == quesInOneSession:
        speak = "You finished the quiz! You final score is "+ sc + ". Say, replay to play again."
        re = "Say replay to start the quiz again! Or say exit to exit the game"
    else:
        if quesAnswered == True:
            speak = "Your score is " + sc + " because you have answered " + sc + " correctly, out of " + str(askedQuesCount) + " questions."
            re = "Move to the next question by saying, next question."
        else:
            speak = "Your score is " + sc + " because you have answered " + sc + " correctly, out of " + str(askedQuesCount-1) + " questions."
            re = "I am waiting for the answer! Say, repeat question, if you want me to repeat the question."

    speech_output = speak
    reprompt_text = re
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))    

def tell_me_more(intent, session):

    card_title = "Tell Me More"

    if quesAnswered == False:
        speak = "You can't know about the answer yet! Answer the question first."
        re = "I am waiting for the answer! Say, repeat question, if you want me to repeat the question."
    else:
        speak = ansInfo[currQues] + " . Say begin to continue. "
        re = "Move to the next question by saying, next question."

    speech_output = speak
    reprompt_text = re
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))  


def replay_quiz(intent, session):
    
    global score
    global currQues
    global askedQuesCount
    global askedQues
    global quesAnswered
    
    score = 0
    currQues = -1
    askedQuesCount = 0
    askedQues = []
    session_attributes = {}
    quesAnswered = True
    
    return quiz(intent, session)    


def no_response():

    card_title = "No!"
    
    speech_output = "I am sorry, I don't understand!"
    reprompt_text = "For rules, say rules!"
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))    
        
def yes_response():

    card_title = "Yes!"
    
    speech_output = "Yes yes but I don't understand!"
    reprompt_text = "For rules, say rules!"
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))    

    
def get_help_response(intent,session):
    
    global rulecount
    
    card_title = "Help"
    sessionAttributes= {}
    rulecount = rulecount + 1
    if rulecount == 1:
        speech_output = "This is a wildlife quiz and the rules are simple. " \
                        "I will ask you a question. You choose your answer by saying, Option 1, or, Option 2, etc. "\
                        "I will tell you, if you were correct. Move to the next question by saying Next! "
    else:
        speech_output = "Hi! Once Again Welcome to Wildlife Guru! " \
                        "This is a wildlife quiz and the rules are simple. " \
                        "After you start the quiz, you will be prompted with a question. "\
                        "Options for the same will be provided. You have to choose one option, by saying, Option 1, or, Option 2, or, Option 3, or, Option 4. " \
                        "After you answer the question, I will tell you, whether you were right, or not. Then say, next question, to move to the next question. "\
                        "You can get a question repeated, by saying, Repeat question. You can also get the options for a question, repeated, by saying, repeat options. "\
                        "You can also know more about the answer, of a question, by saying, tell me more. "\
                        "You will be asked 6 questions. You will get the final score after the game. To get your score between the game, you can ask, what is my score. "
        rulecount = 0                

    if askedQuesCount == 0:
        speech_output = speech_output + "That's all! We're all set to begin! Say begin to get started!"
    else:
        speech_output = speech_output + "Alright! Shall we continue? Say begin to continue!"
                    
    speech_output = speech_output + " For detailed rules, say rules again. "
    reprompt_text = "Hey there! What are you waiting for? " \
                    "Say begin!"
                    
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))



##----------------------------------    ANIMAL CODE -------------------------------#######################
def know_animal(intent, session):
    card_title = "Animal Details"
    session_attributes = {}
    should_end_session = False
    flag=0
    anima=" "
    
    if 'animal' in intent['slots']:
        user_animal = intent['slots']['animal']['value']
        for i in range(len(anim)):
            if user_animal.lower() == anim[i][0]:
                anima=anim[i][1]
                flag=1
                break
        if flag==1:
            speech_output=anima
            reprompt_text=anima
        else:
            speech_output="Sorry I don't know about this animal. You can ask for other animals. "
            reprompt_text="You can ask for animals by saying tell me about animal animal name. "
    else:
        speech_output = "I'm not sure what your animal is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your animal is. " \
                            "You can tell me your animal by saying, " \
                            "tell me about elephant."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session)) 

def park_details(intent, session):
    card_title = "Park Details"
    session_attributes = {}
    should_end_session = False
    park_ans= " " 
    
    if 'citypark' in intent['slots']:
        user_park = intent['slots']['citypark']['value']
        for i in range(len(parkk)):
            if user_park == parkk[i][0]:
                park_ans+=parkk[i][1]
        if park_ans== " ":
            speech_output= "Sorry I don't know about park in this state."
            reprompt_text = "You can now about national parks in other cities too"
        else:
            speech_output = park_ans
            reprompt_text = "You can now about national parks in other cities too"

    else:
        speech_output = "I'm not sure what your city is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your city is. "
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def wild_fact(intent, session):
    import random
    index = random.randint(0,len(wild)-1)
    card_title = "Wildlife Facts"
    session_attributes = {}
    should_end_session = False
    speech_output = "One of the interesting fact related to wildlife is " + wild[index] 
    reprompt_text = "You can know interesting facts about wildlife like by saying Tell me about wildlife"
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def set_movie(intent, session):
    import random
    index = random.randint(0,len(mov)-1)
    card_title = "Wildlife Movies"
    session_attributes = {}
    should_end_session = False
    speech_output = "One of the interesting movie related to wildlife is " + mov[index] 
    reprompt_text = "You can know interesting movies about wildlife like by saying Tell me about movie"
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def product_details(intent, session):
    card_title = "Product Details"
    session_attributes = {}
    should_end_session = False

    if 'typeof' in intent['slots']:
        user_pro = intent['slots']['typeof']['value']
        import random
        index = random.randint(0,len(pro)-1)
        speech_output = pro[index]
        reprompt_text = "You can now about genral product details too by saying general product."
    else:
        speech_output = "I'm not sure what your city is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your city is. "
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def ngo_details(intent, session):
    card_title = "NGO Details"
    session_attributes = {}
    should_end_session = False
    ngo= " "
    flag=0

    if 'cityngo' in intent['slots']:
        user_ngo = intent['slots']['cityngo']['value']
        for i in range(len(ngoo)):
            if user_ngo == ngoo[i][0]:
                ngo+=ngoo[i][1]
                flag=1
        
        if flag==1:
            speech_output=ngo
            reprompt_text=ngo
        else:
            speech_output="Sorry there is no ngo in this country. "
            reprompt_text="You can know about ngos by saying tell me ngo in country name "
    else:
        speech_output = "I'm not sure what your city is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your city is. "
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def product_general(intent, session):
    card_title = "Product General Details"
    session_attributes = {}
    should_end_session = False
    import random
    index = random.randint(0,len(gen)-1)
    speech_output = "Details about general product is "+ gen[index] 
    reprompt_text = gen[index]
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def fallback_func(intent, session):
    card_title = "Fallback"
    session_attributes = {}
    should_end_session = False
    speech_output = "Yes yes but I don't understand."
    reprompt_text = "If you are struck then you can ask for help by saying help wildlife guru."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def know_about_wildlife_guru(intent, session):
    
    session_attributes = {}
    card_title = "About Wildlife Guru"
    speech_output = "Hello, Welcome to the Wildlife Guru. " \
                    "Wildlife Guru is a single place where you come know about various wildlife related things." \
                    "You can continue your interaction with the skill by saying resume"
    reprompt_text = "You can resume back by saying" \
                    "resume"
    
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """
    global score
    global currQues
    global askedQuesCount
    global askedQues
    global quesAnswered

    session_attributes = {}
    score = 0
    currQues = -1
    askedQuesCount = 0
    askedQues = []
    quesAnswered = True
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

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "WhatIsOption":
        return set_option(intent, session)
    elif intent_name == "ProductName":
        return product_details(intent,session)
    elif intent_name == "GeneralProduct":
        return product_general(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return know_about_wildlife_guru(intent,session)
    elif intent_name== "NgoName":
        return ngo_details(intent,session)
    elif intent_name == "ResumeIntent":
        return get_welcome_response()
    elif intent_name== "MovieName":
        return set_movie(intent,session)
    elif intent_name== "ParkName":
        return park_details(intent, session)
    elif intent_name== "AnimalName":
        return know_animal(intent,session)
    elif intent_name== "WildlifeFacts":
        return wild_fact(intent,session)
    elif intent_name == "QuizIntent":
        return quiz(intent, session)
    elif intent_name == "AnswerIntent":
        return get_answer(intent, session)
    elif intent_name == "NextQuestionIntent":
        return get_next_question(intent, session)
    elif intent_name == "RepeatQuestionIntent":
        return repeat_question(intent, session)
    elif intent_name == "RepeatOptionsIntent":
        return repeat_options(intent, session)
    elif intent_name == "ReplayIntent":
        return replay_quiz(intent, session)
    elif intent_name == "WhatsMyScoreIntent":
        return current_score(intent, session)
    elif intent_name == "TellMeMoreIntent":
        return tell_me_more(intent, session)
    elif intent_name == "NoIntent":
        return no_response(intent, session)
    elif intent_name == "YesIntent":
        return yes_response()
    elif intent_name == "RuleIntent":
        return get_help_response(intent,session)
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    elif intent_name=="AMAZON.FallbackIntent":
        return fallback_func(intent,session)
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


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
   
################################# WILDLIFE FACTS ################################################        
wild = [
  'Slugs have four noses.',
  'The fingerprints of a koala are so indistinguishable from humans that they have on occasion been confused at a crime scene.',
  'A snail can sleep for three years.',
  'The heart of a shrimp is located in its head.',
  'Elephants are the only animal that can\'t jump.',
  'A rhinoceros horn is made of hair.',
  'It is possible to hypnotize a frog by placing it on its back and gently stroking its stomach.',
  'It takes a sloth two weeks to digest its food.',
  'Nearly three percent of the ice in Antarctic glaciers is penguin urine.',
  'A cow gives nearly 200,000 glasses of milk in a lifetime.',
  'Bats always turn left when leaving a cave.',
  'Giraffes have no vocal chords.',
  'An ostrich eye is bigger than its brain.',
  'Kangaroos can\'t fart.'
]

######################################ANIMALS DATA SET #########################################################
anim=[["indian rhinoceros","The Indian rhinoceros (Rhinoceros unicornis), also called the greater one-horned rhinoceros and great Indian rhinoceros, is a rhinoceros native to the Indian subcontinent. It is listed as Vulnerable on the IUCN Red List, as populations are fragmented and restricted to less than 20,000 km2 (7,700 sq mi). Moreover, the extent and quality of the rhino's most important habitat, alluvial grassland and riverine forest, is considered to be in decline due to human and livestock encroachment."],
["indian Wild Ass","The Indian wild ass also called the Ghudkhur, Khur or Indian onager in the local Gujarati language, is a subspecies of the onager native to Southern Asia. As of 2016, it is listed as Endangered by IUCN."],
["gaur","The gaur, also called the Indian bison, is the largest extant bovine. This species is native to the Indian subcontinent and Southeast Asia. It has been listed as Vulnerable on the IUCN Red List since 1986. Population decline in parts of its range is likely to be more than 70% during last three generations."],
["yak",	"The domestic yak is a long-haired domesticated bovid found throughout the Himalayan region of the Indian subcontinent, the Tibetan Plateau and as far north as Mongolia and Russia. It is descended from the wild yak."],
["sambar deer",	"The sambar is a large deer native to the Indian subcontinent, southern China, and Southeast Asia that is listed as Vulnerable on the IUCN Red List since 2008. Populations have declined substantially due to severe hunting, insurgency, and industrial exploitation of habitat."],
["chital","The cheetal (Axis axis), also known as spotted deer or axis deer, is a species of deer that is native in the Indian subcontinent. The species was first described by German naturalist Johann Christian Polycarp Erxleben in 1777. A moderate-sized deer, male chital reach nearly 90 cm (35 in) and females 70 cm (28 in) at the shoulder. While males weigh 30–75 kg (66–165 lb), the lighter females weigh 25–45 kg (55–99 lb). The species is sexually dimorphic; males are larger than females, and antlers are present only on males. The upper parts are golden to rufous, completely covered in white spots. The abdomen, rump, throat, insides of legs, ears, and tail are all white. The antlers, three-pronged, are nearly 1 m (3.3 ft) long."],
["nilgai","The nilgai or blue bull is the largest Asian antelope and is endemic to the Indian subcontinent. The sole member of the genus Boselaphus, the species was described and given its binomial name by German zoologist Peter Simon Pallas in 1766."],
["chinkara","The chinkara, also known as the Indian gazelle, is a gazelle species native to Iran, Afghanistan, Pakistan and India."],
["royal bengal tiger","They live in arid plains and hills, deserts, dry scrub and light forests. They inhabit more than 80 protected areas in India. In Pakistan, they range up to elevations of 1,500 m (4,900 ft). In Iran, they inhabit the Kavir National Park. In 2001, the Indian chinkara population was estimated at 100,000 with 80,000 living in the Thar Desert. The population in Pakistan is scattered, and has been severely reduced by hunting. Also in Iran, the population is fragmented. In Afghanistan, chinkaras are probably very rare"],
["asiatic lions","The Asiatic lion is a Panthera leo leo population in India. Its range is restricted to the Gir Forest National Park and environs in the Indian state of Gujarat. On the IUCN Red List it is listed under its former scientific name Panthera leo persica as Endangered because of its small size and area of occupancy."],
["indian leopard","The Indian leopard is a leopard subspecies widely distributed on the Indian subcontinent. The species Panthera pardus is listed as Vulnerable on the IUCN Red List because populations have declined following habitat loss and fragmentation, poaching for the illegal trade of skins and body parts, and persecution due to conflict situations"],
["snow leopard","The snow leopard or ounce is a large cat native to the mountain ranges of Central and South Asia. It is listed as Vulnerable on the IUCN Red List of Threatened Species because the global population is estimated to number less than 10,000 mature individuals and decline about 10% in the next 23 years. As of 2016, the global population was estimated at 4,678 to 8,745 mature individuals."],
["striped hyena","The striped hyena is a species of hyena native to North and East Africa, the Middle East, the Caucasus, Central Asia and the Indian subcontinent. It is listed by the IUCN as near-threatened, as the global population is estimated to be under 10,000 mature individuals which continues to experience deliberate and incidental persecution along with a decrease in its prey base such that it may come close to meeting a continuing decline of 10% over the next three generations."],
["indian wolf",	"The Indian wolf is a subspecies of grey wolf that ranges from Southwest Asia to the Indian Subcontinent. It is intermediate in size between the Tibetan and Arabian wolf, and lacks the former's luxuriant winter coat due to it living in warmer conditions. Two closely related haplotypes within this subspecies have been found basal to all other extant Canis lupus haplotypes apart from the older-lineage Himalayan wolf, and have been proposed as a separate species."],
["golden jackal","The golden jackal is a wolf-like canid that is native to Southeast Europe, Southwest Asia, South Asia, and regions of Southeast Asia. Compared with the Arabian wolf, which is the smallest of the gray wolves, the jackal is smaller and possesses shorter legs, a shorter tail, a more elongated torso, a less-prominent forehead, and a narrower and more pointed muzzle. The golden jackal's coat can vary in color from a pale creamy yellow in summer to a dark tawny beige in winter. It is listed as Least Concern on the IUCN Red List due to its widespread distribution and high density in areas with plenty of available food and optimum shelter."],
["indian wild dog",	"The Ussuri dhole, also known as the Indian wild dog, Eastern Asiatic dhole or Chinese dholeis a subspecies of dhole native to East Asia. It is widespread in the Indian subcontinent and the Indochinese Peninsula. The Ussuri dhole is also native to China, however it is probably extinct in most of its ranges in China, as well as in Mongolia and the Russian Far East."],
["bengal fox","The Bengal fox, also known as the Indian fox, is a fox endemic to the Indian subcontinent and is found from the Himalayan foothills and Terai of Nepal through southern India and from southern and eastern Pakistan to eastern India and southeastern Bangladesh."],
["sloth bear","The sloth bear is an insectivorous bear species native to the Indian subcontinent. It is listed as Vulnerable on the IUCN Red List, mainly because of habitat loss and degradation. It has also been called labiated bear because of its long lower lip and palate used for sucking insects. Compared to brown and black bears, the sloth bear is lankier, has a long, shaggy fur and a mane around the face, and long, sickle-shaped claws. It evolved from the ancestral brown bear during the Pleistocene and through convergent evolution shares features found in insect-eating mammals."],
["asian black bear","The Asian black bear, also known as the moon bear and the white-chested bear, is a medium-sized bear species native to Asia and largely adapted to arboreal life. It lives in the Himalayas, in the northern parts of the Indian subcontinent, Korea, northeastern China, the Russian Far East, the Honshū and Shikoku islands of Japan, and Taiwan. It is classified as vulnerable by the International Union for Conservation of Nature (IUCN), mostly because of deforestation and hunting for its body parts."],
["red panda","The red panda, also called the lesser panda, the red bear-cat, and the red cat-bear is a mammal native to the eastern Himalayas and southwestern China. It has reddish-brown fur, a long, shaggy tail, and a waddling gait due to its shorter front legs; it is roughly the size of a domestic cat, though with a longer body and somewhat heavier. It is arboreal, feeds mainly on bamboo, but also eats eggs, birds, and insects. It is a solitary animal, mainly active from dusk to dawn, and is largely sedentary during the day."],
["rhesus macaque","The rhesus macaque is one of the best-known species of Old World monkeys. It is listed as Least Concern in the IUCN Red List of Threatened Species in view of its wide distribution, presumed large population, and its tolerance of a broad range of habitats. Native to South, Central, and Southeast Asia, rhesus macaque have the widest geographic ranges of any nonhuman primate, occupying a great diversity of altitudes and a great variety of habitats, from grasslands to arid and forested areas, but also close to human settlements."],
["hanuman langur","Gray langurs or Hanuman langurs, the most widespread langurs of the Indian Subcontinent, are a group of Old World monkeys constituting the entirety of the genus Semnopithecus. All taxa have traditionally been placed in the single species Semnopithecus entellus. In 2001, it was recommended that several distinctive former subspecies should be given species status, so that seven species are recognized. A taxonomic classification with fewer species has also been proposed. Genetic evidence suggests that the Nilgiri langur and purple-faced langur, which usually are placed in the genus Trachypithecus, actually belong in Semnopithecus."],
["gees golden langur","Gee's golden langur, or simply the golden langur, is an Old World monkey found in a small region of western Assam, India and in the neighboring foothills of the Black Mountains of Bhutan. It is one of the most endangered primate species of India. Long considered sacred by many Himalayan people, the golden langur was first brought to the attention of the western world by the naturalist E. P. Gee in the 1950s. In a part of Bhutan, it has hybridised with the capped langur T. pileatus."],
["gray langur","Gray langurs or Hanuman langurs, the most widespread langurs of the Indian Subcontinent, are a group of Old World monkeys constituting the entirety of the genus Semnopithecus. All taxa have traditionally been placed in the single species Semnopithecus entellus. In 2001, it was recommended that several distinctive former subspecies should be given species status, so that seven species are recognized. A taxonomic classification with fewer species has also been proposed. Genetic evidence suggests that the Nilgiri langur and purple-faced langur, which usually are placed in the genus Trachypithecus, actually belong in Semnopithecus."],
["lion taled macaque","The lion-tailed macaque, or the wanderoo, is an Old World monkey endemic to the Western Ghats of South India."],
["indian crested porcupine","The Indian crested porcupine, or Indian porcupine, is a large species of hystricomorph rodent belonging to the Old World porcupine family, Hystricidae. It is native to southern Asia and the Middle East."]]



ques = ["The most important human activity, leading to the extinction of wildlife, is",
        "Identify the correct match between tiger reserve and its state",
        "Which of the following is the matching pair of a sanctuary and its main protected wild animal?",
        "Identify the correctly matched pair",
        "The breeding place of Flamingo (Hansawar) in India is most likely",
        "If we uncover half of the forest, covering of the earth, what crisis will be produced at most and at first?",
        "What is the major cause of diminishing wildlife number?",
        "Which of the following is mainly responsible for the extinction of wild life?",
        "Indri-indri lemur is found in",
        "Viable material of endangered species can be preserved by"
        ]

opA = ["pollution of air and water",
       "Manas – Assam",
       "Kaziranga-Musk deer",
       "Corbett park - Aves",
       "Runn of Kutch",
       "some species will be extincted",
       "felling of trees",
       "pollution of air and water",
       "Madagaskar",
       "gene bank"
       ]

opB = ["hunting for valuable wildlife products",
       "Corbett – Madhya Pradesh",
       "Gir-Lion",
       "Runn of Kutch – Wild ass",
       "Ghana Vihar",
       "population and ecological imbalance will rise up",
       "paucity of drinking water",
       "hunting of flesh",
       "Mauritius",
       "gene library"
       ]

opC = ["introduction of alien species",
       "Bandipur – Tamil Nadu",
       "Sunderban-Rhino",
       "Gir forest – Rhino",
       "Sambhar lake",
       "energy crisis will occur",
       "cannibalism",
       "destruction of habitats",
       "India",
       "herbarium"
       ]

opD = ["alteration and destruction of the natural habitats.",
       "Palanau – Orissa.",
       "all of these.",
       "Kajiranga-Elephant.",
       "Chilka lake.",
       "rest half forests will maintain this imbalance.",
       "habitat destruction.",
       "all of these.",
       "Sri Lanka.",
       "gene pool."
       ]

ans = ["D",
       "A",
       "B",
       "D",
       "D",
       "A",
       "D",
       "C",
       "A",
       "A"
       ]

ansInfo = ["Wildlife includes all those naturally occurring plant and animal species which are neither cultivated, or domesticated nor tamed. Several hundred organisms are endangered or on the verge of extinction. The reasons are deforestation, pollution, killing, over exploitation etc. The most important among them is deforestation or destruction of their natural habitat because it will affect the species (flora and fauna) of complete area and not only the few organisms.",
           "Manas biosphere reserve is located in Assam. To save tiger from extinction, ‘Project Tiger’ was launched in our country in 1972. Since, then the tiger population is slowly increasing. In Manas, the tiger population was 31 in 1972 and 41 in 1973. Corbett National Park is located in district Nainital of Uttaranchal. Bandipur National Park is located in district Mysore of Karnataka. Palamu is located in Chhotanagpur, Jharkhand.",
           "Gir sanctuary is a dense forest of 70 km length and 45 km width, situated in Gujarat. This forest is divided into 9 sub-divisions namely-Hiran, Shingavado, Shingavadi, Raval, Dhatervadi, Malan, Machhundari, Papatidi and Shattunji. The climate is hot and humid. The lions are the main attraction of the forest. The Gujarat Government is very keen for the protection of lion. Thus, the Gir sanctuary was extended over both vegetational zones and open area of about 140 square km in 1973 which was upgraded into a National park in 1975.",
           "Kaziranga national park is famous for one- horned rhinoceros of India. Other animals found are elephant, wild buffalo, bison, tiger, leopard, sloth bear etc. Corbett national park is famous for tigers. Gir national park is famous for the Asiatic lions. Runn of Kutch is famous for chinkara.",
           "Flamingoes are protected in Chilika lake, Orissa. Other important birds protected are water fowls, ducks, cranes, golden plovers, sandpipers etc.",
           "Deforestation will affect in different ways. Due to destruction of natural habitat, many species will get extinct. Man will be deprived of the benefits of trees and wild animals. Soil erosion will be increased. Floods and drought will become more frequent. There will also be a change in climate. Deforestation will also decrease the atmospheric humidity which will affect rainfall and makes the air hot. Economy of the forest dwelling people will be deteriorated and wild life will be adversely affected.",
           "Wildlife includes all those naturally occurring plant and animal species which are neither cultivated, or domesticated nor tamed. Several hundred organisms are endangered or on the verge of extinction. The reasons are deforestation, pollution, killing, over exploitation etc. The most important among them is deforestation or destruction of their natural habitat because it will affect the species (flora and fauna) of complete area and not only the few organisms.",
           "Pollution of air and water, hunting of flesh, destruction of habitats, all are responsible for extinction of wildlife. Among these, most important is the destruction of habitat. Wildlife includes all those naturally occurring plant and animal species which are neither cultivated, or domesticated nor tamed. Deforestation or destruction of their natural habitat will affect the species (flora and fauna) of complete area and not only the few organisms.",
           "Indri-indri lemur is found in Madagascar. It is the largest of all surviving lemurs and is best known for its beautiful song which can carry for more than 2 km. It is active during the day, feeding on canopy fruit and leaves. Today, the Indri’s number is small and dwindling due to habitat loss.",
           "Viable material of endangered species can be preserved by gene bank. Gene bank is an institute that maintains stocks of viable seeds (seed banks), live growing plants (orchards), tissue culture and frozen germplasm with the whole range of genetic variability."
           ] 
           
#####-------------------- NGO DATA --------------     ###################
ngoo=[["India","Wildlife Protection Society of India (WPSI)	"],
 ["India","World Wide Fund (WWF-India)	"],
["India","Wildlife Trust of India (WTI)	"],
["India","Friendicoes Seca	"],
["china","FON "],
["china","Greenpeace East Asia	"],
["china","Green Camel Bell	"],
["Nepal","International Centre for Integrated Mountain Development	"],
["Nepal","	National Trust for Nature Conservation	"]]

########--------------------MOVIES DATA --------------------##################
mov=["100 Million BC(2008)", "Babe (1995)", "The Call of the Wild (1923)", "The Dam Keeper (2014)",	"Earth (2007)",	"The Family of Chimps (1984)",
    "101 Dalmatians (1996)", "Babe: Pig in the City (1998)",	"Call of the Wild (1935)",	"The Daring Dobermans (1973)",	"Ed (1996)",	"Fangs of the Wild (1939)",
    "101 Dalmatians II: Patch's London Adventure (2003)",	"Back to the Sea (2012)",	"The Call of the Wild (1972)",	"Dark Tide (2012)",	"The Edge (1997)",	"Fantastic Mr. Fox (2009)",
    "102 Dalmatians (2000)",	"Backcountry (2014)",	"The Call of the Wild (1976)",	"Day of the Animals (1977)",    "Eight Below (2006)",	"Far From Home: The Adventures of Yellow Dog (1995)",
    "10,000 BC (2008)",	"Bailey's Billion$ (2005)",	"The Call of the Wild: Dog of the Yukon (1997)",	"The Day of the Dolphin (1973)",	"Empire of the Ants (1977)",	"Fattys Faithful Fido (1915)",
    "12 Days of Terror (2004)",	"Bait 3D (2012)",	"Call of the Wild (2009)",	"The Deadly Bees (1966)",	"Entertainment (2014)",	"Fattys Plucky Pup (1915)",
    "2-Headed Shark Attack (2012)",	"Balto (1995)",	"The Care Bears Movie (1985)", "The Deadly Mantis (1957)",	"Every Which Way but Loose (1978)",	"The Fearless Four (1997)",
    "3-Headed Shark Attack (2015)",	"Balto II: Wolf Quest (2002)",	"Care Bears Movie II: A New Generation (1986)", "Delicatessen (1991)", "An Extremely", "Goofy Movie (2000)",	"Felidae (1994)"
    ]
####### ---------------------- PARKS DATA ---------------------- ##############################
parkk=[["kerala","Anamudi Shola National Park"],
["karnataka","Anshi National Park	"],
["meghalaya","Balphakram National Park	"],
["madhya pradesh","Bandhavgarh National Park	"],
["karnataka","Bandipur National Park	"],
["karnataka","Bannerghatta National Park	"],
["jharkhand","Betla National Park	"],
["odisha","Bhitarkanika National Park	"],
["tripura","Bison (Rajbari) National Park	"],
["gujarat","Blackbuck National Park, Velavadar	"],
["West bengal","Buxa Tiger Reserve	"],
["andaman and nicobar islands","Campbell Bay National Park	"],
["maharashtra","Chandoli National Park	"],
["tripura","Clouded Leopard National Park	"],
["jammu and kashmir","Dachigam National Park	"],
["rajasthan","Desert National Park	"],
["Assam","Dibru-Saikhowa National Park	"],
["uttar pradesh","Dudhwa National Park	"],
["kerala","Eravkulam National Park	"],
["andaman and nicobar islands","Galathea National Park	"],
["uttarakhand","Gangotri National Park	"],
["gujarat","Gir Forest National Park	"],
["West bengal","Gorumara National Park	"],
["uttarakhand","Govind Pashu Vihar Wildlife Sanctuary	"],
["himachal pradesh","Great Himalayan National Park	"],
["maharashtra","Gugamal National Park	"],
["tamil nadu","Guindy National Park"],
["tamil nadu","Gulf of Mannar Marine National Park"],
["chhattisgarh","Guru Ghasidas (Sanjay) National Park"],
["jammu and kashmir","Hemis National Park"],
["himachal pradesh","Inderkilla National Park"],
["tamil nadu","Indra Gandhi Wildlife Sanctuary and National Park"],
["chhattisgarh","Indravati National Park"],
["West bengal","Jaldapara National Park	"],
["uttarakhand","Jim Corbett National Park"],
["haryana","Kalesar National Park"],
["madhya pradesh","Kanha National Park	"],
["chhattisgarh","Kanger Ghati National Park	"],
["telangana","Kasu Brahmananda Reddy National Park	"],
["Assam","Kaziranga National Park	"],
["manipur","Keibul Lamjao National Park	"],
["rajasthan","Keoladeo National Park	"],
["sikkim","Khangchendzonga National Park	"],
["himachal pradesh","Khirganga National Park	"],
["jammu and kashmir","Kishtwar National Park	"],
["karnataka","Kudremukh National Park	"],
["madhya pradesh","Madhav National Park	"],
["andaman and nicobar islands","Mahatma Gandhi Marine National Park	"],
["telangana","Mahavir Harina Vanasthali National Park	"],
["Assam","Manas National Park	"],
["madhya pradesh","Mandla Plant Fossils National Park	"],
["gujarat","Marine National Park, Gulf of Kutch	"],
["kerala","Mathikettan Shola National Park	"],
["andaman and nicobar islands","	Middle Button Island National Park	"],
["goa","	Mollem National Park	"],
["arunachal pradesh","	Mouling National Park	"],
["rajasthan","	Mount Abu Wildlife Sanctuary	"],
["andaman and nicobar islands","	Mount Harriet National Park	"],
["telangana","	Mrugavani National Park	"],
["tamil nadu","	Mudumalai National Park	"],
["rajasthan","	Mukundra Hills National Park	"],
["tamil nadu","	Mukurthi National Park	"],
["mizoram","	Murlen National Park	"],
["karnataka","	Nagarhole National Park	"],
["arunachal pradesh","	Namdapha National Park	"],
["Assam","	Nameri National Park	"],
["uttarakhand","	Nanda Devi National Park	"],
["maharashtra","	Navegaon National Park	"],
["West bengal","	Neora Valley National Park	"],
["meghalaya","	Nokrek National Park	"],
["andaman and nicobar islands","	North Button Island National Park	"],
["nagaland","	Ntangki National Park	"],
["Assam","	Orang National Park	"],
["kerala","	Pambadum Shola National Park	"],
["madhya pradesh","	Panna National Park	"],
["andhra pradesh","	Papikonda National Park	"],
["madhya pradesh","	Pench National Park	"],
["kerala","	Periyar National Park	"],
["mizoram","	Phawngpui Blue Mountain National Park	"],
["himachal pradesh","	Pin Valley National Park	"],
["uttarakhand","Rajaji National Park"],
["andaman and nicobar islands","Rani Jhansi Marine National Park	"],
["rajasthan","	Ranthambore National Park	"],
["andaman and nicobar islands","	Saddle Peak National Park	"],
["jammu and kashmir","	Salim Ali National Park	"],
["madhya pradesh","	Sanjay National Park"],
["maharashtra","	Sanjay Gandhi National Park	"],
["rajasthan","	Sariska Tiger Reserve	"],
["madhya pradesh","	Satpura National Park	"],
["kerala","	Silent Valley National Park	"],
["himachal pradesh","	Simbalbara National Park	"],
["manipur","	Sirohi National Park	"],
["odisha","	Simlipal National Park	"],
["West bengal","	Singalila National Park	"],
["andaman and nicobar islands","	South Button Island National Park	"],
["andhra pradesh","	Sri Venkateswara National Park	"],
["haryana","	Sultanpur National Park	"],
["West bengal","	Sundarbans National Park	"],
["maharashtra","	Tadoba National Park	"],
["uttarakhand","	Valley of Flowers National Park	"],
["bihar","	Valmiki National Park	"],
["gujarat","	Vansda National Park	"],
["madhya pradesh","	Van Vihar National Park	"]]

########## -------- General Product Info --------------- ####################
gen= [" Some	Marine Products example Reef-building Corals, Organ-pipe Corals, Black Corals, Fire Corals, Sea Fans and other highly endangered marine species including dried seahorses and pipefish; molluscs such as Nautilus, Horse’s Hoof and Horned Helmet are sold as artefacts, curios and jewellery. One report claims that thousands of tonnes of live seashells and corals are dredged from the oceans every day – many of them protected species.	",
" Some	Ivory Items example Figurines, carvings, artefacts and jewellery made from elephant tusks has endangered the future of the Asian Elephants in India and the African Elephant in Africa. Ivory continues to be smuggled to destinations in Asia for carving into decorative itmes.	",
"	ShahtooshShawls example Three to five Tibetan Antelopes (Chirus) are slaughtered to obtain sufficient wool from their soft underbelly to produce just one shahtoosh shawl.	",
"	Reptile skin bags and other accessories are user for Handbags, belts, wallets, shoes and other  products made from the skins of protected species of reptiles including snakes, crocodiles, monitor lizards etc. may be sold in clandestine markets.	",
"	Body parts and derivatives of Tiger, Leopard, Snow Leopard, Clouded Leopard and other wild cats:- Products commonly seen in illegal wildlife trade include for coats, wallets, scarves, traditional Chinese medicines, wine, etc.. Almost every part of a tiger’s body can turn up in illegal trade.	",
"	Live birds sold as pets includes the various parakeets species of India, munias, Hill Mynas, falcons, shikras, Baya Weavers, bulbuls and many other protected wild bird species. More than 450 species of the approximately 1,300 Indian species have been documented in international and domestic trade. Also, in illegal trade are non- native (exotic) species including Grey Parrots, toucans, macaws, sugarbirds and others brought illegally into India without adequate clearances.  Atleast 110 non native species are reported to be in trade in India.	",
"	Black Spotted Turtle, Indian Star Tortoise, Gangetic Softshell Turtle, Indian Flapshell Turtle, Indian Tent Turtle and many other species of tortoises and freshwater turtles are exploited for the illegal pet trade, medicines and meat.	",
"	International trade in 1290 species of orchids, timber soecies and medicinal plants in their raw forms such as logs, whole plants, crude drugs, oil and resinoid extracts is prohibited under India’s EXIM policy. Only value added products such as medicines derived from a cultivated variety of specified species ,may be allowed for export.	",
"	Mongoose hair paintbrushes and makeup brushes, perfume fixative. Incense material, and medicine made from the musk pod of musk deer and medicnes from bear bile and pangolin body parts are also among the products illegally traded.	"]


######## ---------- Necklace Info --------- ###################
pro=["Species affected is Elephant.	Legal Product Alternative is precious stone necklace. Asian elephant and  African elephant are the endangered species found in south-central and southren asia and africa",
    "Species affected is whale.	Legal Product Alternative is metal necklace.	blue whale and gray whale are a few of endangered species found in west pacific ocean",
    "Species affected is Tiger.	Legal Product Alternative is diamond necklace.	tiger are endangered species found in temprate and tropical asia",
    "Species affected is bear. Legal Product Alternative is miniature silver skull necklace.	brown bear and asiatic black bear are a few of endangered species found in china, italy, india, japan, etc",
    "Species affected is rhino. Legal Product Alternative is red pearl necklace.	black rhino and great indian rhino are a few of endangered species found in sub saharan africa and india"
    ]
