# Twitter Streaming App - Capturing hashtag traffic for Texas Senate Elections
Referrence: Recommeded Udemy Course : https://www.udemy.com/apache-spark-streaming-with-python-and-pyspark by Matthew McAteer

## Objective:

Pass a particular topic on to the Twitter API and find out the most popular hashtag in a certain period of time - and theire respective sentiments associated with it - namely Positivem Negative or Neutral. Subjectivity of the tweet is also measured.

## Solution and Architecture:
![BluePrint](https://user-images.githubusercontent.com/35825748/56085011-211cec80-5e02-11e9-8691-41946a004856.jpg)

A python application is used to make API calls to Twitter using the Tweepy library and the tweets are streamed to a TCP port.
A topic is passed in the application. The python script is running on a EC2 Linux environment. A Spark-Streaming application reads the tweets from the port already defined, transform the data and save results in S3 bucket. This also runs in EC2.

## Pre-requisite Steps:
Steps to follow for setting up a Twitter App:-
https://iag.me/socialmedia/how-to-create-a-twitter-app-in-8-easy-steps/

Steps to follow for Download of Oracle Virtual Box :-
https://linus.nci.nih.gov/bdge/installUbuntu.html

Bash Script while creating the AWS EC2 Instance is attached as "Bash Scripts"
Additional EC2 setup commands are below :

Install Spark:
sudo wget http://mirror.olnevhost.net/pub/apache/spark/spark-2.3.1/spark-2.3.1-bin-hadoop2.7.tgz

Unzip the file
sudo tar -zvxf spark-2.3.1-bin-hadoop2.7.tgz

Change Permission
sudo chmod -R 777 spark-2.3.1-bin-hadoop2.7

#export variables
export SPARK_HOME='/home/ubuntu/spark-2.3.1-bin-hadoop2.7'
export PATH=$SPARK_HOME:$PATH
export PYTHONPATH=$SPARK_HOME/python:$PYTHONPATH
export PYSPARK_DRIVER_PYTHON="jupyter"
export PYSPARK_DRIVER_PYTHON=OPTS="notebook"
export PYSPARK_PYTHON=python3

#Next use command tmux to split the terminal
tmux
ctrl-b -> shift-5
To navigate
ctrl-b left arrow/right arrow

The Python application and the Spark file, is executed in sequence and we will be able to see tweets being collected.
For simplicity. the Spark Application runs in a local mode

## End Result:

Once the tweet starts flowing into the port, the Spark Streaming context kicks in and processes the data. It is transformed into a Spark dataframe. The results are stored in temporary tables and donwloaded to AWS S3 in csv format.
![Results](https://user-images.githubusercontent.com/35825748/56085216-67277f80-5e05-11e9-8f17-860b7d61c520.png)

![Results2](https://user-images.githubusercontent.com/35825748/56085217-67c01600-5e05-11e9-8aa8-0b1b8eaf5c6f.png)

For a detailed process oriented overview, kindly the below video:
[https://www.youtube.com/watch?v=eSw6sq3KVtg](url)
