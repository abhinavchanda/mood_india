
# from sentiment import *
# from load_sentiment import *
from services.twitterstream import  *
import csv
from tools.Sanitize.normalize import *
import tools.Sentiment.SentiWordNet.SentimentHelper
import zmq
from textblob import TextBlob
import reverse_geocoder as rg
from flask import Flask, render_template, request
import flask

#SentimentHelper.init()
context = zmq.Context();
consumer = context.socket(zmq.PULL)
consumer.connect("tcp://0.0.0.0:9998")

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}
revstates = {}
for i in states:
	revstates[states[i]]=i


scoreOfStates = {}
tweetofStates = {}

def process():
	#global scoreOfStates
	x = 0
	for i in states:
		scoreOfStates[states[i]]=0
		tweetofStates[states[i]]=0
	#print scoreOfStates
	while True:
		# print line
		try:
			x+=1
			if x==100:
				break
			TweetInfo = consumer.recv_json()
			#print(TweetInfo)
			print x
			if (TweetInfo.has_key("place")):
				if TweetInfo["place"].has_key("bounding_box"):
					if TweetInfo["place"]["bounding_box"]["coordinates"]:
						lis = TweetInfo["place"]["bounding_box"]["coordinates"]
						'''taking the average of the coordinates as the assumed
						location of the tweet and finding the corresponding state 
						using reverse geo lookup'''
						a=0
						b=0
						for i in lis[0]:
							a += i[0]
							b += i[1]
						a /= 4.0
						b /= 4.0
						state = rg.search((b,a))[0]["admin1"]
						score = 0 
						if (TweetInfo.has_key("text")):
							#print(TweetInfo['text'])
							listOfTokens = normalize(TweetInfo['text'])
							text = " ".join(listOfTokens)
							score = TextBlob(text).sentiment.polarity
						if state in states.values():
							scoreOfStates[state]+=score
							tweetofStates[state]+=1
						#print score,state
		except:
			print "Exception found"
			pass


app = Flask(__name__, static_url_path='/static/')
@app.route("/")
def hello():
	return app.send_static_file('land.html')

@app.route("/start", methods=["POST"])
def start():
	try:
		print(request.form['time'])
		return flask.json.dumps({})
	except:
		process()
		return flask.json.dumps({})
		
	#return app.send_static_file('land.html')


@app.route("/json", methods=["POST"])
def json():
	try:
		list = []
		for i in scoreOfStates:
			code = revstates[i]
			val = 0
			if tweetofStates[i]!=0:
				val+= scoreOfStates[i]/tweetofStates[i]
			list.append({"code": code,"value": val*100})
		return flask.json.dumps(list)
	except:
		list = []
		ans = []
		for i in scoreOfStates:
			code = revstates[i]
			val =0
			if tweetofStates[i]!=0:
				val = scoreOfStates[i]/tweetofStates[i]
			list.append({"code": code,"value": val*100})
		return flask.json.dumps(list)
		#return flask.json.dumps({"Afd":"Fdsa"})


	

if __name__ == '__main__':
	app.debug = True
	app.run(host="127.0.0.1", port=8080)

'''

if __name__ == '__main__':
	for i in states:
		scoreOfStates[states[i]]=0
		tweetofStates[states[i]]=0
	main()
	
	for i in scoreOfStates:
		if tweetofStates[i]!=0:
			print i,scoreOfStates[i]/tweetofStates[i]
		else:
			print i,0
			'''
