from spellcheck import correct, words
from os import walk, path

essay_path = 'essays/original/low/'
essay_path = path.abspath(essay_path)
files = []

def get_sentences(text):
	sents = []
	punc = ['.', '?', '!']
	sent = ""
	per_count = 0
	in_quote = False
	for char in text:
		if char not in punc:
			if per_count == 1:
				sent += '.'
				if not in_quote:
					sents.append(sent)
					sent = ""
			if char == '"':
				in_quote = not in_quote

			per_count = 0
			sent += char
		elif char in punc and char != '.' and sent.strip() != "":
			if not in_quote:
				sents.append(sent)
				sent = ""
			else:
				sent += char
		elif char == '.':
			per_count += 1
			if per_count == 3:
				# this is an ellipses
				sent += "..."
			elif per_count > 3:
				# this is some malformed ellipses
				print "malformed ellipses found"
				sent += '.'
				sents.append(sent)
				sent = ""
	if not sent.strip() == "":
		sents.append(sent)

	return sents

if __name__ == '__main__':
	for (dirpath, dirnames, filenames) in walk(essay_path):
		files.extend(filenames)
		break

	do_one = True
	for fname in files:
		print '{0}'.format(fname)
		misspelled = 0
		file_path = essay_path + '\\' + fname
		with open(file_path, 'r') as f:
			for line in f:
				for word in words(line):
					if len(word) > 0 and correct(word) != word:
						misspelled = misspelled + 1
		print '	{0} spelling mistakes'.format(misspelled)


		with open(file_path, 'r') as f:
			print '	sentences '
			for sent in get_sentences(f.read()):
				print "	{0}".format(sent)