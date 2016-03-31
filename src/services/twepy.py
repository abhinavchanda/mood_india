from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import json
import zmq

ckey="qzCipeYsm2EJKmCxCuumvepAt"
csecret="FXKIndpcmlJ41BAd7PzC5gIBCYCzxAk010iRmzJkHJR723Qhy2"
atoken="550251646-3hySSynNeUeNpOz06qaVikaOuBpceVCaZjsJwNmQ"
asecret="VC1Jmr6wNZPXYJZsBLk1Th0qAwpUs2HhCkvM0wQ696eVf"

context = zmq.Context();
zmq_socket = context.socket(zmq.PUSH)
zmq_socket.setsockopt(zmq.HWM,100000)
zmq_socket.bind("tcp://0.0.0.0:9998")



class listener(StreamListener):

    def on_data(self, data):
    	print("Fdsafa");
    	print(data);
        all_data = json.loads(data)
        zmq_socket.send_json(all_data)
        #print(all_data);
            #print((username,tweet))

        return True

    def on_error(self, status):
        print status

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(locations=[-124.7,24.3,-66.8854,59.6])