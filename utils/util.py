import logging
import json
import decimal
import hashlib
import requests
import feedparser
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

LIMIT = 5

def subreddit_changed(subreddit, old_hash):
    subreddit_rss = feedparser.parse("https://www.reddit.com/r/" + subreddit + "/.rss")
    
    to_hash = ""
    entries_length = len(subreddit_rss.entries)
    
    for index in range(LIMIT):
        if index < entries_length:
            to_hash += subreddit_rss.entries[index].updated
    
    new_subreddit_hash = str(hashlib.md5( (to_hash).encode('utf-8') ).hexdigest())
    return new_subreddit_hash != old_hash, new_subreddit_hash
    
# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def convert_speech_to_text(ssml_speech):
    """convert ssml speech to text, by removing html tags."""
    # type: (str) -> str
    s = SSMLStripper()
    s.feed(ssml_speech)
    return s.get_data()

######## Convert SSML to Card text ############
# This is for automatic conversion of ssml to text content on simple card
# You can create your own simple cards for each response, if this is not
# what you want to use.

from six import PY2
try:
    from HTMLParser import HTMLParser
except ImportError:
    from html.parser import HTMLParser


class SSMLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.full_str_list = []
        if not PY2:
            self.strict = False
            self.convert_charrefs = True

    def handle_data(self, d):
        self.full_str_list.append(d)

    def get_data(self):
        return ''.join(self.full_str_list)

################################################