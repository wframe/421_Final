import nltk, string

def get_sentence_tags(sentence): 
    #return [x[1] for x in nltk.pos_tag(nltk.word_tokenize(sentence.translate(string.maketrans("",""), string.punctuation) ))    ]
    return [x[1] for x in nltk.pos_tag(nltk.word_tokenize(sentence))    ]

