import pronouns as pro
from pattern.text.en import parse
import nltk

def coherence(t):
    sentence_data = map(collect_sentence_data, t.sentences)
    pcontext = collect_pronouns(t)
    pronoun_score = process_pronouns(pcontext, sentence_data)
    topic_score = topicality(t)
    return pronoun_score
def topicality(t):
    return 0
def collect_pronouns(t):
    pcons = []
    sent_index = 0
    for sent in t.sentences:
        word_index = 0
        for word in sent.tokens:
            if word in pro.t_pers:
                pcons.append((word, sent_index, word_index))
            word_index +=1
        sent_index += 1
    return pcons
def collect_sentence_data(sent):
    #######################################################################################################
    # was going to use this NER code to detect gendered referents but the false positive rate was insane! #
    # for instance, it inferred all instances of 'Cars' as well as'Great Britain' to be people!?!?!?!?!?! #
    #######################################################################################################
    #people = []
    #for chunk in nltk.ne_chunk(sent.tags,binary=False):                  
    #    if hasattr(chunk, '_label'):
    #        person = str()
    #        if chunk._label == 'PERSON':
    #            print("found person in '" + str(chunk))
    #            for word in chunk:
    #                person += ' ' + word[0].lower()

    p = parse(sent.string)
    inNP = False
    words = p.split()
    #list of noun phrases. each phrase is a tuple of a 0 or 1 to indicate if the current phrase is in a prepositional phrase and a noun list and each noun is a tuple of noun and 'sing' or 'plur' 
    nphrase_list = []
    noun_list = []
    nphrase = ()
    length =  len(words[0])
    i = 0
    for word in words[0]:
        if 'NP' in word[2]:                        
            if not inNP:
                #this indicates we're in the first word in a noun phrase
                inNP = True
                if 'PNP' in word[3]:
                    #this indicates we're in a prep phrase
                    nphrase += 1,
                else:
                    nphrase += 0,
            if 'NN' in word[1]:
                #current word is noun
                if 'S' in word[1]:
                    noun = (word[0], 'Plur', i)
                    noun_list.append(noun)
                else:
                    noun = (word[0], 'Sing', i)
                    noun_list.append(noun)
            elif 'PRP' in word[1]:
                #current word is pronoun
                if 'S' in word[1]:    
                    noun = (word[0], 'Plur' , i)
                    noun_list.append(noun)
                else:
                    noun = (word[0], 'Sing' , i)
                    noun_list.append(noun)
            if i == length - 1:
                nphrase += noun_list,
                nphrase_list.append(nphrase)
                inNP = False
                nphrase = ()
                noun_list = []
        elif inNP:
            nphrase += noun_list,
            nphrase_list.append(nphrase)
            inNP = False
            nphrase = ()
            noun_list = []
        i+=1                        
    return nphrase_list
def process_pronouns(pcons, sd):
    score = 0
    sing_score = 0
    plur_score = 0
    for pcon in pcons:
        if isSingular(pcon[0]):
            pass
            #sing_score += process_singular(pcon)
        else:
            plur_score += process_plural(pcon, sd)
    return plur_score
def isSingular(p):
    return p not in pro.plur
def process_singular(pcon):
    #check_for_singular_antecedent
    pass
def process_plural(pcon, sd):
    curr = pcon[1]
    chain = [x for x in sd if sd.index(x) >= curr - 2 and sd.index(x) <= curr]   
    isCurr = True
    mostRecent = True
    score = 0
    distance_from_curr = 0
    for sent in reversed(chain):
        if isCurr:
            isCurr = False   
            for phrase in reversed(sent):
                for noun in reversed(phrase[1]):
                    if pcon[2] <= noun[2]:
                        pass
                    else:
                        if mostRecent:
                            mostRecent = False
                            if noun[1] == 'Sing':
                                score += -2.0
                            elif phrase[0] == 0:                                                                 
                                score += 2.0                                 
                            else:
                                score += 1.5
                        else:
                            if noun[1] == 'Sing':
                                score += -1.0
                            elif phrase[0] == 0:                                                       
                                score += 1.0                                 
                            else:
                                score += .75         
        else:
            for phrase in reversed(sent):
                for noun in reversed(phrase[1]):
                    if mostRecent:
                        if noun[1] == 'Sing':
                            score += -2.0/distance_from_curr
                        elif phrase[0] == 0:                                                                 
                            score += 2.0/distance_from_curr                                 
                        else:
                            score += 1.5/distance_from_curr
                        mostRecent = False
                    else:
                        if noun[1] == 'Sing':
                            score += -1.0/distance_from_curr
                        elif phrase[0] == 0:                                                      
                            score += 1.0/distance_from_curr                                 
                        else:
                            score += .75/distance_from_curr            
        distance_from_curr += 1                
    return score
  
    