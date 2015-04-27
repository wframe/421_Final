from spellcheck import correct, words
from textblob 		  import TextBlob, Blobber
from textblob.parsers import PatternParser
from textblob.taggers import PatternTagger
from test import pos_agreement, pos_verbs
from os import walk, path
import sys
import pos
import textcoherence as tc
import math, random
def mean(numbers):
    return sum(numbers)/float(len(numbers))
def stdev(numbers):
	avg = mean(numbers)
	variance = sum([pow(x-avg,2) for x in numbers])/float(len(numbers)-1)
	return math.sqrt(variance)
essay_path = 'essays/original/low'
essay_path = path.abspath(essay_path)
files = []

def process_file(file_path):
    misspelled = 0
    misspellings = []
    ovr_agreementscore = 0.0
    ovr_verbscore = 0.0
    with open(file_path, 'r') as f:
        t = TextBlob(f.read())
        sents = t.sentences
        cohesion = tc.coherence(t)
        return cohesion
        # get misspellings 
        #for sent in sents:
	       # for word in sent.tokens:
		      #  if len(word) > 0 and correct(word) != word:
			     #   misspellings.append(word)
			     #   misspelled += 1
		# get agreemnet & verb scores
 #       word_count = 0
 #       agreementscore = 0.0
 #       verbscore = 0.0
 #       for sent in sents:
	#        tags = pos.get_sentence_tags(sent.string)
	#        agreementscore += pos_agreement(tags)
	#        verbscore += pos_verbs(tags)
	#        word_count+=len(tags)                  
 #       agreementscore /= word_count
 #       verbscore/= word_count
        
	#return (misspelled, agreementscore, verbscore, len(sents))

if __name__ == '__main__':
    print "main"
    if len(sys.argv) > 1:
	    essay_path = path.abspath(sys.argv[1])

    for (dirpath, dirnames, filenames) in walk(essay_path):
	    files.extend(filenames)
	    break
    returns = []
    paths = ['essays/original/low','essays/original/medium','essays/original/high']
    for p in paths:
        essay_path = path.abspath(p)
        files = []
        for (dirpath, dirnames, filenames) in walk(essay_path):
	        files.extend(filenames)
	        break
        for fname in files:
            returns.append(process_file(essay_path + '\\' + fname))
        for param in map(list, zip(*returns)):
            print(str(mean(param)))
    #print '{0}'.format(fname)
    misspelled = 0
    #misspelled, agreement, verb, sents = process_file(file_path)                             
        #print "\t1a (spelling errs): {0}\n\t1b (agreement errs): {1}\n\t1c (verb errs): {2}\n\t3a (sentence count): {3}".format(misspelled, agreement, verb, sents)