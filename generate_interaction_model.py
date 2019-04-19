import json
import requests


LIMIT = 500000
counter = 0
URL = "https://www.reddit.com/subreddits.json?limit=100&after="
paging = "null"

data = requests.get("https://www.reddit.com/subreddits.json?limit=100&after=", headers = {'User-agent': 'your bot 0.1'}).json()

values = []
while counter < LIMIT:
    data = requests.get(URL + paging, headers = {'User-agent': 'your bot 0.1'}).json()

    for child in data["data"]["children"]:
        subreddit = child["data"]["url"].split("/r/")[1].strip('/')
        values.append({
            "name": {
                "value": subreddit
            }
        })
        counter += 1
        if(counter == LIMIT): break

    paging = data["data"]["after"]
    if(paging == None): break

print("Gathered {} subreddits!").format(str(counter))

types = []
types.append({
    "name": "subreddit",
    "values": values
})

json_model = {
  "interactionModel": {
    "languageModel": {
      "invocationName": "reddit notifier",
      "intents": [
        {
          "name": "AMAZON.CancelIntent",
          "samples": []
        },
        {
          "name": "AMAZON.HelpIntent",
          "samples": [
              "how to use the skill",
              "guide me",
              "help me",
              "guide",
              "help"
          ]
        },
        {
          "name": "AMAZON.StopIntent",
          "samples": [
              "exit",
              "close",
              "stop"
          ]
        },
        {
          "name": "SubredditInsertionIntent",
          "slots": [
              {
                  "name": "subreddit",
                  "type": "subreddit"
              }
          ],
          "samples": [
            "add {subreddit} to my list",
            "my subreddit is {subreddit}",
            "monitor {subreddit} for new posts"
          ]
        },
        {
          "name": "SubredditsMonitoringIntent",
          "slots": [],
          "samples": [
            "are there new posts",
            "are there new posts for my subreddits",
            "are there any changes",
            "new posts for my subreddits",
            "are there any updates"
          ]
        },
        {
            "name": "SingleSubredditDeletionIntent",
            "slots": [
                {
                    "name": "subreddit",
                    "type": "subreddit"
                }
            ],
            "samples": [
                "cancel {subreddit} from my list",
                "remove {subreddit} from my list"
            ]
        },
        {
            "name": "SingleSubredditMonitoringIntent",
            "slots": [
                {
                    "name": "subreddit",
                    "type": "subreddit"
                }
            ],
            "samples": [
                "there are new posts on {subreddit}",
                "if there are new posts on {subreddit}",
                "new posts on {subreddit}",
                "are there new posts on {subreddit}"
            ]
        },
        {
            "name": "SingleSubredditLastPostsIntent",
            "slots": [
                {
                    "name": "subreddit",
                    "type": "subreddit"
                }
            ],
            "samples": [
                "what are the most recent posts on {subreddit}",
                "the most recent posts on {subreddit}",
                "tell me the most recent posts on {subreddit}"
            ]
        },
        {
            "name": "SubredditsListIntent",
            "slots": [],
            "samples": [
                "which are my subreddits"
            ]
        }
      ],
      "types": types
    }
  }
}


with open('data.json', 'w') as outfile:
    json.dump(json_model, outfile)
