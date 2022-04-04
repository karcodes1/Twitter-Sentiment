# Does the sentiment (emotional valence) of twitter post correlate to short term stock returns?

After the explosion of retail investers in 2020, I was curious to see if social media was driving decision and therefore stock prices. 

## Twitter mood predicts the stock market (Bollen, Mao, and Zeng 2011). 

This paper looks at general tweets and groups them by mood (using a dictionary of words). There were able to find a coorelation between stock returns from the DJIA and the number of calm tweets. This seems to make sense since the market typically reacts negatively to uncertainty, so during periods of calmness the market would have higher expected returns.

## Trading on Twitter: The financial Information Content of Emotion in Social Media (Sul, Dennis, and Yuan 2014)

This paper expanded on previous work by by Boolen, Mao and Zeng. Instead of focusing on the general mood of the twitter population (all tweets) they wanted to see how tweets made about individual firms effected the returns of those firms over the short term. Using a dictionary of positive and negative words they were able to find a coorelation between positive sentiment and same day returns, as well as 10 day returns. They were also able to find a negative coorelation between negative sentiment and same day returns, as well as 10 day returns. 

To replicate the results found in this paper I had to create two programs. One that would scrape twitter for the data during the same time frame (Mar 2011- Feb 2012) and another program that would analyze the data using the methods described. 

## Scraping twitter data **requires twitter academic API access**

Scrapping twitter data was acomplished using twitter-scrape.py. It works by querrying the twitter API for tweets that contain the '$' sign followed by a ticker. This was done for all firms within the S&P 500. 

## Analyizing the twitter data

The data was analyzed using the methods from Sul, Dennis, and Yuan 2014 in 
