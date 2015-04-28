from __future__ import division
from itertools import tee, islice, chain, izip
from textblob  import TextBlob
from spellcheck import correct

#http://stackoverflow.com/questions/1011938/python-previous-and-next-values-inside-a-loop
def previous_and_next(some_iterable):
    prevs, items, nexts = tee(some_iterable, 3)
    prevs = chain([None], prevs)
    nexts = chain(islice(nexts, 1, None), [None])
    return izip(prevs, items, nexts) 
        
def pos_agreement(tags):
    errs = 0
    prev = ""
    verb_err = []
    verb_tags = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
    hasNoun  = False
    for curr in tags:
        if not hasNoun and curr in ['NN','NNS','NNP','NNPS','PRP$','PRP']:
            hasNoun = True
        if prev:
            if verb_err != []:
                if curr in verb_tags:
                    if curr in verb_err:
                        errs +=  10
                    verb_err = []
            elif curr == "NN" and prev != "DT":
                verb_err = ["VBP", "VBN"]
            elif curr == "NNS" and prev != "DT":
                verb_err = ["VBZ", "VBD"]
            elif curr == "NNP":
                verb_err = ["VBP"]
            elif curr == "NNPS":
                verb_err = ["VBZ"]
            elif prev == "DT" and (curr != "NN" and curr != "NNS"):
                errs += 1
            elif prev == "PRP$" and curr not in ["NN", "NNS", "JJ", "JJR", "JJS"]:
                errs += 1
        prev = curr
    if not hasNoun:
        errs += 1
    return errs
    
def pos_verbs(tags):
    errors = 0
    present = True
    if "VBN" in tags or "VBD" in tags:
        present = False

    verb_count = 0
    pres_tags = ['VB','VBZ','VBP','VBG']
    verb_tags = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
    for previous, current, nxt in  previous_and_next(tags):
        if not present and current in pres_tags:
            errors += 1

        if current in verb_tags:
            verb_count += 1
        elif current == "CC":
            if verb_count == 0:
                errors += 1
            verb_count = 0

    if verb_count == 0:
        errors += 1
    return errors

def pos_global_verbs(taglists):
    verbs = 0
    pastverbs = 0
    for taglist in taglists:
        for tag in taglist:
            if tag in ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]:
                verbs += 1
                if tag not in ['VB','VBZ','VBP','VBG']:
                    pastverbs += 1
    return abs((pastverbs/verbs)-1)

def agreement_score(text):
    t = TextBlob(text)
    agreementscore = 0.0
    for sent in t.sentences:
        tags = sent.tags
        agreementscore += pos_agreement(tags)               
    agreementscore /= len(t.words)
    return agreementscore

def verb_tense_score(text):
    t = TextBlob(text)
    verbscore = 0.0
    for sent in t.sentences:
        tags = sent.tags
        verbscore += pos_verbs(tags) 
    verbscore/= len(t.words)
    return verbscore

def misspelling_score(text):
    misspellings = 0
    t = TextBlob(text)
    for w in t.words:
        if correct(w) != w:
            misspellings += 1
    print "\t{0} miss in {1} words".format(misspellings, len(t.words))
    return misspellings/len(t.words)

def sentences_score(text):
    return len(TextBlob(text).sentences)