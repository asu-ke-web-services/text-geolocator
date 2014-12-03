import os
from nltk.tag.stanford import NERTagger


def InitStanfordModule():
	# --- configure java with python
	os.environ["JAVAHOME"] = '/usr/lib/jvm/java-1.7.0-openjdk-amd64/bin' 

	# --- example found here: www.nltk.org/api/nltk.tag.html#module-nltk.tag.stanford
	return NERTagger('geolocator/app/static/stanford-ner-2014-08-27/classifiers/english.all.3class.distsim.crf.ser.gz', 
			'geolocator/app/static/stanford-ner-2014-08-27/stanford-ner.jar')


def FormatInput(file_text):
	punctuations = ['.', '!', '?']
	return file_text.replace(punctuations[0], ' ').replace(punctuations[1], ' ').replace(punctuations[2], ' ')


def IsolateLocations(stanford_list):
	locations = []
	LOCATION = u'LOCATION'
	for x in xrange(len(stanford_list)):
		if stanford_list[x][1] == LOCATION:
			if stanford_list[x+1][1] == LOCATION:
				locations.append(stanford_list[x][0] + ' ' + stanford_list[x+1][0])
				x += 1
			else:
				locations.append(stanford_list[x][0])
	return locations


def FindLocations(file_text):

	# --- remove punctuations for stanford
	file_text = FormatInput(file_text)

	stanford_ner = InitStanfordModule()

	stanford_tagged_entities = stanford_ner.tag(file_text.split())
	stanford_tagged_locations = IsolateLocations(stanford_tagged_entities)

	return stanford_tagged_locations
