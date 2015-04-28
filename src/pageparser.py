from textblob 		  import TextBlob, Blobber
from textblob.parsers import PatternParser
from textblob.taggers import PatternTagger
from HTMLParser 	  import HTMLParser
import io

class PageParser(HTMLParser):
	SELF_CLOSING = ['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'keygen', 'link', 'menuitem', 'meta', 'param', 'source', 'track', 'wbr']
	CLOSING_PUNC = ['?', '!', '.']

	def __init__(self):
		self.tag_stack = []
		self.ignore_data = False
		self.parsed_text = ''
		self.blobber = Blobber(parser=PatternParser(), pos_tagger=PatternTagger())
		HTMLParser.__init__(self)

	def handle_starttag(self, tag, attrs):
		#with io.open(r'test.txt', 'a', encoding='utf-8') as w:
		#	w.write(unicode("{0}\n".format(tag)))
		if tag not in PageParser.SELF_CLOSING:
			self.tag_stack.append(tag)
		if tag in ['script','style','head']:
			self.ignore_data = True

	def handle_endtag(self, tag):
		#with io.open(r'test.txt', 'a', encoding='utf-8') as w:
		#	w.write(unicode("/{0}\n".format(tag)))
		if tag == self.tag_stack[-1]:
			self.tag_stack.pop()
			self.ignore_data = False

	def handle_data(self, data):
		# Get rid of trailing whitespace and newlines
		text = data.strip().replace('\n', '')
		if text != "" and not self.ignore_data:
			blob = self.blobber(text)

			# Simple heuristic - only include text that's a well-formed sentence
			# This fails on malformed sentences like "10 a.m." 
			# but should be a decent heuristic for the data we want
			if len(blob.sentences) > 1 or blob.sentences[0][-1] in PageParser.CLOSING_PUNC:
				self.parsed_text += text + ' '

	def process(self, html):
		self.feed(html)
		return self.parsed_text

	@classmethod
	def parse(cls, html):
		p = PageParser()
		return p.process(html)

if __name__ == '__main__':
	with io.open(r'Corpus\News\How Lincoln Crafted Its New Super-Deluxe Sound System _ WIRED.htm', 'rU', encoding='utf-8') as input: 
		p = PageParser()
		with io.open(r'test.txt', 'a', encoding='utf-8') as w:
			w.write(p.process(input.read()))