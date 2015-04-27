from pattern.web    import Twitter
from pattern.text.en     import tag
from pattern.vector import KNN, count, NaiveBayes, SVM
import os, random
import file_io as fio
corp_dir = 'essays/original'
twitter, knn, nbayes, svm = Twitter(), KNN(), NaiveBayes(), SVM()
from nltk.corpus import stopwords
import lsa
cachedStopWords = stopwords.words("english")
testSet = []

def naive():
    trainingSet = []
    l = lsa.getMod() 
    dirs = [x[0] for x in os.walk(os.path.abspath(corp_dir))]
    for dir in dirs:
        label = 0
        if 'low' in dir:
            label = -1
        elif 'high' in dir:
            label = 1
        tfiles = []
        tfiles = fio.getTopLevelFiles(dir, extension = 'txt')
        train_smpl = []
        if len(tfiles) >  0:
            train_smpl = [ tfiles[i] for i in random.sample(xrange(len(tfiles)), 13)]
        for file in tfiles:
            with open(file, 'r') as f:
                text = ' '.join([word for word in list(f.read().split()) if word not in cachedStopWords]).lstrip().lower()
                if file not in train_smpl:
                    testSet.append((text, label))
                else:
                    trainingSet.append((text, label))                                                                          
        #test_smpl = [ tfiles[i] for tfiles[i] not in train_smpl]
    for sample in trainingSet:
        s = sample[0]
        p = str(sample[1])
        svm.train(s, p)
        #nbayes.train(v, p)
        #knn.train(v, type=p)
    #for tweet in twitter.search('#win OR #fail', start=i, count=100):
    #    s = tweet.text.lower()
    #    p = '#win' in s and 'WIN' or 'FAIL'
    #    v = tag(s)
    #    v = [word for word, pos in v if pos == 'JJ'] # JJ = adjective
    #    v = count(v) 
    #    if v:
    #        knn.train(v, type=p)
if __name__ == '__main__':
    naive()
    for doc in testSet:
        #if nbayes.classify(doc[0]) != str(doc[1]):
        if svm.classify(doc[0]) != str(doc[1]):
            print('document was class {} but was classified as {}'.format(str(doc[1]) ,svm.classify(doc[0])))              
    


    