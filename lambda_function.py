# -*- coding: utf-8 -*-

import logging
import hashlib
import requests
import boto3

from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard

from utils.util import *
from utils import redditNotifier_en_US as lang_US
from utils import redditNotifier_it_IT as lang_IT

user_slot_key = "USER"
subreddit_slot_key = "SUBREDDIT"
subreddit_hash_slot_key = "SUBREDDIT_HASH"

subreddit_slot = "subreddit"

LIMIT = 5

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

dynamoDB = boto3.resource("dynamodb", region_name="eu-west-1")
table = dynamoDB.Table("RedditNotifier")

lang = None

@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    """Handler for Skill Launch."""
    # type: (HandlerInput) -> Response
    
    handler_input.response_builder.set_should_end_session(False)

    handler_input.response_builder.speak(lang.WELCOME_TEXT).ask(lang.WELCOME_REPROMPT_TEXT)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input):
    """Handler for Help Intent."""
    # type: (HandlerInput) -> Response
    
    handler_input.response_builder.set_should_end_session(False)
    
    handler_input.response_builder.speak(lang.HELP_TEXT).ask(lang.HELP_TEXT)
    return handler_input.response_builder.response


@sb.request_handler(
    can_handle_func=lambda handler_input:
        is_intent_name("AMAZON.CancelIntent")(handler_input) or
        is_intent_name("AMAZON.StopIntent")(handler_input))
def cancel_and_stop_intent_handler(handler_input):
    """Single handler for Cancel and Stop Intent."""
    # type: (HandlerInput) -> Response
    
    handler_input.response_builder.set_should_end_session(True)
    
    return handler_input.response_builder.speak(lang.GOODBYE_TEXT).response


@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input):
    """Handler for Session End."""
    # type: (HandlerInput) -> Response
    
    return handler_input.response_builder.speak(lang.GOODBYE_TEXT).response
    
@sb.request_handler(can_handle_func=is_intent_name("SubredditsListIntent"))
def subreddits_list_handler(handler_input):
    """Check if any of the provided subreddits changed
    """
    # type: (Handler) -> Response
    
    handler_input.response_builder.set_should_end_session(False)
    
    speech = lang.SUBREDDITS_MONITORING_INTENT_NO_SUBREDDITS_TEXT + lang.SUBREDDIT_INSERTION_INTENT_UNKOWN_SUBREDDIT_REPROMPT_TEXT
    reprompt = lang.SUBREDDIT_INSERTION_INTENT_UNKOWN_SUBREDDIT_REPROMPT_TEXT
    userID = str(handler_input.request_envelope.session.user.user_id)
    
    response = table.query(
        KeyConditionExpression=Key('user').eq(userID)
    )
    if(len(response) > 0 and len(response['Items']) > 0): 
        speech = lang.SUBREDDITS_LIST_INITIAL_INTENT_TEXT
        for item in response['Items']:
            subreddit = item['subreddit']
            speech = speech + "\u2022 " + subreddit + ".\n"
            speech = speech.replace("&", " and ")
            
        speech = speech + lang.SINGLE_SUBREDDIT_MONITORING_INTENT_REPROMPT_TEXT
        
    handler_input.response_builder.speak(speech).ask(reprompt)
    return handler_input.response_builder.response

@sb.request_handler(can_handle_func=is_intent_name("SubredditsMonitoringIntent"))
def subreddits_monitoring_handler(handler_input):
    """Check if any of the provided subreddits changed
    """
    # type: (Handler) -> Response
    
    handler_input.response_builder.set_should_end_session(False)
    
    speech = lang.SUBREDDITS_MONITORING_INTENT_NO_SUBREDDITS_TEXT + lang.SUBREDDITS_MONITORING_INTENT_REPROMPT_TEXT
    reprompt = lang.SUBREDDITS_MONITORING_INTENT_REPROMPT_TEXT
    userID = str(handler_input.request_envelope.session.user.user_id)
    
    response = table.query(
        KeyConditionExpression=Key('user').eq(userID)
    )

    print(response['Items'])

    if(len(response['Items']) > 0): 
        speech = lang.SUBREDDITS_MONITORING_INTENT_INITIAL_CHANGES_TEXT
        changesCounter = 0
        
        for item in response['Items']:
            subreddit = item['subreddit']
            subreddit_hash = item['subreddit_hash']
            sub_reddit_changed, new_subreddit_hash = subreddit_changed(subreddit, subreddit_hash)
            if(sub_reddit_changed):
                changesCounter += 1
                speech = speech + "\u2022 " + subreddit + ".\n"
                speech = speech.replace("&", " and ")
                
                response = table.update_item(
                    Key={
                        'user': userID,
                        'subreddit':subreddit
                    },
                    UpdateExpression="set subreddit_hash = :sh",
                    ExpressionAttributeValues={
                        ':sh': new_subreddit_hash
                    },
                    ReturnValues="UPDATED_NEW"
                )
            
                logger.info("UpdateItem succeeded:")
        
        speech = speech + lang.SUBREDDITS_MONITORING_INTENT_REPROMPT_TEXT  
            
    if( len(response) > 0 and len(response['Items']) > 0 and changesCounter == 0) :
        speech = lang.SUBREDDITS_MONITORING_INTENT_NO_CHANGES_TEXT + lang.SUBREDDITS_MONITORING_INTENT_REPROMPT_TEXT
        
    
    handler_input.response_builder.speak(speech).ask(reprompt)
    return handler_input.response_builder.response
    
