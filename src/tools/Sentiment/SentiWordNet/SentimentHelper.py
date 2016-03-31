import re
import nltk
import codecs
from nltk.corpus import wordnet as wn


dictOfWordNet = {}

def initialiseDictionary(filename):
   dic={}
   lines = codecs.open(filename, "r", "utf8").read().splitlines()
   lines = filter((lambda x : not re.search(r"^\s*#", x)), lines)
   for i, line in enumerate(lines):
       fields = re.split(r"\t+", line)
       fields = map(unicode.strip, fields)
       pos, offset, pos_score, neg_score, synset_terms, gloss = fields
       if pos and offset:
           offset = int(offset)
           dic[(pos,offset)] = (float(pos_score), float(neg_score))
   return dic

def init():
    dictOfWordNet = initialiseDictionary('SentiWordNet_3.0.0_20100705.txt')

def getWordNetPos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wn.ADJ
    elif treebank_tag.startswith('V'):
        return wn.VERB
    elif treebank_tag.startswith('N'):
        return wn.NOUN
    elif treebank_tag.startswith('R'):
        return wn.ADV
    else:
        return ''

def calculate(listOfTokens):
    score=0
    listOfTokens = nltk.pos_tag(listOfTokens)
    for token in listOfTokens:
        negScore=0
        posScore=0
        tag = getWordNetPos(token[1])
        synset_list = wn.synsets(token[0],tag)
        for synset in synset_list:
            pos = synset.pos
            offset = synset.offset
            if (pos, offset) in dictOfWordNet:
                pos_score, neg_score = dictOfWordNet[(pos, offset)]
                if pos_score>neg_score:
                    posScore+=1
                elif neg_score>pos_score:
                    negScore+=1
        if negScore>posScore:
            score= score-1
        elif negScore<posScore:
            score+=1

    if score>0:
        return (score,1)
    elif score==0:
        return (score,0)
    else:
        return (score,-1)

if __name__=="__main__":
    print calculate(['happy'])


'''


class SentimentHelper:
    _dictOfWordNet = {}

    @staticmethod
    def initialiseDictionary(filename):
       dic={}
       lines = codecs.open(filename, "r", "utf8").read().splitlines()
       lines = filter((lambda x : not re.search(r"^\s*#", x)), lines)
       for i, line in enumerate(lines):
           fields = re.split(r"\t+", line)
           fields = map(unicode.strip, fields)
           pos, offset, pos_score, neg_score, synset_terms, gloss = fields
           if pos and offset:
               offset = int(offset)
               dic[(pos,offset)] = (float(pos_score), float(neg_score))
       return dic

    def __init__(self):
        self._dictOfWordNet = self.initialiseDictionary('SentiWordNet_3.0.0_20100705.txt')

    @staticmethod
    def getWordNetPos(treebank_tag):
        if treebank_tag.startswith('J'):
            return wn.ADJ
        elif treebank_tag.startswith('V'):
            return wn.VERB
        elif treebank_tag.startswith('N'):
            return wn.NOUN
        elif treebank_tag.startswith('R'):
            return wn.ADV
        else:
            return ''

    @staticmethod
    def calculate(self,listOfTokens):
        score=0
        listOfTokens = nltk.pos_tag(listOfTokens)
        for token in listOfTokens:
            negScore=0
            posScore=0
            tag = self.getWordNetPos(token[1])
            synset_list = wn.synsets(token[0],tag)
            for synset in synset_list:
                pos = synset.pos
                offset = synset.offset
                if (pos, offset) in self._dictOfWordNet:
                    pos_score, neg_score = self._dictOfWordNet[(pos, offset)]
                if pos_score>neg_score:
                    posScore+=1
                elif neg_score>pos_score:
                    negScore+=1
            if negScore>posScore:
                score= score-1
            elif negScore<posScore:
                score+=1

        if score>0:
            return (score,1)
        elif score==0:
            return (score,0)
        else:
            return (score,-1)
'''






































