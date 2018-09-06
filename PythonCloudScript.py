#Import all libraries

import findspark

# initialize your spark directory
findspark.init('/home/nilabja/spark-2.3.1-bin-hadoop2.7')


# May cause deprecation warnings, safe to ignore, they aren't errors
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import SQLContext
from pyspark.sql.functions import desc
import re
import time
from textblob import TextBlob
from collections import namedtuple
import boto3
from io import StringIO
import datetime
import awscredentials

# Creating the Spark Context
sc = SparkContext(master="local[2]", appName="WindowWordCount")
sc.setLogLevel("ERROR")

#creating the streaming context
ssc = StreamingContext(sc, 10)
ssc.checkpoint("checkpoint")

#creating the SQL context
sqlContext = SQLContext(sc)


lines = ssc.socketTextStream("localhost", 5599)

#Function to clean tweet
def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", str(tweet)).split())


#Polarity analysis of a tweet
def analyze_sentiment_polarity(tweet):
    analysis = TextBlob(clean_tweet(tweet))
    # return str(analysis.sentiment.polarity)
    if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    else:
        return -1

#subjectivity analysis of a tweet
def analyze_sentiment_subjectivity(tweet):
    analysis = TextBlob(clean_tweet(tweet))
    return str(analysis.sentiment.subjectivity)


#Transforming using basic spark functions
sentiment = lines.map(lambda text: (text, analyze_sentiment_polarity(text), analyze_sentiment_subjectivity(text)))
words = lines.flatMap(lambda text: text.split(" ")).filter(lambda text: text.lower().startswith('#'))

fields = ("hashtags", "count")
Tagscount = namedtuple('Tagscount', fields)

sentimentfields = ("text", "polarity", "subjectivity")
Sentimentobject = namedtuple('Sentimentobject', sentimentfields)

sentiment.window(180, 60).map(lambda p: Sentimentobject(p[0], p[1], p[2])).foreachRDD(
    lambda rdd: rdd.toDF().registerTempTable("sentiment"))
words.countByValueAndWindow(180, 60).map(lambda p: Tagscount(p[0], p[1])).foreachRDD(
    lambda rdd: rdd.toDF().sort(desc('count')).limit(10).registerTempTable("hashtags"))

response = input("Do you want to start the twitter stream ? Y/N (Please execute your stream listener in another terminal session and then put Y)\n")

if response == "Y":
    ssc.start()
    print("Session Started.....")
    print("Collecting tweets...waiting for 60 seconds..")

    time.sleep(60)
    print("Tweets Collected....")

    #Connecting to a boto3 session - Update file in AWS Cloud S3 Bucket

    count = 0
    while count < 10: #We will run the loop 10 times for demonstration
        print("Waiting for 30 Seconds.....")
        time.sleep(30) #This loop will run every 30 seconds. The time interval can be increased as per your wish
        top_10_tweets = sqlContext.sql('Select * from hashtags')
        top_10_df = top_10_tweets.toPandas()

        print("------------------------------- \n")
        print(top_10_df)

        pos_sentiment = sqlContext.sql('Select count(text) from sentiment where polarity = 1')
        neu_sentiment = sqlContext.sql('Select count(text) from sentiment where polarity = 0')
        neg_sentiment = sqlContext.sql('Select count(text) from sentiment where polarity = -1')

        pos_df = pos_sentiment.toPandas()
        neu_df = neu_sentiment.toPandas()
        neg_df = neg_sentiment.toPandas()

        totalsentiment = pos_df['count(text)'].iloc[0] + neg_df['count(text)'].iloc[0] + neu_df['count(text)'].iloc[0]

        percent_pos = (pos_df['count(text)'].iloc[0] / totalsentiment) * 100
        print('Percentage of Positive Sentiment = {} %'.format(round(percent_pos, 2)))

        percent_neu = (neu_df['count(text)'].iloc[0] / totalsentiment) * 100
        print('Percentage of Neutral Sentiment = {} %'.format(round(percent_neu, 2)))

        percent_neg = (neg_df['count(text)'].iloc[0] / totalsentiment) * 100
        print('Percentage of Negative Sentiment = {} %'.format(round(percent_neg, 2)))

        count = count + 1

        #Updating latest hashtag count in a S3 bucket file
        csv_buffer = StringIO()
        top_10_df.to_csv(csv_buffer)

        ts = datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
        filename = str("hashtags_" +  ts + ".csv")

        print("Uploading to S3 - Filename: " + filename + "\n")

        print("Connectine to AWS Boto3 session...Uploading the csv file")
        session = boto3.Session(awscredentials.aws_access_key_id, awscredentials.aws_secret_access_key)
        s3 = session.resource('s3')
        s3.Object('twitter-data-analysis-nilabja', filename).put(Body=csv_buffer.getvalue())

    ssc.awaitTermination()

else:
    print("You ended the program")
    exit()