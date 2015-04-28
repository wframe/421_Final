from __future__ import division
from spellcheck import correct, words
from textblob 		  import TextBlob, Blobber
from textblob.parsers import PatternParser
from textblob.taggers import PatternTagger
from test import pos_agreement, pos_verbs, pos_global_verbs
from clean.scoring import syntax, topicality
from os import walk, path
import sys
import pos
import textcoherence as tc
import math, random
#precomputed training means
spellingMean = 55.9833
spellingSDev = 19.5114
agreementMean = .2078
agreementSDev = .095
verbsMean = .06556
verbsSDev = .03331
parseMean = -3.3233
parseSDev = 6.0137
pronsMean = 0
pronsSDev = 0
topicalityMean = .4816
topicalitySDev = .1227 
lengthMean = 13.4667
lengthSDev = 6.4924
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
        text = f.read()
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
            tags = pos.get_sentence_tags(sent.string)
            agreementscore += pos_agreement(tags)/len(t.words)
            verbscore += gverbs+ (pos_verbs(tags)/len(t.words))

        parse_score = syntax.syntactic_score(text)
        topic_score = topicality.topicality_score(text)


	return [misspelled, agreementscore, verbscore, cohesion[0], cohesion[1], len(sents), parse_score, topic_score]

if __name__ == '__main__':
    returns = []
    if len(sys.argv) > 1:
	    essay_path = path.abspath(sys.argv[1])
    misspelled = 0 
    for (dirpath, dirnames, filenames) in walk(essay_path):
	    files.extend(filenames)
	    break
    paths = ('essays/original/low','essays/original/medium','essays/original/high')
    #for testing
    i = -1
    for p in paths:
        print(p)
        essay_path = path.abspath(p)
        files = []
        for (dirpath, dirnames, filenames) in walk(essay_path):
	        files.extend(filenames)
	        break
        for fname in files:
            returns.append(process_file(essay_path + '\\' + fname))
    for param in map(list, zip(*returns)):
        print(str(mean(param)))
        print(str(stdev(param)))

    #print '{0}'.format(fname)
                           
        #print "\t1a (spelling errs): {0}\n\t1b (agreement errs): {1}\n\t1c (verb errs): {2}\n\t3a (sentence count): {3}".format(misspelled, agreement, verb, sents)