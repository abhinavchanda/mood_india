import re,sys,string
from nltk.corpus import stopwords
import SpellingCorrector.spell as corrector
import nltk.stem.lancaster

# TODO Refactor code into static class

stop_words = set(stopwords.words('english'))
stemmer = nltk.stem.lancaster.LancasterStemmer()

# unicodify(): will encode text as per unicode format
def unicodify(word):
	return word.encode('utf-8')

def tolower(word):
	return word.lower()

# goodify(): will remove characters in a word that occur more than three two times
def goodify(word):
	a = '$'
	b = '$'
	c = '$'
	ret = ''
	for x in word:
		a = b
		b = c
		c = x
		if a==b and b==c:
			continue
		else:
			ret+=x
	return ret

#clean(): Removes all punctuations and newlines, returns list of words.
def tokenize(text):
	regex = re.compile('[%s]' % re.escape(string.punctuation))
	text = regex.sub('', text)
	return text.split()

def preprocess(tweet):
	tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',tweet)
	tweet = re.sub('@[^\s]+','',tweet)
	tweet = re.sub('[\s]+', ' ', tweet)
	tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
	tweet = tweet.strip('\'"')
	tweet.replace("'","");
	tweet.replace('"','');
	return tweet


#normalize(): main driver function
def normalize(text):
	# text = unicodify(text)o
	text = preprocess(text)
	text = tokenize(text)
	return sanitize(text)

#stem(): does Stemming + Correct , so as to get stemmed word which actually lies in the dictionary
def stem(word):
	# word = stemmer.stem(word)
	word = corrector.correct(word)
	return word

#########
# sanitize():
# 1. Converts to lowercase
# 2. goodifies words
# 3. Removes Stop-Words
# 4. Spell-Corrects the word
# 5. Again checks for possible stop-words
##########
def sanitize(text):
	ret = []
	for word in text:
		word = tolower(word)
		#word = goodify(word)
		#print word
		word = corrector.correct(word)
		ret.append(word)
		'''if word not in stop_words:
			word = stem(word)
			
		else:
			continue'''
	return ret

if __name__ =='__main__':
	st = 'i dfsf fds  fd  fds https://www.ggogle.co @anfdsa'
	print normalize(st)
