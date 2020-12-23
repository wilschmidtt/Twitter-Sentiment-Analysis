

from textblob import TextBlob # Library for processing textual data. Provides a simple API for diving into common NLP tasks, like POS tagging
import sys, tweepy, csv, re # Tweepy allows python to communicate with Twitter and use its API. csv allows you to parse csv files. re allows you to search for regular expressions within a string
import matplotlib.pyplot as plt # Plotting library for Python. .pyplot allows matplotlib to work like MATLAB
import numpy as np
import pandas as pd

consumerKey = # upload yours here
consumerSecret = # upload yours here
accessToken = # upload yours here
accessTokenSecret = # upload yours here

class Sentiment:

    def __init__(self):
        self.tweets = []
        self.tweetText = []
        self.listTweets = []
        authenticator = tweepy.OAuthHandler(consumerKey, consumerSecret)
        authenticator.set_access_token(accessToken, accessTokenSecret)
        self.twitter_client = tweepy.API(authenticator)
        
    def get_twitter_client_api(self):
        return self.twitter_client
        
    def cleanAllTweets(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())
    
    # function to calculate percent
    def percent(self, part, whole):
        var = 100 * float(part) / float(whole)
        return format(var, '.2f')

    def GetData(self):
        authenticator = tweepy.OAuthHandler(consumerKey, consumerSecret)
        authenticator.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(authenticator)
        loop = True
        search_type = input("Would you like to search by username or hashtag? Type 1 for username or 2 for hashtag:" )
        while loop:
            if search_type == '1' or search_type == '2':
                loop = False
            else:
                search_type = input("Please enter either 1 for username or 2 for hashtag: ")
        if search_type == '1':
            global search_term
            search_term = input("Enter username that you would like to analyze (don't include the @): ")
        else: 
            search_term = input("Enter the hashtag that you would like to analyze (don't include the #): ")
        global tweet_count
        tweet_count = input("How many tweets would you like to analize? ")
        loop = True
        while loop:
            if tweet_count.isdigit():
                tweet_count = int(tweet_count)
                loop = False
            else:
                tweet_count = input("Please enter a valid number of tweets to analyze: ")
        

        # searching for tweets
        for tweet in tweepy.Cursor(self.twitter_client.user_timeline, id=search_term).items(tweet_count):
                self.tweets.append(tweet)

        # Open/create a file to append data to
        TweetsCSV = open('result.csv', 'a')

        # Use csv writer
        Write_to_CSV = csv.writer(TweetsCSV)

        # creating some variables to store info
        average_polarity = 0
        positive = 0
        weakly_positive = 0
        strongly_positive = 0
        negative = 0
        weakly_negative = 0
        strongly_negative = 0
        neutral = 0

        # iterating through tweets fetched
        for tweet in self.tweets:
            self.tweetText.append(self.cleanAllTweets(tweet.text).encode('utf-8'))
            analysis = TextBlob(tweet.text)
            average_polarity += analysis.sentiment.polarity  # adding up polarities to find the average rating

            if (analysis.sentiment.polarity == 0):
                neutral += 1
            elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.33):
                weakly_positive += 1
            elif (analysis.sentiment.polarity > 0.33 and analysis.sentiment.polarity <= 0.66):
                positive += 1
            elif (analysis.sentiment.polarity > 0.66 and analysis.sentiment.polarity <= 1):
                strongly_positive += 1
            elif (analysis.sentiment.polarity > -0.33 and analysis.sentiment.polarity <= 0):
                weakly_negative += 1
            elif (analysis.sentiment.polarity > -0.66 and analysis.sentiment.polarity <= -0.33):
                negative += 1
            elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.66):
                strongly_negative += 1


        # Write to csv and close csv file
        Write_to_CSV.writerow(self.tweetText)
        TweetsCSV.close()

        # finding average of how people are reacting
        positive = self.percent(positive, tweet_count)
        weakly_positive = self.percent(weakly_positive, tweet_count)
        strongly_positive = self.percent(strongly_positive, tweet_count)
        negative = self.percent(negative, tweet_count)
        weakly_negative = self.percent(weakly_negative, tweet_count)
        strongly_negative = self.percent(strongly_negative, tweet_count)
        neutral = self.percent(neutral, tweet_count)
        
        plt.show()
        average_polarity = average_polarity / tweet_count

        # printing out data
        print("How people are reacting on " + search_term + " by analyzing " + str(tweet_count) + " tweets.")
        print()
        print("Average Sentiment: ")

        if (average_polarity == 0):
            print("Neutral")
        elif (average_polarity > 0 and average_polarity <= 0.3):
            print("Weakly Positive")
        elif (average_polarity > 0.3 and average_polarity <= 0.6):
            print("Positive")
        elif (average_polarity > 0.6 and average_polarity <= 1):
            print("Strongly Positive")
        elif (average_polarity > -0.3 and average_polarity <= 0):
            print("Weakly Negative")
        elif (average_polarity > -0.6 and average_polarity <= -0.3):
            print("Negative")
        elif (average_polarity > -1 and average_polarity <= -0.6):
            print("Strongly Negative")

        print()
        print("In-Depth Analysis: ")
        print(str(positive) + "% people thought it was positive")
        print(str(weakly_positive) + "% people thought it was weakly positive")
        print(str(strongly_positive) + "% people thought it was strongly positive")
        print(str(negative) + "% people thought it was negative")
        print(str(weakly_negative) + "% people thought it was weakly negative")
        print(str(strongly_negative) + "% people thought it was strongly negative")
        print(str(neutral) + "% people thought it was neutral")

        self.plotCharts(positive, weakly_positive, strongly_positive, negative, weakly_negative, strongly_negative, neutral, search_term, tweet_count)
                
    def tweets_to_data_frame(self, tweets): # converts json to data frame
        tweet_df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets']) #used to extract just the text from tweets

        tweet_df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        tweet_df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        tweet_df['date'] = np.array([tweet.created_at for tweet in tweets])
        tweet_df['source'] = np.array([tweet.source for tweet in tweets])
        tweet_df['source_url'] = np.array([tweet.source_url for tweet in tweets])
        tweet_df['len'] = np.array([len(tweet.text) for tweet in tweets])
        tweet_df['id'] = np.array([tweet.id for tweet in tweets])
        
        # Run the following line of code to see all of the elements of the tweet that can be included in the df
        #print(dir(tweets[0]))
        
        pd.set_option('display.max_columns', 30)
        return tweet_df
        
    def plotCharts(self, positive, weakly_positive, strongly_positive, negative, weakly_negative, strongly_negative, neutral, search_term, noOfSearchTerms):
        labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(weakly_positive) + '%]','Strongly Positive [' + str(strongly_positive) + '%]', 'Neutral [' + str(neutral) + '%]',
                  'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(weakly_negative) + '%]', 'Strongly Negative [' + str(strongly_negative) + '%]']
        sizes = [positive, weakly_positive, strongly_positive, neutral, negative, weakly_negative, strongly_negative]
        colors = ['yellowgreen','lightgreen','darkolivegreen', 'gold', 'red','lightsalmon','darkred']
        
        # Pie Chart
        patches, texts = plt.pie(sizes, colors=colors)
        plt.legend(patches, labels, loc="best")
        plt.title('Tweet sentiment for hashtag [' + search_term + '] by analyzing ' + str(noOfSearchTerms) + ' Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()
        
        # Bar Chart
        x = [1,2,3,4,5,6,7]
        sizes = [float(i) for i in sizes]
        plt.title('Tweet sentiment for ' + search_term + ' by analyzing ' + str(noOfSearchTerms) + ' Tweets.')
        plt.barh(x, width = sizes, color = colors, tick_label = labels)
        plt.show()
        
if __name__== "__main__": 
    sa = Sentiment()
    sa.GetData()
    
    tweets = sa.get_twitter_client_api().user_timeline(screen_name=search_term, count=tweet_count)
    tweet_df = sa.tweets_to_data_frame(tweets)
    sort_by_likes = tweet_df.sort_values('likes', ascending = False)
    sort_by_retweets = tweet_df.sort_values('retweets', ascending = False)
    print(f"Most liked tweet: {tweet_df['tweets'][tweet_df['likes'].idxmax()]}")
    print(f"Most retweeted tweet: {tweet_df['tweets'][tweet_df['retweets'].idxmax()]}")
    
    # Time Series for Likes and Retweets
    time_likes = pd.Series(data=tweet_df['likes'].values, index=tweet_df['date'])
    time_likes.plot(figsize=(16, 4), label="likes", legend=True)
    time_retweets = pd.Series(data=tweet_df['retweets'].values, index=tweet_df['date'])
    time_retweets.plot(figsize=(16, 4), label="retweets", legend=True)
    plt.title('Time Series Analysis')
    plt.xlabel('Date of Tweet')
    plt.ylabel('Amount of Likes/Retweets')
    plt.show()
