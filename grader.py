from spellcheck import correct, words
from os import walk, path

essay_path = 'essays/original/high/'
essay_path = path.abspath(essay_path)
files = []

if __name__ == '__main__':
	for (dirpath, dirnames, filenames) in walk(essay_path):
		files.extend(filenames)
		break
	for fname in files:
		misspelled = 0
		with open(essay_path + '\\' + fname, 'r') as f:
			for line in f:
				for word in words(line):
					if len(word) > 0 and correct(word) != word:
						misspelled = misspelled + 1
		print '{0} mistakes in {1}'.format(misspelled, fname)
	