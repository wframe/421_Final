from __future__ import division
import pronouns as pro
from collections import defaultdict	
from pattern.text.en import parse
import nltk
from nltk.corpus import stopwords as sw, wordnet as wn, wordnet_ic as ic
from os import path
import file_io as fio, io
from pattern.vector import Document, Model, HIERARCHICAL, Cluster
from pageparser import PageParser
from textblob import TextBlob
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
from nltk import word_tokenize
from nltk.wsd import lesk
from nltk import word_tokenize
import math
import textcoherence
from textblob_aptagger import PerceptronTagger

cachedStopWords = sw.words("english")
h_topicality_mu = ''
h_topicality_sigma = ''
def mean(numbers):
	return sum(numbers)/float(len(numbers))
def stdev(numbers):
	avg = mean(numbers)
	variance = sum([pow(x-avg,2) for x in numbers])/float(len(numbers)-1)
	return math.sqrt(variance)
def coherence(t):
	sentence_data = map(collect_sentence_data, t.sentences)
	pcontext = collect_pronouns(t)
	pronoun_score = process_pronouns(pcontext, sentence_data, t)
	return pronoun_score
def topicality(t,f):
	opinion = 0
	#for sent in t.sentences:
	#	sentipol = sent.sentiment.polarity
	#	sentisub = sent.sentiment.subjectivity        
	#	opinion += sentipol + sentisub
	#return abs(opinion/float(len(t.sentences)))
	return relevance(f)
def relevance(file):
	hvs = GetHighVectorLogSums('high')

	percepticon = PerceptronTagger()
	cat_dict = defaultdict(int)
	files = fio.recGetTextFiles('training')
	file_sum = 0
	extended_text = ExtendText(file,percepticon)
	word_count = 0
	with open(file,'r') as f:
		word_count = len(f.read().split())
	for term in extended_text.split():
		if term in hvs.keys():
			file_sum += hvs[term]

	file_sum = file_sum/len(extended_text.split())	
	return file_sum
def collect_pronouns(t):
	pcons = []
	sent_index = 0
	for sent in t.sentences:
		word_index = 0
		for word in sent.tokens:
			#if word in pro.masc or word in pro.fem:
			if word in pro.t_pers:
				pcons.append((word, sent_index, word_index))
			word_index +=1
		sent_index += 1
	return pcons
def collect_sentence_data(sent):
	#######################################################################################################
	# was going to use this NER code to detect gendered referents but the false positive rate was insane! #
	# for instance, it inferred all instances of 'Cars' as well as'Great Britain' to be people!?!?!?!?!?! #
	#######################################################################################################
	#people = []
	#for chunk in nltk.ne_chunk(sent.tags,binary=False):                  
	#    if hasattr(chunk, '_label'):
	#        person = str()
	#        if chunk._label == 'PERSON':
	#            print("found person in '" + str(chunk))
	#            for word in chunk:
	#                person += ' ' + word[0].lower()

	p = parse(sent.string)
	inNP = False
	words = p.split()
	#list of noun phrases. each phrase is a tuple of a 0 or 1 to indicate if the current phrase is in a prepositional phrase and a noun list and each noun is a tuple of noun and 'sing' or 'plur' 
	nphrase_list = []
	noun_list = []
	nphrase = ()
	length =  len(words[0])
	i = 0
	for word in words[0]:
		if 'NP' in word[2]:                        
			if not inNP:
				#this indicates we're in the first word in a noun phrase
				inNP = True
				if 'PNP' in word[3]:
					#this indicates we're in a prep phrase
					nphrase += 1,
				else:
					nphrase += 0,
			if 'NN' in word[1]:
				#current word is noun
				if 'S' in word[1]:
					noun = (word[0], 'Plur', i)
					noun_list.append(noun)
				else:
					noun = (word[0], 'Sing', i)
					noun_list.append(noun)
			elif 'PRP' in word[1]:
				#current word is pronoun
				if 'S' in word[1]:    
					noun = (word[0], 'Plur' , i)
					noun_list.append(noun)
				else:
					noun = (word[0], 'Sing' , i)
					noun_list.append(noun)
			if i == length - 1:
				nphrase += noun_list,
				nphrase_list.append(nphrase)
				inNP = False
				nphrase = ()
				noun_list = []
		elif inNP:
			nphrase += noun_list,
			nphrase_list.append(nphrase)
			inNP = False
			nphrase = ()
			noun_list = []
		i+=1                        
	return nphrase_list
