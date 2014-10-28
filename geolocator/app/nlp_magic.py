import nltk
from nltk.tag.stanford import NERTagger

# part-of-speech tagging
def nlp_geo_magic(file_text):

	text = nltk.word_tokenize(file_text)
	parts_of_speech = nltk.pos_tag(text)

	return str(parts_of_speech)

def stanford_nlp_location_magic(file_text):

	import os

	# --- command to get executing directory
	# return os.getcwd()

	# --- attempt to configure java with python
	os.environ["JAVAHOME"] = '/usr/lib/jvm/java-1.7.0-openjdk-amd64/bin' 
	# return str(os.environ)

	# --- attempt to configure java with nltk
	# nltk.internals.config_java('../usr/lib/jvm/default-java/jre/bin/java')
	# nltk.internals.config_java('/usr/bin/java')

	# --- example found here: www.nltk.org/api/nltk.tag.html#module-nltk.tag.stanford
	# --- does not currently work
	st = NERTagger('geolocator/app/static/stanford-ner-2014-08-27/classifiers/english.all.3class.distsim.crf.ser.gz', 'geolocator/app/static/stanford-ner-2014-08-27/stanford-ner.jar')
	stanford_magic = st.tag(file_text.split())
	return str(stanford_magic)
