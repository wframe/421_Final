from __future__ import division
import file_io as fi
import pos
import grader as gr
from itertools import tee, islice, chain, izip
from os import path
#http://stackoverflow.com/questions/1011938/python-previous-and-next-values-inside-a-loop
def previous_and_next(some_iterable):
    prevs, items, nexts = tee(some_iterable, 3)
    prevs = chain([None], prevs)
    nexts = chain(islice(nexts, 1, None), [None])
    return izip(prevs, items, nexts)
    
def test_tag_performance():
    fis_arr = [fi.recGetTextFiles(path.abspath(r'essays\original\low')),
                fi.recGetTextFiles(path.abspath(r'essays\original\medium')),
                fi.recGetTextFiles(path.abspath(r'essays\original\high'))]
    agreementscores = []
    verbscores = []
    for fis in fis_arr:
        ovr_agreementscore = 0.0
        ovr_verbscore = 0.0
        for file in fis:
            words = 0
            agreementscore = 0.0
            verbscore = 0.0
            ftext = open(file,'r')
            text = ftext.read()
            for sent in gr.get_sentences(text):
                tags = pos.get_sentence_tags(sent)
                agreementscore += pos_agreement(tags)
                verbscore += pos_verbs(tags)
                words+=len(tags)
            ovr_agreementscore += agreementscore/len(text)
            ovr_verbscore += verbscore/len(text)
        agreementscores.append(ovr_agreementscore)
        verbscores.append(ovr_verbscore)
    print("low agreement score: " + str(agreementscores[0]))
    print("low verb score: " + str(verbscores[0]))
    print("med agreement score: " + str(agreementscores[1]))
    print("med verb score: " + str(verbscores[1]))
    print("high agreement score: " + str(agreementscores[2]))
    print("high verb score: " + str(verbscores[2]))    
        
def pos_agreement(tags):
    errs = 0
    verb_err = []
    verb_tags = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
    prev = ""
    for curr in tags:
        if prev:
            if verb_err != []:
                if curr in verb_tags:
                    if curr in verb_err:
                        errs +=  1
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
            elif prev == "PRP$" and (curr != "NN" and curr != "NNS"):
                errs += 1
        prev = curr
    return errs
    
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
        
        