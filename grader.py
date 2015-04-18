from spellcheck import correct, words
from grammarcheck import get_sentences
from test import pos_agreement, pos_verbs
from os import walk, path
import sys
import pos

essay_path = 'essays/test'
essay_path = path.abspath(essay_path)
files = []

def process_file(file_path):
	misspelled = 0
	misspellings = []
	ovr_agreementscore = 0.0
	ovr_verbscore = 0.0
	with open(file_path, 'r') as f:
		# get misspellings
		sents = get_sentences(f.read())
		for sent in sents:
			for word in words(sent):
				if len(word) > 0 and correct(word) != word:
					misspellings.append(word)
					misspelled += 1

		# get agreemnet & verb scores
		word_count = 0
		agreementscore = 0.0
		verbscore = 0.0
		for sent in sents:
			tags = pos.get_sentence_tags(sent)
			agreementscore += pos_agreement(tags)
			verbscore += pos_verbs(tags)
			word_count+=len(tags)
		agreementscore /= word_count
		verbscore/= word_count
	
	return (misspelled, agreementscore, verbscore)

if __name__ == '__main__':
	if len(sys.argv) > 1:
		essay_path = path.abspath(sys.argv[1])

	for (dirpath, dirnames, filenames) in walk(essay_path):
		files.extend(filenames)
		break

	for fname in files:
		print '{0}'.format(fname)
		misspelled = 0
		file_path = essay_path + '\\' + fname
		misspelled, agreement, verb = process_file(file_path)
		print "\t 1a (spelling errs): {0}\n\t1b (agreement errs): {1}\n\t1c (verb errs): {2}".format(misspelled, agreement, verb)