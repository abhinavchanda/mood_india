class SentimentHelper:
	_dictOfScores = {}

	@staticmethod
	def initialiseDictionary(filename):
		dic={}
		with open(filename) as f:
			for line in f:
				word,score=line.split('\t')
				score=int(score)
				dic[word]=score
		return dic

	def __init__(self):
		self._dictOfScores = self.initialiseDictionary('AFINN-111.txt')

	@staticmethod
	def calculate(self,listOfTokens):
		score=0.0
		for token in listOfTokens:
			if self._dictOfScores.has_key(token):
				score += self._dictOfScores[token]

		if score > 0:
			return 1
		elif score == 0:
			return 0
		else:
			return -1
