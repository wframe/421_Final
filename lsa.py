from pattern.vector import Document, Model, HIERARCHICAL, Cluster
from pageparser   import PageParser
from textblob 		  import TextBlob
from numpy import argmax
import entity_recognition as er
import file_io as fio
import string
import io
from os import walk, path
essay_path = 'essays/original/high'
essay_path = path.abspath(essay_path)
def write_cluster(cluster, file, prepend):
	file.write(unicode(prepend + "CLUSTER\n"))
	for d in cluster:
		if isinstance(d, Cluster):
			write_cluster(d, file, prepend + "\t")
		else:
			name = d.name.split('\\')[-1]
			name = filter(lambda x: x in string.printable, name)
			file.write(unicode(prepend + "\t" + name))
			file.write(unicode("\n"))

if __name__ == '__main__':
	files = fio.getTopLevelFiles(essay_path, extension = 'txt')
	docs = []
	for f in files:
		with io.open(f, 'r', encoding='utf-8') as w:
			text = TextBlob(PageParser.parse(w.read()))
			ent_text = ' '.join(er.recognize_entities(text.sentences))
			#ent_text = PageParser.parse(w.read())
			docs.append(Document(ent_text, name=f, top=40))


	m = Model(docs)
	
	# Clustering could be a useful technique, commenting out for now
	#with io.open(r'lsa.txt', 'w+', encoding='utf-8') as w:
	#	write_cluster(m.cluster(method=HIERARCHICAL, k=4), w, "")
	
	lsa = m.reduce(30)

	with io.open(r'lsa.txt', 'w+', encoding='utf-8') as w:
		for i,concept in enumerate(m.lsa.concepts):
			#print("Concept {0}:".format(i)),
			w.write(unicode("Concept {0}:".format(i)))
			count = 0

			# Show top only first 5 features we come across
			for feature, weight in m.lsa.concepts[i].items(): 
				if abs(weight) > 0.2:
					#print(feature),
					w.write(feature + " ")
					count += 1

				if count > 5:
					break
			w.write(unicode('\n'))
			#print 

			cat_docs = []
			for d in m.documents:
				cat = (0,0, {})
				#print d.name.split('\\')[-1]
				for idx,weight in m.lsa.vectors[d.id].items():
					#print "\tCat {0}: {1}".format(idx, weight)
					if abs(weight) > abs(cat[1]) or cat[1] == 0:
						cat = (idx,weight,d)

				if cat[0] == i:
					cat_docs.append(cat)
					#print "\t{0}".format(d.name.split('\\')[-1])

			cat_docs.sort(key=lambda tup: abs(tup[1]), reverse=True)
			for cat,weight,d in cat_docs:
				f = d.name.split('\\')[-1]
				w.write(unicode("\t{0} - {1}\n").format(filter(lambda x: x in string.printable, f), weight))
					


