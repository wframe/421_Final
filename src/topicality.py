from __future__ import division
from pattern.text.en import tag
from pattern.text.en import wordnet, NOUN

ESSAY_TOPIC = 'In twenty years, there will be fewer cars in use than there are today.'
#For speed, store the nouns from the essay topic
ESSAY_NOUNS = [
			wordnet.synsets(u'years', pos=NOUN)[1],
			wordnet.synsets(u'car', pos=NOUN)[0],
			wordnet.synsets(u'use', pos=NOUN)[0],
			wordnet.synsets(u'today', pos=NOUN)[0]
		   ]
SIMILARITY_THRESHOLD = 0.50

# Could potentially expand this to account for the whole noun phrase
def topicality_score(text):
	# loop through all nouns 
	# (this should give some idea of what's being discussed)
	noun_count = 0
	related_nouns = 0
	for word, pos in tag(text):
		if pos in ['NN', 'NNS', 'NNP', 'NNPS']:
			noun_count += 1
			syn_possibility = wordnet.synsets(word, pos=NOUN)
			for essay_word in ESSAY_NOUNS:
				for synword in syn_possibility:
					sim = wordnet.similarity(synword, essay_word)
					if sim > SIMILARITY_THRESHOLD:
						related_nouns += 1
						break

	if noun_count > 0:
		return related_nouns / noun_count	
	else:
		return 0
