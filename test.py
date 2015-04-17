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
    lofis = fi.recGetTextFiles(r'C:\Users\William\CS421Proj\421_Final\essays\original')
    mefis = fi.recGetTextFiles(r'C:\Users\William\CS421Proj\421_Final\essays\original\medium')
    hifis = fi.recGetTextFiles(r'C:\Users\William\CS421Proj\421_Final\essays\original\high')
    loscore = 0
    for file in lofis:
        filescore = 0
        text = open(file,'r')
        for sent in gr.get_sentences(text.read()):
            tags = pos.get_sentence_tags(sent)
            filescore += pos_score(tags)
        loscore += filescore
    print("low pos score: " + str(loscore))
    mescore = 0
    for file in mefis:
        filescore = 0
        text = open(file,'r')
        for sent in gr.get_sentences(text.read()):
            tags = pos.get_sentence_tags(sent)
            filescore += pos_score(tags)
        mescore += filescore
    print("med pos score: " + str(mescore))

    hiscore = 0
    for file in hifis:
        filescore = 0
        text = open(file,'r')
        for sent in gr.get_sentences(text.read()):
            tags = pos.get_sentence_tags(sent)
            filescore += pos_score(tags)
        hiscore += filescore
    print("hi pos score: " + str(hiscore))        
        
def pos_score(tags):
    errors = 0    
    for previous, current, nxt in     previous_and_next(tags):
        if current == "NN":
            if nxt == "VBP" or nxt == "NNS":
                errors += 1
        if current == "NNS":
            if nxt == "VBZ" or nxt == "NN":
                errors += 1
    return errors
        
        