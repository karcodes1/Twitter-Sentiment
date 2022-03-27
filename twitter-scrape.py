import requests
import os
import json
import pandas as pd
import csv
import os.path
from os import path
import dateutil
import time
import datetime as dt
from configparser import ConfigParser
import pandas as pd

#load the ini file which will keep track of the current progress of each ticker
INI_FILE = "twitter.ini"
DATA_FILE = './twitter_data_2020.csv'
config_object = ConfigParser()
config_object.read(INI_FILE)

#do you want to collect data for the S&P 500 or Russell 100? -- comment out whichever you do not want.
SP500_bool = True
#R1000_bool = True


#add column names to our output file
if path.exists(DATA_FILE) == False:
    csvFile = open("twitter_data_2020.csv", "a", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile)
    #Create headers for the data you want to save, in this example, we only want save these columns in our dataset
    csvWriter.writerow(['author id', 'created_at', 'id','lang', 'like_count', 'quote_count', 'reply_count','retweet_count','source','tweet','ticker_searched'])
    csvFile.close()


if SP500_bool == True:
    #load historical S&P500 information and save it to an array
    #since we are loading a file with historical SP500 information we need to make sure that we are adding it for companies within the time frame
    SP500 = pd.read_csv('./S&P500.txt')
    SP500['dtdate'] = pd.to_datetime(SP500['date'], format = "%Y-%m-%d")
    SP500 = SP500.loc[(SP500['dtdate'] > '2011-01-01') & (SP500['dtdate'] < '2012-03-02')].copy()
    tickers = []
    i = 1711
    while i < 1815:
        current_tickers = (SP500.at[i,'tickers'])
        current_tickers_arr = current_tickers.split(',')
        for tickers_ in current_tickers_arr:
            tickers.append(tickers_)
        i = i + 1
    all_tickers = set(tickers)
    tickers = list(all_tickers)
    tickers.sort()
    
    else if R1000_bool = True:
        R1000 = pd.read_csv('./Stocks in the Russell 1000 Index.csv')
        tickers = R1000['Symbol'].to_numpy()

#create auth token for twitter
os.environ['TOKEN'] = ''
def auth():
    return os.getenv('TOKEN')
def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

#function to create the url
def create_url(keyword, start_date, end_date, max_results = 10):

    search_url = "https://api.twitter.com/2/tweets/search/all" #Change to the endpoint you want to collect data from

    #change params based on the endpoint you are using
    query_params = {'query': keyword,
                    'start_time': start_date,
                    'end_time': end_date,
                    'max_results': max_results,
                    'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
                    'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source',
                    'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
                    'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
                    'next_token': {}}
    return (search_url, query_params)

#function to get data from the API
def connect_to_endpoint(url, headers, params):
    response = requests.request("GET", url, headers = headers, params = params)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

#function to save to the CSV file
def append_to_csv(json_response, fileName, tickers):

    #counter variable
    counter = 0

    #Open OR create the target CSV file
    csvFile = open(fileName, "a", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile)

    #Loop through each tweet
    for tweet in json_response['data']:

        # We will create a variable for each since some of the keys might not exist for some tweets
        # So we will account for that
        # 1. Author ID
        author_id = tweet['author_id']

        # 2. Time created
        created_at = dateutil.parser.parse(tweet['created_at'])

        # 4. Tweet ID
        tweet_id = tweet['id']

        # 5. Language
        lang = tweet['lang']

        # 6. Tweet metrics
        retweet_count = tweet['public_metrics']['retweet_count']
        reply_count = tweet['public_metrics']['reply_count']
        like_count = tweet['public_metrics']['like_count']
        quote_count = tweet['public_metrics']['quote_count']

        # 7. source
        try:
            source = tweet['source']
        except:
            source = None

        # 8. Tweet text
        text = tweet['text']

        # 9. Ticker searched
        ticker_searched = tickers

        # Assemble all data in a list
        res = [author_id, created_at, tweet_id, lang, like_count, quote_count, reply_count, retweet_count, source, text, ticker_searched]

        # Append the result to the CSV file
        csvWriter.writerow(res)
        counter += 1

    # When done, close the CSV file
    csvFile.close()

    # Print the number of tweets for this iteration
    print("# of Tweets added from this response: ", counter)

#get auth
bearer_token = auth()
headers = create_headers(bearer_token)

#set the start_time (end time is variable)
#start_time = "2011-02-28T00:00:00.000Z"
start_time = "2020-02-29T00:00:00.000Z"

max_results = 500

#loop through all the tickers in the S&P500 array
for tickers_ in tickers:
    #if there is a previous date for a ticker we will use that, otherwise it will set the end_time to the 'date_of_interest' end_time
    try:
        prev_run = config_object['PREVIOUS_RUN_DATE']
        end_time = prev_run[str(tickers_)]
    except:
        no_prev_run = config_object['DATES_OF_INTEREST']
        end_time = no_prev_run['end_time']
    end_time_compare = pd.to_datetime(end_time)
    print("collecting data for ticker " + tickers_ + "current end time: " + end_time)

    #set the keyword (search value)
    keyword = "$" + tickers_

    #call the url function which creates the search URL
    url = create_url(keyword, start_time, end_time, max_results)

    #we will try to call the function that collects data from the API
    #if it fails we will log the error and try again
    try:
        json_response = connect_to_endpoint(url[0], headers, url[1])
    except Exception as error:
        print(error)
        file1 = open("errors.txt", "a")
        file1.write(str(error)+"\n")
        file1.close()
        time.sleep(60)
        pass

    #wait 2 seconds (limited by API how fast we can collect data)
    time.sleep(2)

    #if there is no data (we have previously reached the end or the ticker has no data)
    #we will go to the next ticker
    if json_response['meta']['result_count'] == 0:
        continue

    #save the data that we collected from the API
    append_to_csv(json_response, DATA_FILE, tickers_)

    #get the last datetime value, this will be the end_time since the API searches from end to beginning
    current_time_compare = pd.to_datetime(dateutil.parser.parse(json_response['data'][-1]['created_at']))
    current_time = current_time_compare.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    #we will save the 'current_time'/'end_time' to the ini file, this will keep track of our progress
    prev_run[tickers_] = current_time
    with open('twitter.ini', 'w') as conf:
        config_object.write(conf)

    #we can ask the API to continue our previous querry by passing the 'next_token'
    #so we will continue to search while a 'next_token' exists
    while 'next_token' in json_response['meta']:
        #we change the 'next_token' value in our URL
        url[1]['next_token'] = json_response['meta']['next_token']
        #we try to collect data from the API
        #if it fails we will log the error and try again
        try:
            json_response = connect_to_endpoint(url[0], headers, url[1])
        except Exception as error:
            print(error)
            file1 = open("errors.txt", "a")
            file1.write(str(error)+"\n")
            file1.close()
            time.sleep(60)
            pass

        #sleep 2 seconds
        time.sleep(2)

        #save the data
        append_to_csv(json_response, DATA_FILE, tickers_)

        #get the last datetime value
        current_time_compare = pd.to_datetime(dateutil.parser.parse(json_response['data'][-1]['created_at']))
        current_time = current_time_compare.strftime("%Y-%m-%dT%H:%M:%S.000Z")

        #save the 'current_time'/'end_time' to ini file
        prev_run[tickers_] = current_time
        with open('twitter.ini', 'w') as conf:
            config_object.write(conf)
