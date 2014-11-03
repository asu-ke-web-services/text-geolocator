import nltk
from nltk.tag.stanford import NERTagger

# part-of-speech tagging
def nlp_geo_magic(file_text):

	text = nltk.word_tokenize(file_text)
	parts_of_speech = nltk.pos_tag(text)

	return str(parts_of_speech)

def stanford_nlp_location_magic(file_text):

	import os

	locations = []
	LOCATION = u'LOCATION'

	# --- command to get executing directory
	# return os.getcwd()

	# --- attempt to configure java with python
	os.environ["JAVAHOME"] = '/usr/lib/jvm/java-1.7.0-openjdk-amd64/bin' 

	# --- example found here: www.nltk.org/api/nltk.tag.html#module-nltk.tag.stanford
	st = NERTagger('geolocator/app/static/stanford-ner-2014-08-27/classifiers/english.all.3class.distsim.crf.ser.gz', 'geolocator/app/static/stanford-ner-2014-08-27/stanford-ner.jar')
	stanford_magic = []
	# split = file_text.split()
	punctuations = ['.', '!', '?']
	file_text = file_text.replace(punctuations[0], ' ')
	file_text = file_text.replace(punctuations[1], ' ')
	file_text = file_text.replace(punctuations[2], ' ')
	stanford_magic = st.tag(file_text.split())
	for x in xrange(len(stanford_magic)):
		if stanford_magic[x][1] == LOCATION:
			if stanford_magic[x+1][1] == LOCATION:
				locations.append(stanford_magic[x][0] + ' ' + stanford_magic[x+1][0])
				x += 1
			else:
				locations.append(stanford_magic[x][0])
	return str(locations)
