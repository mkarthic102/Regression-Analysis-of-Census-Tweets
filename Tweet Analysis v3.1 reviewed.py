#!/usr/bin/env python
# coding: utf-8

# In[6]:


import tweepy
from tweepy import OAuthHandler
import pandas as pd
import matplotlib.pyplot as plt
import re
import json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.sentiment import SentimentIntensityAnalyzer
import pytz

# cleans the tweet
def preprocess(tweet):
    tweet = tweet.full_text.lower()  
    tweet = re.sub(r"(@[A-Za-z0-9_]+)", "", tweet) # removes mentions
    tweet = re.sub("http://\S+|https://\S+", "", tweet) # removes links
    tweet = re.sub(r"[^\w\s]", "", tweet) # removes punctuation
    tweet = re.sub(r"_[_]", "", tweet) # removes underscores
    tweet = re.sub(r"[0-9][t][h]", "", tweet) # removes numbers (i.e. 234th)
    tweet = re.sub(r"[0-9]", "", tweet) # removes numbers (i.e. 234)
    
    # removes words that don't contribute to sentiment (i.e. "and", "but", "for")
    words = word_tokenize(tweet)
    tweet = [word for word in words if not word in stopwords.words()]
    tweet = " ".join(tweet)
    return tweet

# stems the word (i.e. released -> releas)
def stemmer(tweet):
    porter = PorterStemmer()
    words = word_tokenize(tweet)
    stem_sentence = []
    for word in words:
        stem_sentence.append(porter.stem(word))
    tweet = " ".join(stem_sentence)
    return tweet

# determines the sentiment of the tweet
def sentiment_score(tweet):
    sentiment_dict = sent_analyzer.polarity_scores(tweet)
    compound_score = sentiment_dict["compound"]
    sentiment_list = []
    sentiment_list.append(compound_score)
    
    if compound_score >= 0.05:
        sentiment = "positive"
    elif compound_score <= -0.05:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    
    sentiment_list.append(sentiment)
    highest_score_in_breakdown = max(sentiment_dict["neg"], sentiment_dict["pos"], sentiment_dict["neu"])
    majority = ""
    
    if (sentiment_dict["neg"] == max):
        majority = "neg"
    elif (sentiment_dict["pos"] == max):
        majority = "pos"
    else:
        majority = "neu"

    sentiment_list.append(majority)
    return sentiment_list

# twitter credentials
access_token = "1529194813622571009-0To6QExLSoPhnuQBPo9BAvZDTi0EUH"
access_token_secret = "RAuBeA7zggS5N0LK2924UOHMZUIGnKT2fP8PhkTVv1obl"
api_key = "4X93I3CxrTEOxcw4FuuipULoJ"
api_secret_key = "jc6rdWgmC2oYvmpnzqXTKoWmJFOocEO9KxSJK9x4aA1WrevqoL"

# passing twitter credentials to tweepy
auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# creating dataframe
all_tweet_data = pd.DataFrame(columns = ["Date", "Time (EST)", "Text", "Length (w/o links)", "Media?", "URL?", "Poll?", "Thread Length (0 = no thread)", "Quan. Position in Thread (0 = no thread)", "Qual. Position in Thread", "Hashtags", "# of Hashtags", "Retweets", "Likes", "Sentiment Score", "Sentiment"])

# sentiment intensity analyzer object
sent_analyzer = SentimentIntensityAnalyzer()
counter = 0

# reading in file with IDs representing tweets
file = "Tweet_IDs_Short.xlsx"
data = pd.read_excel(file)

# create a list of ids
ids = []
for i in range(len(data)):
    row = data.iloc[i]
    id = row["Tweet IDs"]
    # checks if the tweet exists (if it doesn't, then it was deleted from the Twitter account)
    try:
        tweet = api.get_status(id, tweet_mode = "extended", include_entities = True)
        count += 1
        ids.append(id)
    except:
        continue
    
# sort the list
ids.sort(reverse = True) 

# create a list called thread_replies
thread_replies = []
for id in ids:
    curr_reply = {}
    tweet = api.get_status(id, tweet_mode = "extended", include_entities = True)
    count += 1
    reply_id = tweet.in_reply_to_status_id
    reply_id = int(0 if reply_id is None else reply_id) # converting Nonetype object to int
    curr_reply["reply_id"] = reply_id
    curr_reply["text"] = tweet.full_text
    curr_reply["id"] = tweet.id
    thread_replies.append(curr_reply)

