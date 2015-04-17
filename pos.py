import nltk

def get_sentence_tags(sentence): 
    return [x[1] for x in nltk.pos_tag(nltk.word_tokenize(sentence))    ]

