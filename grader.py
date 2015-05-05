from __future__ import division
from src              import *
from src.test         import pos_agreement, pos_verbs, pos_global_verbs
from src.scoring      import syntax, topicality
from src.spellcheck   import correct, words
from textblob         import TextBlob, Blobber
from textblob.parsers import PatternParser
from textblob.taggers import PatternTagger
from pattern.text.en import tag as tag_sent
from os               import walk, path
import src.textcoherence as tc
import sys
import src.pos as pos
import math, random
import numpy

#precomputed training means
paramStats = []
spellingStats= (55.9833, 19.5114)
agreementStats = (.2059, .0934)
verbStats = (.1218, .0761)
parseStats =  (0, 1)
pronsStats = (-3.3233,6.0137)
#opinionStats = (.4816,.1227 )
#relevanceStats = (124.74,26.63)
topicalityStats = (25.926,5.469)
lengthStats = (13.4667, 6.4924)

def mean(numbers):
	return sum(numbers)/float(len(numbers))
def stdev(numbers):
	avg = mean(numbers)
	variance = sum([pow(x-avg,2) for x in numbers])/float(len(numbers)-1)
	return math.sqrt(variance)
def computeZ(param, mu, dev):
	return (param - mu)/dev
essay_path = 'training'
essay_path = path.abspath(essay_path)
files = []

def process_file(file_path):
	misspelled = 0
	misspellings = []

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
					misspelled += -1
		#get agreement & verb scores
		word_count = 0
		agreementscore = 0.0
		verbscore = gverbs 
		for sent in sents:
			tags = tag_sent(sent.string)
			agreementscore += pos_agreement(tags)/len(tags)
			verbscore += (pos_verbs(tags)/len(tags))
		#parse_score = syntax.syntactic_score(text)
		parse_score = 0

		verbscore = 0
		
		#topic_score = topicality.topicality_score(text)
		topic_score = tc.topicality(text,file_path)

	return [misspelled, agreementscore, verbscore, parse_score, cohesion, topic_score, len(sents)]

if __name__ == '__main__':
	returns = []
	if len(sys.argv) > 1:
		essay_path = path.abspath(sys.argv[1])
	misspelled = 0 
	for (dirpath, dirnames, filenames) in walk(essay_path):
		files.extend(filenames)
		break
	#paths = ('input/original/',)
	paths = ('input/original/low','input/original/medium','input/original/high')
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
				print "processing {0}...".format(fname)
				param = process_file(essay_path + '\\' + fname)

				ret = process_file(essay_path + '\\' + fname)
		
				#precomputed stats based on training data
				paramStats = []
				spellingStats= (-55.9833, 19.5114)
				agreementStats = (-.9411, .6866)
				#verbStats = (0, 1.3521)
				verb1Stats = (-.9411,)
				verb2Stats = (0, 1.3521)
				verbStats = (0, 1)
				parseStats =  (0, 1)
				pronsStats = (-3.3233,6.0137)
				#topicalityStats = (.4816,.1227 )
				topicalityStats = (25.926,5.469)
				lengthStats = (13.4667, 6.4924)
				paramStats.append(spellingStats)
				paramStats.append(agreementStats)
				paramStats.append(verbStats)
				paramStats.append(parseStats)
				paramStats.append(pronsStats)
				paramStats.append(topicalityStats)
				paramStats.append(lengthStats)
	
				fscore = 0
				fscores = []
				label = 0
				j = 0
				for param in ret:
					fscores.append(computeZ(param, paramStats[j][0], paramStats[j][1]))
					j+=1
				fscore +=  (1*fscores[0]) + (1*fscores[1]) + .5*fscores[2] + .5*fscores[3] + (2*fscores[4]) + (2*fscores[5]) + (3*fscores[6]) + (3*fscores[7])
				if fscore < -4.74:
					label = 0
				elif fscore < 4.74:
					label = 1
				else:
					label = 2

				LABELS = ['low', 'medium', 'high']
				out.write("{0:12}".format(fname))
				for val in fscores:
					if isinstance(val, (int, long, float, complex)):
						out.write("{0:6} ".format(round(val, 2)))
				out.write(LABELS[label])
				out.write('\n')