@sb.request_handler(can_handle_func=is_intent_name("SingleSubredditMonitoringIntent"))
def single_subreddit_monitoring_handler(handler_input):
    """Check if subreddit is provided in slot values. If provided, then
    check if it changed.
    If not, then it asks the user to provide the subreddit.
    """
    # type: (HandlerInput) -> Response
    
    handler_input.response_builder.set_should_end_session(False)
    
    slots = handler_input.request_envelope.request.intent.slots

    if subreddit_slot in slots:
        
        #if we don't have a value raise an error
        if(slots[subreddit_slot].value is None): raise TypeError
        
        if(slots[subreddit_slot].resolutions.resolutions_per_authority[0].values is None):
           subreddit_to_check = slots[subreddit_slot].value.replace(" ","")
        else:
            subreddit_to_check = slots[subreddit_slot].resolutions.resolutions_per_authority[0].values[0].value.name
        
        subreddit_to_check = subreddit_to_check.lower()
        #we first try with the best authoritative resolution, if empty try with the provided value
        
        userID = str(handler_input.request_envelope.session.user.user_id)
        
        try:
            response = table.get_item(
                Key={
                    'user':userID,
                    'subreddit': subreddit_to_check
                    }
            )
        except ClientError as e:
            logger.info("error is " + e.response['Error']['Message'])
        else:

            if('Item' not in response.keys()):
            
                raise KeyError
                                
            logger.info("response contains Item :" + 'Item' in response.keys())
            subreddit = response['Item']['subreddit']
            subreddit_hash = response['Item']['subreddit_hash']
            logger.info("GetItem succeded:")
            
            reprompt = lang.SINGLE_SUBREDDIT_MONITORING_INTENT_REPROMPT_TEXT
            
            sub_reddit_changed, new_subreddit_hash = subreddit_changed(subreddit, subreddit_hash)
            if(not sub_reddit_changed):
                speech = lang.SINGLE_SUBREDDIT_MONITORING_INTENT_NO_CHANGE_TEXT.format(subreddit) + lang.SINGLE_SUBREDDIT_MONITORING_INTENT_REPROMPT_TEXT
            else:
                speech = lang.SINGLE_SUBREDDIT_MONITORING_INTENT_CHANGE_TEXT.format(subreddit) + lang.SINGLE_SUBREDDIT_LAST_POSTS_INTENT_SUCCESS_REPROMPT_TEXT.format(subreddit)
                
                response = table.update_item(
                    Key={
                        'user': userID,
                        'subreddit':subreddit
                    },
                    UpdateExpression="set subreddit_hash = :sh",
                    ExpressionAttributeValues={
                        ':sh': new_subreddit_hash
                    },
                    ReturnValues="UPDATED_NEW"
                )
        
                logger.info("UpdateItem succeeded:")

    else:
        speech = lang.SINGLE_SUBREDDIT_MONITORING_INTENT_UNKNOWN_SUBREDDIT_TEXT + lang.SINGLE_SUBREDDIT_MONITORING_INTENT_REPROMPT_TEXT
        reprompt = lang.SINGLE_SUBREDDIT_MONITORING_INTENT_REPROMPT_TEXT

    handler_input.response_builder.speak(speech).ask(reprompt)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("SubredditInsertionIntent"))
