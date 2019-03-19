'''
Gibson Farabow
Personal Project: Popularity of 2020 Democrat Candidats in NC
Examining Twitter data with Tweepy and a standard Twitter API

Program is set up to search the last x amount of tweets on Twitter which mention candidates,
and then from there tweets are further grouped, in this case by a NC location
(groupings can be easily updated), and then writen to a csv file in a format which can
be analyzed. This script finds the average amount of followers that NC twitter users have who
mention the candidates.
'''

import csv
import tweepy
import time
import pandas

# enter
dpath = ' ' # for location of csv file to be created
file = open(dpath + 'Dem_Candidate_Query.csv', 'w') # will be appended later
file.close()

# enter Twitter API information
consumer_key = ' '
consumer_secret =  ' '
access_token = ' '
access_token_secret = ' '

# Tweepy initialization
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


x = 1000  # amount of search items; this program has code to handle Twitter's rate limit

def NC_Candidate_Query(candidate):
    all_users = []
    trump_count = 0
    tweet_count = 0
    for tweets in tweepy.Cursor(api.search, q=candidate).items(x):
        grouping = tweets.user.location
        if ', NC' in grouping or 'North Carolina' in grouping:
            all_users.append(tweets.user)
            tweet_count += 1
            if 'Trump' in tweets.text:
                trump_count += 1 # see print statement in output

    results = [[candidate, tweet.location, tweet.followers_count] for tweet in all_users]

    with open (dpath + 'Dem_Candidate_Query.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow(['Candidate', 'Location', 'Followers'])
        writer.writerows(results)

    print('Trump mentioned with ' + candidate + ' ' + str(trump_count) \
          + ' times out of ' + str(tweet_count) + ' tweets')


#  estimate of how candidates will be mentioned on Twitter (not case sensitive)
candidates = ['Biden', 'Bernie', "O'Rourke", 'Booker', 'Klobuchar', ' Elizabeth Warren', \
              'Senator Warren', '@SenWarren','Senator Harris', 'Kamala Harris', '@SenKamalaHarris']

def run_without_limit(candidates): # keeps going after data rate limit exceeded
        for candidate in candidates:
            try:
                NC_Candidate_Query(candidate)
            except tweepy.TweepError:
                print('Rate Limit Exceeded: Sleeping')
                time.sleep(60 * 15) # rate limit resets after 15 minutes
                # with x = 1000, program can go through two candidates before limit exceeded
                continue

def average_user_followers(candidate):
        print("")
        data = pandas.read_csv(dpath + 'Dem_Candidate_Query.csv')
        data = data[data.Candidate == candidate]
        data.Followers = pandas.to_numeric(data.Followers, errors='coerce')
        print('Accounts that mention ' + candidate + ' have this many followers on average: ')
        print(data.Followers.mean())

# run script
run_without_limit(candidates)
for candidate in candidates:
        average_user_followers(candidate)
