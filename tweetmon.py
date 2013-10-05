from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

from lore_api import LoreAPI

# Twitter stuff. TODO: Load this from config. -Vikram
CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""

# Lore stuff. TODO: Load this from config. -Vikram
LORE_API_SCHEME = ""
LORE_API_HOST = ""
LORE_API_AUTH_TOKEN = ""

# TODO: Make this an arg. -Vikram
TWITTER_USER_ID_TO_MONITOR = 950395704

class HashtagMonitor(StreamListener):
    """A StreamListener that monitors tweets mentioning a given user for hashtags.
    Clients pass in a callback to handle these hashtags."""
    
    def __init__(self, user_id_to_monitor, handle_status_callback):
        """ user_id_to_monitor: a valid Twitter user handle

            handle_status_callback: a callback that takes 
            (hashtag, originating_twitter_user_id, tweet) as parameters.
            
            The client callback will be invoked on every hashtag in a tweet
            that mentions it."""
                       
        StreamListener.__init__(self)
        self.user_id_to_monitor = user_id_to_monitor
        self.handle_status = handle_status_callback

    def on_status(self, status):
        is_mention = False

        for mention in status.entities["user_mentions"]:
            print "<HashtagMonitor> %s" % mention["screen_name"]
            print "<HashtagMonitor> %s" % str(mention["id"])
            if mention["id"] == self.user_id_to_monitor:
                is_mention = True
                break

        # We don't care about tweets that don't mention the user we're monitoring.
        if not is_mention:
            print "<HashtagMonitor> We are not mentioned in this tweet. Bail."
            return

        for hashtag_entity in status.entities["hashtags"]:
            hashtag = hashtag_entity["text"]
            user_id = status.user.id
            message = status.text
            self.handle_status(hashtag, user_id, message)

    # TODO: Deal with all this error handling. -Vikram

    def on_limit(self, track):
        print "LIMIT REACHED"
        print track

    def on_error(self, status_code):
        print "ERROR"
        print status_code

    def on_timeout(self):
        print "TIMEOUT"

def get_status_handler():
    api = LoreAPI(LORE_API_SCHEME, LORE_API_HOST, LORE_API_AUTH_TOKEN)

    def post_tweet_to_course(url_name, twitter_user_id, tweet):
        print "<post_tweet_to_course> Handling %s, %d, '%s'" % (url_name, twitter_user_id, tweet)

        # Bail if the hashtag doesn't correspond to a course.
        response = api.get_course_by_url_name(url_name)
        if response.status_code != 200:
            return
        course_id = response.json["result"]["target"]["id"]

        # Bail if the twitter user doesn't correspond to a course.
        lore_user_id = api.get_lore_user_id(twitter_user_id)
        if not lore_user_id:
            return

        # TODO: What if this fails?
        print "Posting Tweet to course %d, authored by %d" % (course_id, lore_user_id)
        response = api.post_text_to_course(tweet, course_id, lore_user_id)
        print "Post response: %d" % (response.status_code)

    return post_tweet_to_course

if __name__ == "__main__":
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    hashtag_monitor = HashtagMonitor(TWITTER_USER_ID_TO_MONITOR, get_status_handler())
    stream = Stream(auth, hashtag_monitor)
    stream.userstream()


