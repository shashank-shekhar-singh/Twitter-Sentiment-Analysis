import os
import csv
import matplotlib
import matplotlib.pyplot as plt
import re
import tweepy
from flask import Blueprint, render_template, request
from textblob import TextBlob

matplotlib.use('TkAgg')

# second = Blueprint("second", __name__, static_folder="static", template_folder="template")


# @second.route("/sentiment_analyzer")
# def sentiment_analyzer():
#     return render_template("sentiment_analyzer.html")


class SentimentAnalysis:

    def __init__(self):
        self.tweets = []
        self.tweetText = []

    def DownloadData(self, keyword, number_of_tweets):

        consumerKey = 'IP5Zd0GFVv15u2kYW2LN4v9G1'
        consumerSecret = 't0BeyBIsSE0RdW4F1qgi2c7XN0oMBcZGPdc78fmZKuOPfWbeuJ'
        accessToken = '461434789-5lSaeLlLT6RKPUV34hh94kkpUh45sMA82qpf3Inw'
        accessTokenSecret = 'p7hjJxDfqqVhl4byuyojMejpKZjI9JKp4cqvNxJGFPlpm'

        # authenticating
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth, wait_on_rate_limit=True)

        # input for term to be searched and how many tweets to search
        # searchTerm = input("Enter Keyword/Tag to search about: ")
        # NoOfTerms = int(input("Enter how many tweets to search: "))

        # searching for tweets
        # tweepy.Cursor(api.search, q=keyword, lang="en").items(number_of_tweets)
        self.tweets = tweepy.Cursor(api.search, q=keyword, lang="en").items(number_of_tweets)
        # print(list(self.tweets))

        # Open/create a file to append data to
        csvFile = open('result.csv', 'a')

        # Use csv writer
        csvWriter = csv.writer(csvFile)

        # creating some variables to store info
        polarity = 0
        positive = 0
        wpositive = 0
        spositive = 0
        negative = 0
        wnegative = 0
        snegative = 0
        neutral = 0

        # iterating through tweets fetched
        for tweet in self.tweets:
            # Append to temporary list so that we can store in csv later. We used encode UTF-8
            self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
            # print(tweet.text.translate(non_bmp_map))
            # print(self.cleanTweet(tweet.text))
            analysis = TextBlob(tweet.text)
            # print(analysis.sentiment)  # print tweet's polarity
            polarity += analysis.sentiment.polarity  # adding up polarities to find the average later
            # adding reaction of how people are reacting to find average later

            if analysis.sentiment.polarity == 0:
                neutral += 1
            elif 0 < analysis.sentiment.polarity <= 0.3:
                wpositive += 1
            elif 0.3 < analysis.sentiment.polarity <= 0.6:
                positive += 1
            elif 0.6 < analysis.sentiment.polarity <= 1:
                spositive += 1
            elif -0.3 < analysis.sentiment.polarity <= 0:
                wnegative += 1
            elif -0.6 < analysis.sentiment.polarity <= -0.3:
                negative += 1
            elif -1 < analysis.sentiment.polarity <= -0.6:
                snegative += 1

        # Write to csv and close csv file
        csvWriter.writerow(self.tweetText)
        csvFile.close()

        # finding average of how people are reacting
        positive = self.percentage(positive, number_of_tweets)
        wpositive = self.percentage(wpositive, number_of_tweets)
        spositive = self.percentage(spositive, number_of_tweets)
        negative = self.percentage(negative, number_of_tweets)
        wnegative = self.percentage(wnegative, number_of_tweets)
        snegative = self.percentage(snegative, number_of_tweets)
        neutral = self.percentage(neutral, number_of_tweets)

        # finding average reaction
        polarity = polarity / number_of_tweets

        # printing out data
        #  print("How people are reacting on " + keyword + " by analyzing " + str(tweets) + " tweets.")
        #  print("General Report: ")

        if polarity == 0:
            htmlpolarity = "Neutral"
            # print("Neutral")
        elif 0 < polarity <= 0.3:
            htmlpolarity = "Weakly Positive"
            # print("Weakly Positive")
        elif 0.3 < polarity <= 0.6:
            htmlpolarity = "Positive"
        elif 0.6 < polarity <= 1:
            htmlpolarity = "Strongly Positive"
        elif -0.3 < polarity <= 0:
            htmlpolarity = "Weakly Negative"
        elif -0.6 < polarity <= -0.3:
            htmlpolarity = "Negative"
        elif -1 < polarity <= -0.6:
            htmlpolarity = "strongly Negative"

        self.plotPieChart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, keyword,
                          number_of_tweets)
        # print(polarity, htmlpolarity)
        return polarity, htmlpolarity, positive, wpositive, spositive, negative, wnegative, snegative, neutral, keyword, number_of_tweets

        # Remove Links, Special Characters etc from tweet

    def cleanTweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    # function to calculate percentage
    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

    def plotPieChart(self, positive, wpositive, spositive, negative, wnegative, snegative, neutral, keyword, tweets):
        fig = plt.figure()
        labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]',
                  'Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
                  'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]',
                  'Strongly Negative [' + str(snegative) + '%]']
        sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
        colors = ['yellowgreen', 'lightgreen', 'darkgreen', 'gold', 'red', 'lightsalmon', 'darkred']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.axis('equal')
        plt.tight_layout()
        # strFile = r"C:\Users\LENOVO\PycharmProjects\SentimentAnalysis\static\images\plot1.png"
        strFile = r"D:\Studies\Projects\ML\SentimentAnalysis\static\images\plot1.png"
        if os.path.isfile(strFile):
            os.remove(strFile)  # Opt.: os.system("rm "+strFile)
        plt.savefig(strFile)
        plt.show()


# @second.route('/sentiment_logic', methods=['POST', 'GET'])
# def sentiment_logic():
#     keyword = request.form.get('keyword')
#     number_of_tweets = int(request.form.get('number_of_tweets'))
#     sa = SentimentAnalysis()
#     polarity, htmlpolarity, positive, \
#     wpositive, spositive, negative, wnegative, \
#     snegative, neutral, keyword1, tweet1 = sa.DownloadData(keyword, number_of_tweets)
#
#     return render_template('sentiment_analyzer.html', polarity=polarity, htmlpolarity=htmlpolarity, positive=positive,
#                            wpositive=wpositive, spositive=spositive,
#                            negative=negative, wnegative=wnegative, snegative=snegative, neutral=neutral,
#                            keyword=keyword1, tweets=tweet1)
#
#
# @second.route('/visualize')
# def visualize():
#     return render_template('PieChart.html')
