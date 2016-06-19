#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv
from secrets import *

#Twitter API credentials imported from secrets
consumer_key = C_K
consumer_secret = C_S
access_key = A_K
access_secret = A_S

def initTwitterConnection():
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    return api
    
def get_all_tweets(screen_name, api):
    #Twitter only allows access to a users most recent 3240 tweets with this method

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

def postHaiku(haiku, api):
    api.update_status(status = haiku)

def syllable_count(word):
    #shittiest syllable counter in the world
    #literally the worst
    #fails on soooooooooooooo many words oh well.
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

def find_haiku_sentence(sentence):
    syl_count = 0
    exceptions = ['\n',' ','!',':',';','?','!','']
    words = sentence.split(' ')
    if '@' in sentence or 'http' in sentence or 'co/' in sentence:
        return 0
        
    for word in words:
        if word in exceptions:
            continue
        syl_count += syllable_count(word)
    print syl_count
    if syl_count == 5:
        return 1
    elif syl_count == 7:
        return 2
    else:
        return 0
    
def store_haiku_sentences(screen_name):
    #store5 = []
    #store7 = []
    with open('%s_tweets.csv' % screen_name, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            lines = row[2].split('\n')
            for line in lines:
                sentences = line.split('.')
                for sentence in sentences:
                    print sentence                    
                    result = find_haiku_sentence(sentence)
                    if result == 1:
                        with open('5_syl.csv', 'a') as five:
                            writer = csv.writer(five)
                            writer.writerow([sentence])
                    elif result == 2:
                        with open('7_syl.csv', 'a') as seven:
                            writer = csv.writer(seven)
                            writer.writerow([sentence])
 
def buildHaiku():
    #haiku = ""
    five = open('5_syl.csv', 'r')
    seven = open('7_syl.csv', 'r')
    r_five = csv.reader(five)
    r_seven = csv.reader(seven)
    haiku = ""
    haiku += r_five.next()[0] + '\n'
    haiku += r_seven.next()[0] + '\n'
    haiku += r_five.next()[0] 
    return haiku
        
if __name__ == '__main__':
    #pass in the username of the account you want to download
    api = initTwitterConnection()
    screen_name = "SwiftOnSecurity"
    #get_all_tweets(screen_name, api)
    #store_haiku_sentences(screen_name)
    haiku = buildHaiku()
    postHaiku(haiku, api)
    #print syllable_count("barely")
    #print CountSyllables("barely")
