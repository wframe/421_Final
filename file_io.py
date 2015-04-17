import os, fnmatch
def recGetTextFiles(directory):
	matches = []
	for root, dirnames, filenames in os.walk(directory):
	  for filename in fnmatch.filter(filenames, '*.txt'):
		matches.append(os.path.join(root, filename))
	return matches
 
 


