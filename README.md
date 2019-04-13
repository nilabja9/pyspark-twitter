# Twitter Streaming App - Capturing hashtag traffic for Texas Senate Elections
Referrence: Recommeded Udemy Course : https://www.udemy.com/apache-spark-streaming-with-python-and-pyspark by Matthew McAteer

## Objective:

Pass a particular topic on to the Twitter API and find out the most popular hashtag in a certain period of time - and theire respective sentiments associated with it - namely Positivem Negative or Neutral. Subjectivity of the tweet is also measured.

## Solution and Architecture:
https://user-images.githubusercontent.com/35825748/56085011-211cec80-5e02-11e9-8691-41946a004856.jpg


## Pre-requisite Steps:




## End Result:






Steps to follow for setting up a Twitter App:-

https://iag.me/socialmedia/how-to-create-a-twitter-app-in-8-easy-steps/

Steps to follow for Download of Oracle Virtual Box :-

https://linus.nci.nih.gov/bdge/installUbuntu.html

Bash Script while creating the AWS EC2 Instance is attached as "Bash Scripts"

Additional EC2 setup commands are below :

#Install Spark:

sudo wget http://mirror.olnevhost.net/pub/apache/spark/spark-2.3.1/spark-2.3.1-bin-hadoop2.7.tgz

#Unzip the file

sudo tar -zvxf spark-2.3.1-bin-hadoop2.7.tgz

#Change Permission

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


