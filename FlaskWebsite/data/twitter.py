import tweepy
import datetime
import pytz
import pandas as pd
import emoji
import re

def get_tweets(twitterId, dateFrom, dateTo):
    api_key = "MmiVY1qtW6NKXEUqDMIhxH7Zk"
    api_secret = "9uVYrtEtdmZiAzUFNqPyj3eU2uFyUUiUPeHde6zcWgWsCKiqI8"
    access_token = "25368429-RIo1mxKU0vDl5fwgdkzjUr3KexrkpuasuCFC4809J"
    access_token_secret = "2lKjkdBuTziqLAJ1jKJp5fyQwAIoiZVY6KqEC1QuAKo3M"
    #bearer_token = "XXXXX"

    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    candidate_username = twitterId
    # Twitter username of the candidate (without the '@')
    
    start_date = datetime.datetime.fromisoformat(dateFrom)
    end_date = datetime.datetime.fromisoformat(dateTo)
    # The time period of the tweets 

    utc = pytz.UTC 
    start_date = utc.localize(start_date)
    end_date = utc.localize(end_date)
    #Normalizes the timezone according to the UTC



    name = []
    bio = []
    follower_count = []
    tweets = []
    fav_count = []
    rt_count = []
    time = []
    time_Y_M_D = []
    time_H_M_S = []
    is_quote = []
    in_reply_to = []
    tweet_id = []
    hashtags = []
    is_retweet = []
    mentions = []
    emojicons = []

    # Creates a cursor objects and iterates through it to store tweet text and metadata of the tweet in lists
    for i in tweepy.Cursor(api.user_timeline, id = candidate_username ,  tweet_mode = 'extended').items():
        if i.created_at > start_date and i.created_at < end_date:
        #If throws timezone error, try utc.localize(i.created_at)
            name.append(i.user.name)
            tweets.append(i.full_text)
            time.append(i.created_at)
            time_Y_M_D.append(i.created_at.strftime('%Y-%m-%d %X')[:10])
            time_H_M_S.append(i.created_at.strftime('%Y-%m-%d %X')[-8:])
            bio.append(i.user.description)
            follower_count.append(i.user.followers_count)
            fav_count.append(i.favorite_count)
            rt_count.append(i.retweet_count)
            is_quote.append(i.is_quote_status)
            in_reply_to.append(i.in_reply_to_screen_name)
            tweet_id.append(i.id)
            is_retweet.append('retweeted_status' in dir(i))
            temp_mentions = []
            for dicti in i.entities['user_mentions']:
                temp_mentions.append(dicti['screen_name'])
            mentions.append(temp_mentions)
            temp_hashtags = []
            for dicti in i.entities['hashtags']:
                temp_hashtags.append(dicti['text'])
            hashtags.append(temp_hashtags)

    for tweet in tweets:
        de_emojized = emoji.demojize(tweet.replace(':', ' '))
        emojis = re.findall(r'(:[^:]*:)', de_emojized)
        emojicons.append(emojis)

    df = pd.DataFrame({'name':name, 
                  'bio': bio, 
                  'follower_count': follower_count, 
                  'tweet_text':tweets, 
                  'tweet_id':tweet_id, 
                  'fav_count':fav_count, 
                  'rt_count':rt_count, 
                  'in_reply_to': in_reply_to, 
                  'mentions' : mentions,
                  'is_retweet':is_retweet, 
                  'is_quote': is_quote, 
                  'hashtags': hashtags,
                  'emojicons': emojicons,
                  'time':time,
                  'time_Y_M_D' : time_Y_M_D,
                  'time_H_M_S' : time_H_M_S     
                  })

    columns = ['mentions', 'hashtags', 'emojicons']
    for column in columns:
        for j in range(len(df[column])):
            df[column][j] = ', '.join(i for i in df[column][j])
            if df[column][j] == '':
                df[column][j] = None

    return df
