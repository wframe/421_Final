from pattern.vector import Document, NB, SVM, count, DETECTION
from pattern.en		import tag
from bs4			import BeautifulSoup, Comment

HEADLINES_CORPUS = 'headlines.txt'
TEST_DOC = 'Corpus\\News\\2014\'s most challenged books - CNN.com.htm'

def process_text(text):
	if text is None:
		return None

	features = {}

	# Count occurence of pos tags
	pos = tag(text)
	features.update(count([word for word,pos in tag(text)]))

	if text.startswith("<"):
		print text
		print features
		print '\n'

	# Consider total length of region text & region tag name
	#features['length'] 	  = len(text)


	return features	

class HtmlNewsHandler:
	def __init__(self, text):
		self._raw_html = text
		self._raw_soup = BeautifulSoup(text)
		self._classifier = None	

	@property
	def text(self):
		if self._classifier == None or self._text == None:
			# Train naive bayes model with a small corpus of generic English sentences
			self._classifier = SVM(type=DETECTION)
			with open(HEADLINES_CORPUS) as f:
				for line in f:
					self._classifier.train(process_text(line), type='valid_english')

			# eliminate all style, script & head tags
			[tag.extract() for tag in self._raw_soup.find(['script', 'style' 'head'])]
			# crawl over doc testing all tags to see if they're readable english
			self._text = ""
			for text in self._raw_soup.findAll(text=True):
				# we know a few places text won't be
				if text.parent.name not in ['style', 'script', 'head'] and not isinstance(text, Comment):
					if text.strip() != '' and self._classifier.classify(process_text(text.strip())):
						self._text += ' ' + text.strip()
			self._text = self._text.replace('\n',' ')
		return self._text

if __name__ == "__main__":
	with open(TEST_DOC) as f:
		news = HtmlNewsHandler(f.read())
		print(news.text)