# -*- coding: utf-8 -*-
from nltk.tag.stanford import NERTagger
from app import app


def InitStanfordModule():
    # Example here: www.nltk.org/api/nltk.tag.html#module-nltk.tag.stanford

    return NERTagger(app.config['SNER_CLASSIFIERS'],
                     app.config['SNER_JARFILE'])


def FormatInput(file_text):
    punctuations = ['.', '!', '?']
    return file_text.replace(punctuations[0], ' ') \
                    .replace(punctuations[1], ' ') \
                    .replace(punctuations[2], ' ')


def IsolateLocations(stanford_list):
    locations = []
    LOCATION = u'LOCATION'
    for x in xrange(len(stanford_list)):
        if stanford_list[x][1] == LOCATION:
            if stanford_list[x + 1][1] == LOCATION:
                locations.append(stanford_list[x][0] + ' '
                                 + stanford_list[x + 1][0])
                x += 1
            else:
                locations.append(stanford_list[x][0])
    return locations


def FindLocations(file_text):

    # Remove punctuations for stanford

    file_text = FormatInput(file_text)

    stanford_ner = InitStanfordModule()

    stanford_tagged_entities = stanford_ner.tag(file_text.split())
    stanford_tagged_locations = \
        IsolateLocations(stanford_tagged_entities)

    return stanford_tagged_locations
