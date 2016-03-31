class SentimentHelper:
    _positiveWordsList = []
    _negativeWordsList = []

    @staticmethod
    def initialiseWordList(filename):
        words = []
        with open(filename) as f:
            for line in f:
                words.append(str(line))
        f.close()
        return set(words)

    def __init__(self):
        self._positiveWordsList = self.initialiseWordList('positive-words.txt')
        self._negativeWordsList = self.initialiseWordList('negative-words.txt')

    @staticmethod
    def calculate(self,listOfTokens):
        score = 0.0
        for token in listOfTokens:
            print token,
            if token in self._negativeWordsList:
                score -= -1.0
            elif token in self._positiveWordsList:
                score += 1

        if score > 0:
            return 1
        elif score == 0:
            return 0
        else:
            return -1
