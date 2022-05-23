from tweepy import *
from datetime import datetime, timezone
from collections import Counter
import sys
import os

from dotenv import load_dotenv #storing env variables in .env file
load_dotenv()

consumer_key=os.environ.get("key")
consumer_secret=os.environ.get("secret-key")
access_token = os.environ.get("access-token")
access_token_secret = os.environ.get("access-token-secret")

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
auth_api = API(auth, wait_on_rate_limit=False)

"""
Parameters: 
----------------
target : string
    screen name of user

Output:
----------------
No exceptions
    "ID: <user id>"
    "Grabbing data from: <screen_name>"
Exception
    "User not found"

"""
def verify(target):
    try:
        u = auth_api.get_user(screen_name=target)
        print("ID:", u.id_str)
        print("Grabbing data from: ", u.screen_name)

    except Exception:
        print("User not found")
        sys.exit(1)


"""
Parameters: 
----------------
target : string
    screen name of user

Returns:
----------------
dct : dictionary
    contains dictionary format of User variables
"""

def dictify(target):
    dct = {}
    pii = {}
    try:
        user = User(target)
    except Exception:
        print('Possible rate limit exceeded. Please try again in 15 minutes.')
        sys.exit(1)

    pii['screen_name'] = user.user
    pii['name'] = user.name
    pii['description'] = user.desc
    pii['follower_count'] = user.follower_count
    pii['age'] = user.age

    dct['PII'] = pii
    dct['most retweeted'] = user.tws
    dct['most user retweeted'] = user.rtws
    dct['common hashtags'] = user.hashtags
    dct['followers'] = user.followers
    dct['new followers'] = user.new_followers

    return dct
    

class User:
      
    def __init__(self, target, load=False):

        if not load:
            self.target = target
            
            self.item = auth_api.get_user(screen_name=target)        
            self.name = self.item.name
            self.user = self.item.screen_name
            self.desc = self.item.description
            self.follower_count = self.item.followers_count
            self.age = (datetime.now(timezone.utc) - self.item.created_at).days
            
            self.tws, self.rtws, self.hashtags = self.retweets()
            
            self.followers = self.get_followers()
            self.new_followers = self.get_new_followers()

        else:
            dct = target

            pii = dct['PII']
            self.user = pii['screen_name'] 
            self.name = pii['name']
            self.desc = pii['description']
            self.follower_count = pii['follower_count']
            self.age = pii['age']

            self.tws = dct['most retweeted']
            self.rtws = dct['most user retweeted'] 
            self.hashtags = dct['common hashtags'] 
            self.followers = dct['followers'] 
            self.new_followers = dct['new followers']
        
    
    def retweets(self):
        tweets = Cursor(auth_api.user_timeline, screen_name=self.user).items()
        tws = []
        rtws = []
        ht = {}
        
        for tw in tweets:
            if hasattr(tw, 'retweeted_status'):
                rtws.append((tw.text, tw.retweet_count, tw.created_at.strftime("%m/%d/%Y, %H:%M:%S")))
            else:
                tws.append((tw.text, tw.retweet_count, tw.created_at.strftime("%m/%d/%Y, %H:%M:%S")))
                
            for h in tw.entities['hashtags']:
                if h['text'] in ht:
                    ht[h['text']] += 1
                else:
                    ht[h['text']] = 1
                    
        if len(ht) >= 5:
            ht = dict(Counter(ht).most_common(5))
                
        tws.sort(key = lambda x: x[1])
        rtws.sort(key = lambda x: x[1])
        
        if len(rtws) < 5 and len(tws) < 5:
            return tws, rtws, ht
        
        if len(rtws) < 5:
            return tws[-6:-1], rtws, ht
        
        if len(tws) < 5:
            return tws, rtws[-6:-1], ht
            
        return tws[-6:-1], rtws[-6:-1], ht
    
    def get_followers(self):
        followers = []
        fcall = Cursor(auth_api.get_followers, screen_name=self.user).items(50)
        
        for fol in fcall:
            followers.append(fol.screen_name)
            
        return followers
    
    def get_new_followers(self):
        if len(self.followers) < 10:
            return self.followers
        return self.followers[0:10]

