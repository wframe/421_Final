from __future__ import division
import file_io as fi
import pos
import grader as gr
from itertools import tee, islice, chain, izip
#http://stackoverflow.com/questions/1011938/python-previous-and-next-values-inside-a-loop
def previous_and_next(some_iterable):
    prevs, items, nexts = tee(some_iterable, 3)
    prevs = chain([None], prevs)
    nexts = chain(islice(nexts, 1, None), [None])
    return izip(prevs, items, nexts)
    
def test_tag_performance(directory):
    lofis = fi.recGetTextFiles(r'C:\Users\William\CS421Proj\421_Final\essays\original\low')
    mefis = fi.recGetTextFiles(r'C:\Users\William\CS421Proj\421_Final\essays\original\medium')
    hifis = fi.recGetTextFiles(r'C:\Users\William\CS421Proj\421_Final\essays\original\high')
    lo_agreementscore = 0.0
    lo_verbscore = 0.0
    for file in lofis:
        agreementscore = 0.0
        verbscore = 0.0
        ftext = open(file,'r')
        text = ftext.read()
        for sent in gr.get_sentences(text):
            tags = pos.get_sentence_tags(sent)
            agreementscore += pos_agreement(tags)/len(tags)
            verbscore += pos_verbs(tags)/len(tags)
        lo_agreementscore += agreementscore
        lo_verbscore += agreementscore
    print("low agreement score: " + str(lo_agreementscore))
    print("low verb score: " + str(lo_verbscore))
    med_agreementscore = 0.0
    med_verbscore = 0.0
    for file in mefis:
        agreementscore = 0.0
        verbscore = 0.0
        ftext = open(file,'r')
        text = ftext.read()
        for sent in gr.get_sentences(text):
            tags = pos.get_sentence_tags(sent)
            agreementscore += pos_agreement(tags)/len(tags)
            verbscore += pos_verbs(tags)/len(tags)
        med_agreementscore += agreementscore
        med_verbscore += agreementscore
    print("med agreement score: " + str(med_agreementscore))
    print("med verb score: " + str(med_verbscore))
    hi_agreementscore = 0.0
    hi_verbscore = 0.0
    for file in hifis:
        agreementscore = 0.0
        verbscore = 0.0
        ftext = open(file,'r')
        text = ftext.read()
        for sent in gr.get_sentences(text):
            tags = pos.get_sentence_tags(sent)
            agreementscore += pos_agreement(tags)/len(tags)
            verbscore += pos_verbs(tags)/len(tags)
        hi_agreementscore += agreementscore
        hi_verbscore += agreementscore
    print("hi agreement score: " + str(hi_agreementscore))
    print("hi verb score: " + str(hi_verbscore))     
        
def pos_agreement(tags):
    errors = 0

    for previous, current, nxt in  previous_and_next(tags):
        if current == "NN":
            if nxt == "VBP" or nxt == "VBN":
                errors += 1
        if current == "NNS":
            if nxt == "VBZ" or nxt == "VBD":
                errors += 1
    return errors
    
def pos_verbs(tags):
    errors = 0
    present = True
    if "VBN" in tags or "VBD" in tags:
        present = False
    presTags = ['VB','VBZ','VBP','VBG']
    for previous, current, nxt in  previous_and_next(tags):
        if not present and current in presTags:
            errors += 1
    return errors
        
        