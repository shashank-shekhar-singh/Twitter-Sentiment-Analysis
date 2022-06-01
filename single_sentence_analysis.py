from textblob import TextBlob
import re


# def cleanTweet(tweet):
#     return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())


def singleSentenceAnalysis(string):
    # string = input("Enter a sentence: ")
    # print(cleanTweet(string))
    # blob = TextBlob(cleanTweet(string))
    blob = TextBlob(string)
    polarity = blob.sentiment.polarity

    if polarity == 0:
        return "neutral"
    elif 0 < polarity <= 0.3:
        return "weakly positive"
    elif 0.3 < polarity <= 0.6:
        return "positive"
    elif 0.6 < polarity <= 1:
        return "strongly positive"
    elif -0.3 < polarity <= 0:
        return "weakly negative"
    elif -0.6 < polarity <= -0.3:
        return "negative"
    elif -1 < polarity <= -0.6:
        return "strongly negative"
