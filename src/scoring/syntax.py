from __future__ import division
from nltk.parse import stanford
from textblob 	import TextBlob
import os
import nltk

ROOT_DIR = r'C:\Users\William\Desktop\421_Final'
JAVA_HOME =  r"C:\Program Files\Java\jre1.8.0_45\bin\java.exe"

os.environ['STANFORD_PARSER'] = ROOT_DIR + r'\src\scoring\stanford-parser'
os.environ['STANFORD_MODELS'] = ROOT_DIR + r'\src\scoring\stanford-parser'
os.environ['JAVA_HOME']		  = JAVA_HOME
#parser = stanford.StanfordParser(model_path=os.environ['STANFORD_PARSER'] + r"\edu\stanford\nlp\models\lexparser\englishPCFG.ser.gz")

def syntactic_score(text):
	t = TextBlob(text)
	sentences = [unicode(x) for x in t.sentences]
	#sentences = parser.raw_parse_sents([unicode(x) for x in t.sentences])
	#sentences = parser.raw_parse_sents(["My dog with a broken leg I not want"])

	bad_leaves = 0
	leaf_count = 1
	# GUI
	for sent in sentences:
		# Stanford parser chokes on large sentences
		# if the sentences is longer than 60 words,
		# I'll give the essay a large hit for a run-on and continue
		if len(sent.split()) > 50:
			bad_leaves += 15
			leaf_count += 15

		for s in parser.raw_parse(sent):
			# We're at the ROOT, explore all the subtrees
			for t in s:
				bd, cnt = syn_rec(t, s.label())
				bad_leaves += bd
				leaf_count += cnt

	return bad_leaves / leaf_count

def syn_rec(leaf, parent_label):
	bad_leaves = 0
	leaf_count = 1
	all_bad = False

	if isinstance(leaf, nltk.tree.Tree):

		if leaf.label() == 'FRAG':
			# fragment
			all_bad = True

		if leaf.label() == 'SBAR' and parent_label != 'VP' and leaf[0].label != 'IN':
			# embedded SBAR
			all_bad = True

		for t in leaf:
			bd, cnt = syn_rec(t, leaf.label())
			bad_leaves += bd
			leaf_count += cnt

		# if we have a fragment or a misplaced SBAR, all the leaves 
		# under this one are bad so we only care about the count
		if all_bad:
			return (leaf_count, leaf_count)
		else:
			return (bad_leaves, leaf_count)
	else:
		return (0,1)