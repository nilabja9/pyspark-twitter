# pyspark-twitter
Twitter Streaming with Spark
#Recommeded Udemy Course : 

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