def process_pronouns(pcons, sd, t):
	score = 0
	sing_score = 0
	plur_score = 0
	plurs = 0
	for pcon in pcons:
		if isSingular(pcon[0]):
			pass
			#sing_score += process_singular(pcon)
		else:
			plur_score += process_plural(pcon, sd, t)
			plurs+=1
	if plurs > 0:
		return plur_score/plurs
	else:
		return 0
def isSingular(p):
	return p not in pro.plur
def process_singular(pcon):
	#check_for_singular_antecedent
	pass
def process_plural(pcon, sd, t):
	curr = pcon[1]
	chain = [x for x in sd if sd.index(x) >= curr - 2 and sd.index(x) <= curr]   
	isCurr = True
	mostRecent = True
	score = 0
	distance_from_curr = 0
	for sent in reversed(chain):
		if isCurr:
			isCurr = False   
			for phrase in reversed(sent):
				for noun in reversed(phrase[1]):
					if pcon[2] <= noun[2]:
						pass
					else:
						if mostRecent:
							mostRecent = False
							if noun[1] == 'Sing':
								score += -2.0
							elif phrase[0] == 0:                                                                 
								score += 2.0                                 
							else:
								score += 1.5
						else:
							if noun[1] == 'Sing':
								score += -1.0
							elif phrase[0] == 0:                                                       
								score += 1.0                                 
							else:
								score += .75         
		else:
			for phrase in reversed(sent):
				for noun in reversed(phrase[1]):
					if mostRecent:
						if noun[1] == 'Sing':
							score += -1.0/distance_from_curr
						elif phrase[0] == 0:                                                                 
							score += 2.0/distance_from_curr                                 
						else:
							score += 1.5/distance_from_curr
						mostRecent = False
					else:
						if noun[1] == 'Sing':
							score += -.5/distance_from_curr
						elif phrase[0] == 0:                                                      
							score += 1.0/distance_from_curr                                 
						else:
							score += .75/distance_from_curr            
		distance_from_curr += 1                
	return score
def ExtendText(fileName,tagger=PerceptronTagger()):
	with io.open(fileName, 'r') as w:
		text = TextBlob(w.read(), pos_tagger=tagger)
		extended_text = []
		for sent in text.sentences:		
			for word in sent.pos_tags:
				#word = "bank"
				penn_tags = ['JJ','NN','V']
				extending = False
				for tag in penn_tags:
					if tag in word[1]:
						extending = True
						pos = tag[0].lower()
						try:
							l = lesk(sent.string, word[0].lower(), pos)
							syns = l._lemma_names
							for syn in syns:
								extended_text.append(syn)
							break
						except:
							extended_text.append(word[0].lower())
				if not extending:
					extended_text.append(word[0].lower())
		extended_text = ' '.join([word for word in extended_text if word not in cachedStopWords]).lstrip()
		return extended_text
def GetVectors():
	essay_path = 'training'
	files = fio.recGetTextFiles(path.abspath(essay_path))
	docs = []
	percepticon = PerceptronTagger()
	cat_dict = defaultdict(int)
	for f in files:
		extended_text = ExtendText(f, percepticon)
		name = ''
		cats = ['high','medium','low']			
		for cat in cats:
			if cat in f:
				name = cat+str(cat_dict[cat])
				cat_dict[cat] += 1				
		docs.append(Document(extended_text, name=name, top=None))
	m = Model(docs)
	#lsa = m.reduce(5)
	return m
def GetHighVectorLogSums(label):
	m = GetVectors()
	high_tf_sums = defaultdict(float)
	for corpuscle in m._documents:
		if label in corpuscle._name:
			for tf in corpuscle.vector:
				high_tf_sums[tf] -= math.log(corpuscle.vector[tf])
	return high_tf_sums  
if __name__ == '__main__':
	hvs = GetHighVectorLogSums('high')

	percepticon = PerceptronTagger()
	cat_dict = defaultdict(int)
	files = fio.recGetTextFiles(r'C:\Users\William\Desktop\421_Final\training')
	file_sums = []
	for file in files:
		file_sum = 0
		extended_text = ExtendText(file,percepticon)
		word_count = 0
		with open(file,'r') as f:
			word_count = len(f.read().split())
		for term in extended_text.split():
			#learn below weights through experimentation
			if term in hvs.keys():
				file_sum += hvs[term]
		file_sums.append(file_sum/len(extended_text.split()))	
	print('mean' + str(mean(file_sums)))
	print('stdev' + str(stdev(file_sums)))