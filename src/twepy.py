from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import json
import zmq



#        replace mysql.server with "localhost" if you are running via your own server!
#                        server       MySQL username	MySQL pass  Database name.



#consumer key, consumer secret, access token, access secret.
ckey="avngLhaJFPziKYQkI4bJqobfY"
csecret="qqdYCAH2etbI2rOHBXmlbTk1rXNK5TGAnDXPAnEG3xSNIe4VG2"
atoken="831078007-oe1TBcecaLDEQcW1Hx1mhaq2pICIb9P2mclhSGX0"
asecret="XsUa71xGSotYCxZHcflhiwvvX63zkVUecRzOa0NZbvS0F"

context = zmq.Context();
zmq_socket = context.socket(zmq.PUSH)
zmq_socket.bind("tcp://0.0.0.0:9998")



class listener(StreamListener):

    def on_data(self, data):

        all_data = json.loads(data)
        zmq_socket.send_json(all_data)

            #print((username,tweet))

        return True

    def on_error(self, status):
        print status

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(locations=[-129.7,21.3,-50.0,59.6])