def subreddit_insertion_handler(handler_input):
    """Check if subreddit is provided in slot values. If provided, then
    add it to the list of subreddits.
    If not, then it asks the user to provide the subreddit.
    """
    # type: (HandlerInput) -> Response
    
    handler_input.response_builder.set_should_end_session(False)
    
    slots = handler_input.request_envelope.request.intent.slots

    if subreddit_slot in slots:
        
        if(slots[subreddit_slot].value is None): raise TypeError
        
        if(slots[subreddit_slot].resolutions.resolutions_per_authority[0].values is None):
           chosen_subreddit = slots[subreddit_slot].value.replace(" ","")
        else:
            chosen_subreddit = slots[subreddit_slot].resolutions.resolutions_per_authority[0].values[0].value.name
        
        chosen_subreddit = chosen_subreddit.lower()
        
        speech = lang.SUBREDDIT_INSERTION_INTENT_SUCCESS_TEXT.format(chosen_subreddit) + lang.SUBREDDIT_INSERTION_INTENT_SUCCESS_REPROMPT_TEXT.format(chosen_subreddit)
        reprompt = lang.SUBREDDIT_INSERTION_INTENT_SUCCESS_REPROMPT_TEXT.format(chosen_subreddit)

        user_id = str(handler_input.request_envelope.session.user.user_id)
        
        subreddit_rss = feedparser.parse("https://www.reddit.com/r/" + chosen_subreddit + "/.rss")
        if(not subreddit_rss.has_key('entries') or len(subreddit_rss.entries) == 0): raise TypeError

        to_hash = ""
        entries_length = len(subreddit_rss.entries)
        
        for index in range(LIMIT):
            if index < entries_length:
                to_hash += subreddit_rss.entries[index].updated
        
        subreddit_hash = str(hashlib.md5( (to_hash).encode('utf-8') ).hexdigest())

        response = table.put_item(
            Item={
                'user': user_id,
                'subreddit': chosen_subreddit,
                'subreddit_hash': subreddit_hash
            }
        )

        logger.info("PutItem succeeded:")
        #logger.info(json.dumps(response, indent=4, cls=DecimalEncoder))
        
    else:
        speech = lang.SUBREDDIT_INSERTION_INTENT_UNKNOWN_SUBREDDIT_TEXT + lang.SUBREDDIT_INSERTION_INTENT_UNKOWN_SUBREDDIT_REPROMPT_TEXT
        reprompt = lang.SUBREDDIT_INSERTION_INTENT_UNKOWN_SUBREDDIT_REPROMPT_TEXT

    handler_input.response_builder.speak(speech).ask(reprompt)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("SingleSubredditDeletionIntent"))
def single_subreddit_deletion_handler(handler_input):
    """Deletes one of the stored subreddits.
    """
    # type: (HandlerInput) -> Response
    
    handler_input.response_builder.set_should_end_session(False)
    
    slots = handler_input.request_envelope.request.intent.slots

    if subreddit_slot in slots:
        
        if(slots[subreddit_slot].value is None): raise TypeError
        
        if(slots[subreddit_slot].resolutions.resolutions_per_authority[0].values is None):
           subreddit_to_delete = slots[subreddit_slot].value.replace(" ","")
        else:
            subreddit_to_delete = slots[subreddit_slot].resolutions.resolutions_per_authority[0].values[0].value.name
        
        subreddit_to_delete = subreddit_to_delete.lower()
        
        speech = lang.SINGLE_SUBREDDIT_DELETION_INTENT_SUCCESS_TEXT.format(subreddit_to_delete) + lang.SINGLE_SUBREDDIT_DELETION_INTENT_SUCCESS_REPROMPT_TEXT
        reprompt = lang.SINGLE_SUBREDDIT_DELETION_INTENT_SUCCESS_REPROMPT_TEXT
        
        userID = str(handler_input.request_envelope.session.user.user_id)
        
        try:
            response = table.get_item(
                Key={
                    'user':userID,
                    'subreddit': subreddit_to_delete
                    }
            )
        except ClientError as e:
            logger.info("error is " + e.response['Error']['Message'])
        else:
            if('Item' not in response.keys()): #if we didn't find the subreddit we say it to the user
                    
                speech = lang.SINGLE_SUBREDDIT_DELETION_INTENT_UNKOWN_SUBREDDIT_TEXT + lang.SINGLE_SUBREDDIT_DELETION_INTENT_UNKOWN_SUBREDDIT_REPROMPT_TEXT
                reprompt = lang.SINGLE_SUBREDDIT_DELETION_INTENT_UNKOWN_SUBREDDIT_REPROMPT_TEXT

                handler_input.response_builder.speak(speech).ask(reprompt)
                return handler_input.response_builder.response
                
                                
            else: # we have found the single item
        
                response = table.delete_item(
                    Key={
                        'user': userID,
                        'subreddit': subreddit_to_delete
                    }
                )

                print("DeleteItem succeeded:")
        
    else:
        speech = lang.SINGLE_SUBREDDIT_DELETION_INTENT_UNKOWN_SUBREDDIT_TEXT + lang.SINGLE_SUBREDDIT_DELETION_INTENT_UNKOWN_SUBREDDIT_REPROMPT_TEXT
        reprompt = lang.SINGLE_SUBREDDIT_DELETION_INTENT_UNKOWN_SUBREDDIT_REPROMPT_TEXT

    handler_input.response_builder.speak(speech).ask(reprompt)
    return handler_input.response_builder.response