thread = []
all_threads = []
is_it_a_thread = "False"
position = len(thread_replies) - 1

# creating a list of threads for later use (i.e. determining if the tweet is contained in a thread)
while (position >= 0):
    if (position == len(thread_replies) - 1):
        tweet = thread_replies[position]
        reply = thread_replies[position - 1]
        
        if (tweet["id"] == reply["reply_id"]):
            thread.append(tweet)
    
    elif (position > 0):
        tweet = thread_replies[position]
        reply = thread_replies[position - 1]
        
        tweet_reverse = thread_replies[position + 1]
        reply_reverse = thread_replies[position]
        
        if (tweet["id"] == reply["reply_id"]):
            thread.append(tweet)
            
        # last tweet in thread
        elif (tweet_reverse["id"] == reply_reverse["reply_id"]):
            thread.append(reply_reverse)
            all_threads.append(thread)
            thread = []
            
    elif (position == 0):
        reply = thread_replies[position]
        tweet = thread_replies[position + 1]
        if (tweet["id"] == reply["reply_id"]):
            thread.append(reply)
            all_threads.append(thread)
            thread = []
    position -= 1

# identifying attributes in each tweet and storing in dataframe
for i in range(len(data)):
    row = data.iloc[i]
    id = row["Tweet IDs"]
    
    # checking if the tweet exists
    try:
        tweet = api.get_status(id, tweet_mode="extended", include_entities=True)
    except:
        continue
    
    # converting time to account location's timezone
    created_at = tweet.created_at
    created_at = created_at.astimezone(pytz.timezone("America/New_York")) # EST
    
    # variables for date and time created
    created_at = str(created_at)
    date = created_at.split(" ")[0]
    time = created_at.split(" ")[1]
    
    # variables to store text, retweets, and likes
    text = tweet.full_text
    retweets = tweet.retweet_count
    likes = tweet.favorite_count
    
    # length of the tweet
    text_no_links = re.sub("http://\S+|https://\S+", "", text) # removes links
    length = len(text_no_links)
    
    # determines if tweet contains a poll
    poll = "False"
    if text.__contains__("_"):
        poll = "True"
    
    # number of hashtags
    hashtags = []
    num_hashtags = 0
    for hashtag in tweet.entities["hashtags"]:
        hashtags.append(hashtag["text"])
        num_hashtags += 1
    
    # thread characteristics (thread length, tweets position in thread)
    contained_in_this_thread = []
    thread_length = 0
    quan_position_in_thread = 0
    qual_position_in_thread = "n/a"
    
    for i in range(len(all_threads)):
        single_thread = all_threads[i]
        for j in range(len(single_thread)):
            single_tweet = single_thread[j]
            if (single_tweet["id"] == tweet.id):
                contained_in_this_thread = single_thread
                quan_position_in_thread = j + 1
                break
    
    thread_length = len(contained_in_this_thread)
    
    if (quan_position_in_thread == 1):
        qual_position_in_thread = "first"
    elif (quan_position_in_thread == thread_length and thread_length != 0):
        qual_position_in_thread = "last"
    elif (quan_position_in_thread != 0):
        qual_position_in_thread = "mid"
    
    # determines if the tweet contains media
    media = "False"
    try:
        for media in tweet.entities["media"]:
            media = "True"
    except:
        media = "False"
        
    # determines if the tweet contains a link
    url = "False"
    try:
        for url in tweet.entities["urls"]:
            url = "True"
    except:
        url = "False"

    # sentiment of tweet
    cleaned_tweet = preprocess(tweet)
    cleaned_tweet = stemmer(cleaned_tweet)
    sentiment_list = sentiment_score(cleaned_tweet)
    
    # includes tweet in dataset
    single_tweet_data = [date, time, text, length, media, url, poll, thread_length, quan_position_in_thread, qual_position_in_thread, hashtags, num_hashtags, retweets, likes, sentiment_list[0], sentiment_list[1]]
    all_tweet_data.loc[counter] = single_tweet_data # storing all tweets in this dataframe
    
    # keeps track of total tweets and resets reply count
    counter += 1
    tweets_in_thread = 0
    
# displays dataframe
with pd.option_context('display.max_rows', None, 'display.max_columns', None,'display.precision', 3):
    display(all_tweet_data)
    
#all_tweet_data.to_excel("USCB_Twitter_Data_Updated.xlsx")


# In[ ]:




