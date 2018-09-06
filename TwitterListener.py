import socket
import json
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import twittercredentials


#Stream Listener Class
class TweetsListener(StreamListener):

    def __init__(self, csocket):
        self.client_socket = csocket


    def on_data(self, data):
        try:
            msg = json.loads(data)
            if ('retweeted_status' in msg):
                if ('extended_tweet' in msg['retweeted_status']):
                    print(msg['retweeted_status']['extended_tweet']['full_text'])
                    self.client_socket.send((str(msg['retweeted_status']['extended_tweet']['full_text']) + "\n").encode('utf-8'))
            elif ('extended_status' in msg):
                print(msg['extended_status']['full_text'])
                self.client_socket.send((str(msg['extended_status']['full_text']) + "\n").encode('utf-8'))
            else:
                print(msg['text'])
                self.client_socket.send((str(msg['text']) + "\n").encode('utf-8'))
        except BaseException as e:
            print("Error on_data: %s" % str(e))

        return True


    def on_error(self, status):
        print(status)
        return True


#Initializing the port and host
host = 'localhost'
port = 5599
address = (host, port)

#Initializing the socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(address)
server_socket.listen(5)

print("Listening for client...")
conn, address = server_socket.accept()

print("Connected to Client at " + str(address))

#authenticating
auth = OAuthHandler(twittercredentials.consumer_key, twittercredentials.consumer_secret)
auth.set_access_token(twittercredentials.access_token, twittercredentials.access_token_secret)

#Establishing the twitter stream
twitter_stream = Stream(auth, TweetsListener(conn), tweet_mode="extended_tweet")
twitter_stream.filter(track=['US Open'])

