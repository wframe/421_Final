from __future__ import division
from textblob_aptagger import PerceptronTagger
from itertools import tee, islice, chain, izip
from textblob  import TextBlob
import os 
from os import path
import fnmatch
from spellcheck import correct
from textblob import TextBlob
import math
def recGetTextFiles(directory):
	matches = []
	for root, dirnames, filenames in os.walk(directory):
	  for filename in fnmatch.filter(filenames, '*.txt'):
		matches.append(os.path.join(root, filename))
	return matches
#http://stackoverflow.com/questions/1011938/python-previous-and-next-values-inside-a-loop
def previous_and_next(some_iterable):
    prevs, items, nexts = tee(some_iterable, 3)
    prevs = chain([None], prevs)
    nexts = chain(islice(nexts, 1, None), [None])
    return izip(prevs, items, nexts) 
def computeZ(param, mu, dev):
	return (param - mu)/dev        
def pos_agreement(tags):
    errs = 0
    prev = ""
    verb_err = []
    verb_tags = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
    hasNoun  = False
    for curr in tags:
        if not hasNoun and curr in ['NN','NNS','NNP','NNPS','PRP$','PRP']:
            hasNoun = True
        if prev:
            if verb_err != []:
                if curr in verb_tags:
                    if curr in verb_err:
                        errs +=  10
                    verb_err = []
            elif curr == "NN" and prev != "DT":
                verb_err = ["VBP", "VBN"]
            elif curr == "NNS" and prev != "DT":
                verb_err = ["VBZ", "VBD"]
            elif curr == "NNP":
                verb_err = ["VBP"]
            elif curr == "NNPS":
                verb_err = ["VBZ"]
            elif prev == "DT" and (curr != "NN" and curr != "NNS"):
                errs += 1
            elif prev == "PRP$" and curr not in ["NN", "NNS", "JJ", "JJR", "JJS"]:
                errs += 1
        prev = curr
    if not hasNoun:
        errs += 1
    return -1 * errs
    
def pos_verbs(tags):
    errors = 0
    present = True
    if "VBN" in tags or "VBD" in tags:
        present = False

    verb_count = 0
    pres_tags = ['VB','VBZ','VBP','VBG']
    verb_tags = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
    for previous, current, nxt in  previous_and_next(tags):
        if not present and current in pres_tags:
            errors += 1

        if current in verb_tags:
            verb_count += 1
        elif current == "CC":
            if verb_count == 0:
                errors += 1
            verb_count = 0

    if verb_count == 0:
        errors += 1
    return -1 * errors

def pos_global_verbs(taglists):
    verbs = 0
    pastverbs = 0
    for tagtuple in taglists:
        if tagtuple[1] in ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]:
            verbs += 1
            if tagtuple[1] not in ['VB','VBZ','VBP','VBG']:
                pastverbs += 1
    return abs((pastverbs/verbs)-1)

def agreement_score(text):
    t = TextBlob(text)
    agreementscore = 0.0
    for sent in t.sentences:
        tags = sent.tags
        agreementscore += pos_agreement(tags)               
    agreementscore /= len(t.words)
    return agreementscore

def verb_tense_score(text):
    t = TextBlob(text)
    verbscore = 0.0
    for sent in t.sentences:
        tags = sent.tags
        verbscore += pos_verbs(tags) 
    verbscore/= len(t.words)
    return verbscore

def misspelling_score(text):
    misspellings = 0
    t = TextBlob(text)
    for w in t.words:
        if correct(w) != w:
            misspellings += 1
    print "\t{0} miss in {1} words".format(misspellings, len(t.words))
    return misspellings/len(t.words)

def sentences_score(text):
    return len(TextBlob(text).sentences)
def mean(numbers):
	return sum(numbers)/float(len(numbers))
def stdev(numbers):
	avg = mean(numbers)
	variance = sum([pow(x-avg,2) for x in numbers])/float(len(numbers)-1)
	return math.sqrt(variance)
if __name__ == '__main__':
	percepticon = PerceptronTagger()
	files = recGetTextFiles(r'C:\Users\William\Desktop\421_Final\training')
	verb_sums = []
	lverb_sums = []
	gverb_sums = []
	agree_sums = []
	for file in files:
		with open(file,'r') as f:
			text = TextBlob(f.read(), pos_tagger=percepticon)
			gverbs = pos_global_verbs(text.tags)
			lverbs = 0
			agree = 0
			for sent in text.sentences:
				tags = sent.tags
				if len(tags) > 0:
					lverbs += (pos_verbs(tags)/len(tags))
					agree += (pos_agreement(tags)/len(tags))
			gverb_sums.append(gverbs)
			lverb_sums.append(lverbs)
			agree_sums.append(lverbs)
			verb_sums.append(computeZ(lverbs,-.941085997745,.686621431068)+computeZ(gverbs, .881815018201, .0764697386088))
	print('lverb mean' + str(mean(lverb_sums)))
	print('lverb stdv' + str(stdev(lverb_sums)))
	print('gverb mean' + str(mean(gverb_sums)))
	print('gverb stdv' + str(stdev(gverb_sums)))
	print('z computed mean' + str(mean(verb_sums)))
	print('z computed stdv' + str(stdev(verb_sums)))
	print('agree mean' + str(mean(agree_sums)))
	print('agree stdv' + str(stdev(agree_sums)))
	print('predicted mean : -.06')
	print('predicted stdev : 1.6')