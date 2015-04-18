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
    loscore = 0
    for file in lofis:
        filescore = 0.0
        ftext = open(file,'r')
        text = ftext.read()
        for sent in gr.get_sentences(text):
            tags = pos.get_sentence_tags(sent)
            filescore += pos_score(tags)/len(text)
        loscore += filescore
    print("low pos score: " + str(loscore))
    mescore = 0
    for file in mefis:
        filescore = 0.0
        text = ftext.read()
        for sent in gr.get_sentences(text):
            tags = pos.get_sentence_tags(sent)
            filescore += pos_score(tags)/len(text)
        mescore += filescore
    print("med pos score: " + str(mescore))
    hiscore = 0
    for file in hifis:
        filescore = 0.0
        text = ftext.read()
        for sent in gr.get_sentences(text):
            tags = pos.get_sentence_tags(sent)
            filescore += pos_score(tags)/len(text)
        hiscore += filescore
    print("hi pos score: " + str(hiscore))        
        
def pos_score(tags):
    errors = 0
    present = True
    if "VBN" in tags or "VBD" in tags:
        present = False
    presTags = ['VB','VBZ','VBP','VBG']
    for previous, current, nxt in  previous_and_next(tags):
        if not present and current in presTags:
            errors += 1
        if current == "NN":
            if nxt == "VBP" or nxt == "VBN":
                errors += 1
        if current == "NNS":
            if nxt == "VBZ" or nxt == "VBD":
                errors += 1
        if current == ",":
            if (previous == "NN" and nxt == "NNS") or (previous == "NNS" and nxt == "NN"):
                errors += 1
    return errors
        
        