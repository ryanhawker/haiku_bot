#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv
from secrets import *

#Twitter API credentials
consumer_key = C_K
consumer_secret = C_S
access_key = A_K
access_secret = A_S


def get_all_tweets(screen_name):
    #Twitter only allows access to a users most recent 3240 tweets with this method
    
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    
    #initialize a list to hold all the tweepy Tweets
    alltweets = []    
    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    
    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print "getting tweets before %s" % (oldest)
        
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        
        print "...%s tweets downloaded so far" % (len(alltweets))
    
    #transform the tweepy tweets into a 2D array that will populate the csv    
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
    
    #write the csv    
    with open('%s_tweets.csv' % screen_name, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(["id","created_at","text"])
        writer.writerows(outtweets)
    
    pass

def syllable_count(word):
    #shittiest syllable counter in the world
    #literally the worst
    count = 0
    vowels = 'aeiouy'
    word = word.lower().strip(".:;?!")
    if word[0] in vowels:
        count +=1
    for index in range(1,len(word)):
        if word[index] in vowels and word[index-1] not in vowels:
            count +=1
    if word.endswith('e'):
        count -= 1
    if word.endswith('le'):
        count+=1
    if word.endswith('ia'):
        count+=1
    if count == 0:
        count +=1
    return count    

def store_haiku_sentences(screen_name):
    #store5 = []
    #store7 = []
    exceptions = ['\n',' ','!',':',';','?','!','']
    with open('%s_tweets.csv' % screen_name, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            sentences = row[2].split('.')
            #sentences = [k.split('\n') for k in sentences]
            for sentence in sentences:
                print sentence
                syl_count = 0
                words = sentence.split(' ')
                for word in words:
                    if word in exceptions:
                        continue
                    syl_count += syllable_count(word)
                print syl_count

    
if __name__ == '__main__':
    #pass in the username of the account you want to download
    screen_name = "shitty_haiku_nz"
    #get_all_tweets(screen_name)
    store_haiku_sentences(screen_name)
    #print syllable_count()
