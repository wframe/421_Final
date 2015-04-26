import pronouns as pro
#DEBUGGING STRUCTURE DELETE LATER
def coherence(t):
    pcons = collect_pronouns(t)
    pronoun_score = process_pronouns(pcons)
    topic_score = topicality(t)
    return pronoun_score, topic_score
def topicality(t):
    return 0
def collect_pronouns(t):
    pcons = []
    sent_index = 0
    for sent in t.sentences:
        for word in sent.tokens:
            if word in pro.t_pers:
                pcons.append((word, sent_index))
        sent_index += 1
    return pcons
def process_pronouns(pronoun_contexts):
    score = 0
    sing_score = 0
    plur_score = 0
    for pcon in pronoun_contexts:
        if isSingular(pcon[0]):
            sing_score += process_singular(pcon)
        else:
            plur_score += process_plural(pcon)
    return
def isSingular(p):
    return p not in pro.plur
def process_singular(pcon):
    return 0
def process_plural(pcon):
    return 0
def check_for_singular_antecedent(pronoun_context):
    pass