@sb.request_handler(can_handle_func=is_intent_name("SingleSubredditLastPostsIntent"))
def _intent_handler(handler_input):
    """Reads the the last 5 posts of your chosen subreddit
    """
    # type: (HandlerInput) -> Response
    
    handler_input.response_builder.set_should_end_session(False)

    slots = handler_input.request_envelope.request.intent.slots

    if subreddit_slot in slots:

        if(slots[subreddit_slot].value is None): raise TypeError
        
        if(slots[subreddit_slot].resolutions.resolutions_per_authority[0].values is None):
           chosen_subreddit = slots[subreddit_slot].value.replace(" ","")
        else:
            chosen_subreddit = slots[subreddit_slot].resolutions.resolutions_per_authority[0].values[0].value.name

        chosen_subreddit = chosen_subreddit.lower()

        speech = lang.SINGLE_SUBREDDIT_LAST_POSTS_INSERTION_INTENT_SUCCESS_TEXT.format(chosen_subreddit)
        reprompt = lang.SINGLE_SUBREDDIT_LAST_POSTS_INTENT_UNKOWN_SUBREDDIT_REPROMPT_TEXT

        subreddit_rss = feedparser.parse("https://www.reddit.com/r/" + chosen_subreddit + "/.rss")
        if(len(subreddit_rss.entries) == 0): raise TypeError

        counter = 0
        print(len(subreddit_rss.entries))
        for entry in subreddit_rss.entries:
            
            if(entry.title[-1] != '.' and entry.title[-1] != '?'): entry.title = entry.title + "."
            speech = speech + "\u2022 " + entry.title + " \n "
            speech = speech.replace("&", " and ")
            
            if counter == 5: break
            counter += 1

        speech = speech + reprompt
        
    else:
        speech = lang.SINGLE_SUBREDDIT_LAST_POSTS_INTENT_UNKNOWN_SUBREDDIT_TEXT + lang.SINGLE_SUBREDDIT_LAST_POSTS_INTENT_UNKOWN_SUBREDDIT_REPROMPT_TEXT
        reprompt = lang.SINGLE_SUBREDDIT_LAST_POSTS_INTENT_UNKOWN_SUBREDDIT_REPROMPT_TEXT

    handler_input.response_builder.speak(speech).ask(reprompt)
    return handler_input.response_builder.response

@sb.request_handler(can_handle_func=is_intent_name("AMAZON.FallbackIntent"))
def fallback_handler(handler_input):
    """AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    handler_input.response_builder.set_should_end_session(False)
    # type: (HandlerInput) -> Response
    speech = (
        "The {} skill can't help you with that.  "
        "You can tell me your subreddit to monitor ,by saying: "
        "Monitor example for new posts. ").format(lang.SKILL_NAME)
    reprompt = ("You can tell me your subreddit ,by saying,:"
                "My subreddit is example. ")
    handler_input.response_builder.speak(speech).ask(reprompt)
    return handler_input.response_builder.response


@sb.global_response_interceptor()
def add_card(handler_input, response):
    """Add a card by translating ssml text to card content."""
    # type: (HandlerInput, Response) -> None
    response.card = SimpleCard(
        title=lang.SKILL_NAME,
        content=convert_speech_to_text(response.output_speech.ssml))


@sb.global_response_interceptor()
def log_response(handler_input, response):
    """Log response from alexa service."""
    # type: (HandlerInput, Response) -> None
    print("Alexa Response: {}\n".format(response))


@sb.global_request_interceptor()
def log_request(handler_input):
    """Log request to alexa service."""
    # type: (HandlerInput) -> None
    print("Alexa Request: {}\n".format(handler_input.request_envelope.request))
    
    request_locale = handler_input.request_envelope.request.locale
    global lang
    if(request_locale == 'it-IT'):
        lang = lang_IT
    else:
        lang = lang_US

@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input, exception):
    handler_input.response_builder.set_should_end_session(False)
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    # type: (HandlerInput, Exception) -> None
    print("Encountered following exception: {}".format(exception))
    print("of type: {}".format(exception.__class__.__name__))
    speech = ""
    if(exception.__class__.__name__ == "TypeError"):
        speech = lang.EXCEPTION_SUBREDDIT_TEXT + lang.EXCEPTION_REPROMPT_TEXT
    elif(exception.__class__.__name__ == "KeyError"):
        speech = lang.EXCEPTION_UNKNOWN_SUBREDDIT_TEXT
    else:
        speech = lang.EXCEPTION_GENERIC_TEXT + lang.EXCEPTION_REPROMPT_TEXT

    handler_input.response_builder.speak(speech).ask(lang.EXCEPTION_REPROMPT_TEXT)

    return handler_input.response_builder.response


# Handler to be provided in lambda console.
lambda_handler = sb.lambda_handler()