import tweepy
from credentials import *
import numpy as np
import pandas as pd
from os import path

class Scraper():

    def __init__(self):

        self.scraped = {'TimeStamps': [],
                        'Screen name': [],
                        'Username': [],
                        'Tweets': []}
        self.df = pd.DataFrame(self.scraped)
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(self.auth,wait_on_rate_limit=True)
    

    def scrape(self, text, num_tweets):

        text += ' -filter:retweets'
        num_needed = num_tweets
        timestamp_list = []
        tweet_list = [] # Lists to be added as columns( Tweets, usernames, and screen names) in our dataframe 
        user_list = []
        screen_name_list = []
        tw_id = [] 
        last_id = -1 # ID of last tweet seen
        while len(tweet_list) < num_needed:
            try:
                new_tweets = self.api.search_tweets(q = text, count = num_needed, max_id = str(last_id - 1), lang = 'en', tweet_mode = 'extended') 
            except Exception as e:
                print("Error", e)
                break
            else:
                if not new_tweets:
                    print("Could not find any more tweets!")
                    break
                else:
                    for tweet in new_tweets:

                        # Fetching the screen name and username
                        timestamp = tweet.created_at
                        screen_name = tweet.author.screen_name
                        user_name = tweet.author.name
                        tweet_text = tweet.full_text
                        
                        timestamp_list.append(timestamp)
                        tweet_list.append(tweet_text)
                        user_list.append(user_name)
                        screen_name_list.append(screen_name)
                        tw_id.append(tweet.id) 
            last_id = min(tw_id) 

        for idx in range(len(timestamp_list)):
            self.scraped['TimeStamps'].append(timestamp_list[idx])
            self.scraped['Screen name'].append(screen_name_list[idx])
            self.scraped['Username'].append(user_list[idx])
            self.scraped['Tweets'].append(tweet_list[idx])

        self.df = pd.DataFrame(self.scraped)


    def save_cleaned_df(self, file_name='twitter_scrape.csv'):
        self.df = self.df.drop_duplicates()
        self.df.to_csv(file_name, index=False)
    