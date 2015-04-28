from __future__ import division
from src              import *
from src.test         import pos_agreement, pos_verbs, pos_global_verbs
from src.scoring      import syntax, topicality
from src.spellcheck   import correct, words
from textblob         import TextBlob, Blobber
from textblob.parsers import PatternParser
from textblob.taggers import PatternTagger
from pattern.en import tag as tag_sent
from os               import walk, path
import src.textcoherence as tc
import sys
import src.pos as pos
import math, random

#precomputed training means
paramStats = []
spellingStats= (55.9833, 19.5114)
agreementStats = (.2059, .0934)
verbStats = (.06556, .03331)
parseStats =  (0, 1)
pronsStats = (-3.3233,6.0137)
topicalityStats = (.4816,.1227 )
lengthStats = (13.4667, 6.4924)



def mean(numbers):
    return sum(numbers)/float(len(numbers))
def stdev(numbers):
	avg = mean(numbers)
	variance = sum([pow(x-avg,2) for x in numbers])/float(len(numbers)-1)
	return math.sqrt(variance)
def computeZ(param, mu, dev):
    return (param - mu)/dev
essay_path = 'essays/original/low'
essay_path = path.abspath(essay_path)
files = []

def process_file(file_path):
    misspelled = 0
    misspellings = []
    ovr_agreementscore = 0.0
    ovr_verbscore = 0.0
    with open(file_path, 'r') as f:
        text = unicode(f.read())
        t = TextBlob(text)
        sents = t.sentences
        cohesion = tc.coherence(t)
        #get misspellings
        gverbs = pos_global_verbs(t.tags)
        for sent in sents:
	        for word in sent.tokens:
		        if len(word) > 0 and correct(word) != word:
			        misspellings.append(word)
			        misspelled += 1
		#get agreement & verb scores
        word_count = 0
        agreementscore = 0.0
        verbscore = 0.0
        for sent in sents:
            tags = tag_sent(sent.string)
            agreementscore += pos_agreement(tags)/len(t.words)
            verbscore += gverbs+ (pos_verbs(tags)/len(t.words))

        parse_score = 0#syntax.syntactic_score(text)
        topic_score = topicality.topicality_score(text)


	return (misspelled, agreementscore, verbscore, cohesion[0], cohesion[1], len(sents), parse_score, topic_score)

if __name__ == '__main__':
    returns = []
    if len(sys.argv) > 1:
	    essay_path = path.abspath(sys.argv[1])
    misspelled = 0 
    for (dirpath, dirnames, filenames) in walk(essay_path):
	    files.extend(filenames)
	    break
    paths = ('input/original',)
    #for testing
    i = -1
    with open(r'output\result.txt', 'w+') as out:
        for p in paths:
            print(p)
            essay_path = path.abspath(p)
            files = []
            for (dirpath, dirnames, filenames) in walk(essay_path):
	           files.extend(filenames)
	           break
            for fname in files:
                tup = process_file(essay_path + '\\' + fname)
                out.write("%s" % (tup,))
                out.write('\n')
