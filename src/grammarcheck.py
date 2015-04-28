import os
from nltk.parse import stanford

#curr_dir, garbage = os.path.split(os.path.abspath(__file__));
#os.environ['STANFORD_PARSER'] = os.path.join(curr_dir, 'stanford-parser')
#os.environ['STANFORD_MODELS'] = os.path.join(curr_dir, 'stanford-parser')
#PCFG_PATH = os.path.join(curr_dir, 'stanford-parser\\edu\\stanford\\nlp\\models\\lexparser\\englishPCFG.ser.gz')
#os.environ['JAVAHOME'] = 'C:\\Program Files\\Java\\jre1.8.0_25\\bin\java.exe'
#parser = stanford.StanfordParser(model_path=PCFG_PATH)

def parse_sentences(sents):
	return parser.raw_parse_sents((sents))

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

