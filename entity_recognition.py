#import local as loc
import nltk, re
from pattern.text.en import tokenize as tok
from pattern.text.en import tag
from pattern.text.en import wordnet as wnet
from pattern.text.en import parsetree as pt
from pattern.vector import stem, PORTER, LEMMA
from handlers import TextHandler
domains = ['cnn','reuters','nytimes',' wired',' vice','facebook','twitter',' news','video', 'toggle']
def extend_entities(entity, intersector=None, intersect=False):
    syns = []
    syns.append(entity) 
    keys = set(intersector.keys())
    for word in entity:
        if word in keys:
            for syn in wnet.synsets(word):
                syns.append(syn[0])
    return syns 
def recognize_entities(sentences, intersector=None, intersect=False):
    with open('intersection_entity14.txt', 'a+') as inf:
        entities = []
        entities_nltk = []
        for sent in sentences:
        #these two methods produce different results...also the first is prolly quicker...we could also mess around with letting expected entity type be a feature:
            for chunk in nltk.ne_chunk(sent.tags,binary=True):
                if hasattr(chunk, '_label'):
                    entity = str()
                    if chunk._label == 'NE':
                        for word in chunk:
                            entity += ' ' + word[0].lower()
                        include = True
                        for dom in domains:
                            if dom in entity:
                                include = False
                        if include:     
                            #ptree = pt(sent, relations=True, lemmata=True)
                            #sent = stem(sent, stemmer=LEMMA)                                   
                            #entities+=extend_entities(entity.lstrip(), intersect=intersect, intersector=intersector)
                            entities.append(entity.lstrip())
            #for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent)),binary=True):
            #    if hasattr(chunk, '_label'):
            #        entity = str()
            #        if chunk._label == 'NE':
            #            for word in chunk:
            #                entity += ' ' + word[0]
            #                entities_nltk.append(entity.lstrip().lower())
        #f.write('\nUSING PATTERN:\n' + str(entities))
        #f.write('\nUSING NLTK:\n' + str(entities_nltk))

        #ret = intersect(entities,entities_nltk)
        #a,b,c = (len(entities),len(entities_nltk),len(ret))
        #inf.write('\nSET LENGTHS:\n' + str((a,b,c)))
        #inf.write('\nENTITIES:\n' + str(entities))
        #return ret
        return entities

def intersect(a, b):
     return list(set(a) & set(b))
                       
if __name__ == "__main__":
    text="Kylie Jenner Baggins has encouraged young women not to be afraid to experiment with their looks. The 17-year-old reality star has become famous for her extremely full pout, which she achieves with lip liner and trickery."
    #text=r'Summer School of the Arts filling fast\n Wanganui people have the chance to learn the intricacies of decorative sugar art from one of the country\xe2\x80\x99s top pastry chefs at Whanganui UCOL\xe2\x80\x99s Summer School of the Arts in January.\nTalented Chef de Partie, Adele Hingston will take time away from her duties at Christchurch\xe2\x80\x99s Crowne Plaza to demonstrate the tricks and techniques of cake decorating including creating flower sprays and an introduction to royal icing.\nDemand has been high for places in the Summer School of the Arts but there are still opportunities for budding artists to hone their skills in subjects as diverse as jewellery making, culinary sugar art and creative writing. \n\xe2\x80\x9cThe painting, pattern drafting and hot glass classes filled almost immediately,\xe2\x80\x9d says Summer School Coordinator Katrina Langdon. \xe2\x80\x9cHowever there are still places available in several of the programmes.\xe2\x80\x9d\nEighteen distinguished artists will each share their particular creative talents during week long programmes in painting, writing, drawing, jewellery, fibre arts, printmaking, photography, sculpture, glass, fashion and culinary arts.\n\xe2\x80\x9cI suggest anyone who is considering joining us for the Summer School should register now. January will be here before we know it,\xe2\x80\x9d says Katrina.\nWhanganui UCOL Summer School of the Arts runs from 10-16 January 2010. Enrolments are now open and brochures are available online at www.ucol.ac.nz or contact Katrina Langdon, K.Langdon@ucol.ac.nz, Ph 06 965 3801 ex 62000.\nThe Whanganui Summer School of the Arts programme includes:\nPainting: R ob McLeod - Marks, multiples and texture, Michael Shepherd - Oil painting, Julie Grieg \xe2\x80\x93 Soft pastel painting.Drawing: Terrie Reddish \xe2\x80\x93 Botanical Drawing.Printmaking: Ron Pokrasso \xe2\x80\x93 Beyond Monotype, Stuart Duffin \xe2\x80\x93 Mezzotint printmaking.Photography: Fleur Wickes \xe2\x80\x93 The New Portrait, Rita Dibert \xe2\x80\x93 Pinholes, Holga\xe2\x80\x99s & Cyanotypes.Sculpture: Brent Sumner \xe2\x80\x93 Darjit Sculpture, Michel Tuffery \xe2\x80\x93 Sculptural Effigy.Glass: Jeff Burnette \xe2\x80\x93 Hot glass techniques, Brock Craig \xe2\x80\x93 Kiln-forming techniques.Jewellery: Craig Winton \xe2\x80\x93 Jewellery Making-Tricks of the trade.Fashion: John Kite \xe2\x80\x93 Pattern drafting for made to measure.Fibre and Fabric: Fiona Wright \xe2\x80\x93 Felting - Text and texture, Deb Price \xe2\x80\x93 Baskets and Beyond.Culinary Arts: Adele Hingston \xe2\x80\x93 Sugar art.Literature: Frankie McMillan \xe2\x80\x93 Creative writing.\nENDS \r \r '
    recognize_entities(text)

