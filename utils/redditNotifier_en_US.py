SKILL_NAME = "Reddit Notifier"
HELP_TEXT = (" Please tell me the subreddit that you want me to monitor for new posts. You can say: Monitor worldnews for new posts. \n "
             "If you want to check for new posts on one of your subreddits, you can ask: Are there new posts on worldnews? \n "
             "You can also ask me to check if any of your subreddits got new posts, by saying: Are there any updates? \n "
             "If you want to remove a subreddit from your list, you can do it, by saying: Remove worldnews from my list. \n "
             "If you want the list of your subreddits, ask, by saying: Which are my subreddits? \n "
             "If you want to check the titles of the most recent posts on a subreddit, you can say: Tell me the most recent posts on worldnews. ")
WELCOME_TEXT = "Welcome to the Reddit Notifier skill. For any information on how to use the skill, just say: Help me, or, Guide me. "
WELCOME_REPROMPT_TEXT = "You can add, monitor and delete your favourite subreddits. You can also check for the most recent posts. For any information on how to use the skill, just say: Help me, or, Guide me."

GOODBYE_TEXT = "Thank you for using Reddit Notifier. Goodbye!"

SUBREDDITS_LIST_INITIAL_INTENT_TEXT = "The subreddits that you are currently monitoring are: \n"

SUBREDDITS_MONITORING_INTENT_NO_SUBREDDITS_TEXT = ("Currently you're not monitoring any subreddit. If you want me to check a subreddit for new posts, just say: "
                "Monitor worldnews for new posts. ")
SUBREDDITS_MONITORING_INTENT_REPROMPT_TEXT = "You can ask me if there are new posts on your subreddits, by saying: Are there any new posts? "
SUBREDDITS_MONITORING_INTENT_NO_CHANGES_TEXT = "There aren't any new posts on your subreddits. "
SUBREDDITS_MONITORING_INTENT_INITIAL_CHANGES_TEXT = "The subreddits on which new posts have been submitted are: \n"
SUBREDDITS_MONITORING_INTENT_CHANGES_TEXT = "From now on I'll monitor their updated version. "

SINGLE_SUBREDDIT_MONITORING_INTENT_CHANGE_TEXT = "There are new posts on r/{}! Now I'll monitor it's new updated version. "
SINGLE_SUBREDDIT_MONITORING_INTENT_NO_CHANGE_TEXT = "There aren't any new posts on r/{}. "
SINGLE_SUBREDDIT_MONITORING_INTENT_UNKNOWN_SUBREDDIT_TEXT = "I'm not sure what subreddit you want me to check. "
SINGLE_SUBREDDIT_MONITORING_INTENT_REPROMPT_TEXT = "You can ask me if there are any new posts on a subreddit, by saying: Are there new posts on worldnews? "

SUBREDDIT_INSERTION_INTENT_SUCCESS_REPROMPT_TEXT = "You can ask me if there are new posts on your subreddit, by saying: Are there new posts on {} ?"
SUBREDDIT_INSERTION_INTENT_SUCCESS_TEXT = "Now I know that you want me to check for new posts on r/{}. "
SUBREDDIT_INSERTION_INTENT_UNKNOWN_SUBREDDIT_TEXT = "I'm not sure what your chosen subreddit is. "
SUBREDDIT_INSERTION_INTENT_UNKOWN_SUBREDDIT_REPROMPT_TEXT = "You can tell me a subreddit that you want to monitor, by saying: Monitor worldnews for new posts. "

SINGLE_SUBREDDIT_DELETION_INTENT_SUCCESS_TEXT = "I have removed r/{} from the list of your subreddits. "
SINGLE_SUBREDDIT_DELETION_INTENT_SUCCESS_REPROMPT_TEXT = "You can ask me to monitor other subreddits, by saying: My subreddit is worldnews. "
SINGLE_SUBREDDIT_DELETION_INTENT_UNKOWN_SUBREDDIT_TEXT = "This subreddit is not part of your monitored subreddits. "
SINGLE_SUBREDDIT_DELETION_INTENT_UNKOWN_SUBREDDIT_REPROMPT_TEXT = "You can tell me the subreddit that you want to delete, by saying: Remove worldnews from my list. "

SUBREDDITS_DELETION_INTENT_TEXT = "Your list of subreddits is now empty. "
SUBREDDITS_DELETION_INTENT_ADD_SUBREDDITS_TEXT = "You can add subreddits to your lists, by saying: Monitor worldnews for new posts"

SINGLE_SUBREDDIT_LAST_POSTS_INTENT_SUCCESS_REPROMPT_TEXT = "You can ask me for the most recent posts on your subreddit, by saying: Tell me the most recent posts for {}. "
SINGLE_SUBREDDIT_LAST_POSTS_INSERTION_INTENT_SUCCESS_TEXT = "The titles for the most recent posts on r/{} are: \n"
SINGLE_SUBREDDIT_LAST_POSTS_INTENT_UNKNOWN_SUBREDDIT_TEXT = "I'm not sure what your chosen subreddit is. "
SINGLE_SUBREDDIT_LAST_POSTS_INTENT_UNKOWN_SUBREDDIT_REPROMPT_TEXT = "You can tell me the subreddit for which you want the most recent posts, by saying: Tell me the most recent posts on worldnews. "

EXCEPTION_SUBREDDIT_TEXT = "Sorry, I couldn't understand your provided subreddit. "
EXCEPTION_UNKNOWN_SUBREDDIT_TEXT = "This subreddit is not part of your monitored subreddits. You can add it by saying: Monitor worldnews for new posts. "
EXCEPTION_GENERIC_TEXT = "Sorry, there was some problem. "
EXCEPTION_REPROMPT_TEXT = "For any information on how to use the skill, just say, Help me, or, Guide me. "

