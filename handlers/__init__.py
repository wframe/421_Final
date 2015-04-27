import nltk
from textblob 		  import Blobber, TextBlob
from textblob.taggers import PatternTagger
from textblob.parsers import PatternParser
from bs4 	 	 	  import BeautifulSoup, Comment
from pattern.vector   import SVM, count, DETECTION
from pattern.en		  import tag

SENTENCES_CORPUS = 'headlines.txt'

TAGS = {
	'NOUN': ['NN', 'NNS', 'NNP', 'NNPS']
}

def process_text(text):
	if text is None:
		return None

	# Count occurence of pos tags
	return count([word for word,pos in tag(text)])	

class HtmlHandler:
	__classifier = None

	def __init__(self, html):
		self._raw_html   = html
		self._raw_soup 	 = BeautifulSoup(html)
		self._text 		 = None

	@property
	def text(self):
		if HtmlHandler.__classifier == None:
			# Train naive bayes model with a small corpus of generic English sentences
			HtmlHandler.__classifier = SVM(type=DETECTION)
			with open(SENTENCES_CORPUS) as f:
				for line in f:
					HtmlHandler.__classifier.train(process_text(line), type='valid_english')

		if self._text == None:
			# crawl over doc testing all tags to see if they're readable english
			self._text = ""
			for text in self._raw_soup.findAll(text=True):
				# we know a few places text won't be
				if text.parent.name not in ['style', 'script', 'head'] and not isinstance(text, Comment):
					if text.strip() != '' and HtmlHandler.__classifier.classify(process_text(text)):
						self._text += ' ' + text.strip()
			self._text = TextHandler(self._text.replace('\n',' '))
		return self._text

class TextHandler:
	def __init__(self, text):
		self._raw_text = text
		self._sentences = None
		self._blobber = Blobber(parser = PatternParser(), pos_tagger = PatternTagger())
		self._text_dirty = False

	def __str__(self):
		return self._raw_text

	@property
	def sentences(self):
		if self._sentences is None or self._text_dirty:
			self._sentences = []
			sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
			for sent in sent_detector.tokenize(self._raw_text):
				self._sentences.append(self._blobber(sent))
		return self._sentences

	@property
	def words(self):
		words = []
		for sent in self.sentences:
			words.extend(map(lambda (word,pos): word, sent.tags))
		return words

	# remove all tags if they don't satisfy a certain func
	def filter_words(self, func):
		new_text = ''
		for sent in self.sentences:
			for word,pos in sent.tags:
				if func((word,pos)):
					new_text += ' ' + word
		self._raw_text = new_text
		self._text_dirty = True