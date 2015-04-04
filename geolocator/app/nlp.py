# -*- coding: utf-8 -*-
"""
Contains the following classes:

    * StanfordNerTagger
    * LocationTagger

This file manages all NLP operations within this application
"""
from nltk.tag.stanford import NERTagger
from nltk.tokenize import word_tokenize
from app import app


NLP_PUNCTUATION_TOKEN = 'NLP_PUNCTUATION_TOKEN'
"""Marks the place of a period in uploaded file's text"""


class StanfordNerTagger():
    """
    Wrapper class for the nltk.tag.stanford.NERTagger module. Provides
    streamlined instantiation and helper methods to simplify the process
    of using the tagger.
    """
    def __init__(self):
        # Example here: www.nltk.org/api/nltk.tag.html#module-nltk.tag.stanford
        self.Tagger = NERTagger(
            app.config['SNER_CLASSIFIERS'],
            app.config['SNER_JARFILE'],
            encoding='utf-8')
        return

    def Tag(self, text):
        """
        Given text, the tagger will identify all entities mentioned in
        the text and associate them with an entity type.

        Example:

            Input: "I am Jack and I live in Phoenix, Arizona."

            Tag Result:

                "[(I)]... TODO"


        :param str text: text to tokenize and tag

        :returns: list of tuples -- see above example
        """
        entities = self.Tagger.tag(text)
        return entities

    def __repr__(self):
        return "<StanfordNerTagger(Tagger=%s)>" % (self.Tagger)


class MultiWordLocationStitcher(object):

    def _IsLocation(self, loc_tuple):
        """
        Determines if loc_tuple has been tagged as a LOCATION.

        :param tuple loc_tuple: NER Tagger tuple

        :returns: True if loc_tuple[1] == 'LOCATION'
        """
        if isinstance(loc_tuple, tuple) and len(loc_tuple) > 1:
            return loc_tuple[1] == 'LOCATION'
        else:
            return False

    def _GetListIndex(self, element, list_to_search):
        """
        Returns the index of element in list_to_search

        :param ? element: element to search list for
        :param list list_to_search: list to search in

        :returns: int (0 or greater) if found; otherwise -1
        """
        index = -1
        if isinstance(list_to_search, list):
            try:
                index = list_to_search.index(element)
            except ValueError:
                pass
        return index

    def _GetNextLocationIndex(self, ner_tuples, start):
        """
        Returns index of next 'LOCATION' from ner_tuples

        :param list ner_tuples: tuples to search for location in
        :param int start: starting index to search from

        :returns: int -- index of next location
        """
        if isinstance(start, int):
            i = start + 1
            if isinstance(ner_tuples, list):
                while i < len(ner_tuples):
                    # print '\t\ti: %s, loc: %s' % (str(i), str(ner_tuples[i]))
                    if self._IsLocation(ner_tuples[i]):
                        # print str(ner_tuples[i]) + ' is a location!'
                        return i
                    i += 1
        # print 'returning -1'
        return -1

    def StitchMultiWordLocations(self, originals, tagged):
        """
        The Stanford NER Tagger tags multi word locations like this:

            "Sun City" = [('Sun', 'LOCATION'), ('City', 'LOCATION')]

        This function will reunite the separated locations so they look like:

            "Sun City" = [('Sun City', 'Location')]

        This is done to improve accuracy when retrieving coordinates

        :param list originals: tokenized text from uploaded file
        :param list tagged: results of Stanford NER Tagger tagging

        :returns: list -- tagged locations with separated locations reunited
        """
        locations = []
        # reunited = []
        # remove = []
        # iterate over all tagged locations
        for i, t in enumerate(tagged):
            loc_index = i
            delete_orgs = []
            if self._IsLocation(t):
                # find index of this location in originals
                org_index = self._GetListIndex(t[0], originals)
                if org_index > -1:
                    loc_name = t[0]
                    delete_orgs.append(org_index)
                    loop = True
                    # print '******'
                    # print originals
                    # print 't: %s' % str(t)
                    # print '\tadded delete: %s' % str(originals[org_index])
                    # print 'len(originals) = %s' % str(len(originals))
                    # print 'org_index = %s' % str(org_index)
                    while loop and (org_index+1) < len(originals):
                        next_org = originals[org_index+1]
                        next_loc_index = self._GetNextLocationIndex(
                            tagged, loc_index)
                        if next_loc_index == -1:
                            break
                        next_loc = tagged[next_loc_index][0]
                        # print '\t----------'
                        # print '\tnext_org: %s' % next_org
                        # print '\tnext_loc: %s' % next_loc
                        if next_org == next_loc:
                            # found a multi-word location
                            loc_name += ' %s' % str(next_org)
                            # del originals[index+1]
                            org_index += 1
                            loc_index += 1
                            delete_orgs.append(org_index)
                            # if org_index < len(originals):
                            #     print ('\tadded delete: %s' %
                            #            str(originals[org_index]))
                        else:
                            # multi-word location has ended, move to next tuple
                            loop = False
                    # clear used locations from originals
                    for d in reversed(delete_orgs):
                        # print '\tdeleting: %s' % originals[d]
                        del originals[d]
                    # print '\tadding: %s' % loc_name
                    locations.append((loc_name, 'LOCATION'))
        return locations

    def __repr__(self):
        return "<MultiWordLocationStitcher()>"


class LocationTagger():
    """
    Uses the StanfordNerTagger to find all locations within a given str.
    """
    def __init__(self):
        self.Tagger = StanfordNerTagger()

    def _RemovePunctuations(self, text):
        """
        Replaces all punctuation in 'text' with whitespace so that
        StanfordNerTagger will process the entire document

        Punctuation Marks Removed:

            * '.'
            * '!'
            * '?'

        :param str text: text to process

        :returns: the same text without the above punctuation marks
        """
        punctuations = ['.', '!', '?']
        for p in punctuations:
            text = text.replace(p, ' %s' % NLP_PUNCTUATION_TOKEN)
        return text

    def _Tokenize(self, text):
        """
        Tokenizes 'text' (aka splits text into individual words) by
        calling .split()

        Example:

            Text: "Hello, my name is Jack!"
            Result: ['Hello', ',', 'my', 'name', 'is', 'Jack', '!']
        Punctuation is separate from everything else

        :param str text: text to split

        :returns: list -- strings that were separated by whitespace
        """
        return word_tokenize(text)

    def _PreProcessText(self, text):
        """
        Formats 'text' so that it is in the optimal format for the
        Stanford NER Tagger. Operations include:

            * Removing punctuation
            * Tokenizing text (aka splitting into individual words)
            * Does not remove commas inside text

        :param str text: text to process

        :returns: str -- processed text
        """
        text = self._RemovePunctuations(text)
        text = self._Tokenize(text)
        return text

    def _ReuniteSeparatedLocations(self, originals, tagged):
        """
        The Stanford NER Tagger tags multi word locations like this:

            "Sun City" = [('Sun', 'LOCATION'), ('City', 'LOCATION')]

        This function will reunite the separated locations so they look like:

            "Sun City" = [('Sun City', 'Location')]

        This is done to improve accuracy when retrieving coordinates

        :param list originals: tokenized text from uploaded file
        :param list tagged: results of Stanford NER Tagger tagging

        :returns: list -- tagged locations with separated locations reunited
        """
        stitcher = MultiWordLocationStitcher()
        locations = stitcher.StitchMultiWordLocations(originals, tagged)
        return locations

    def _IsolateLocations(self, stanford_ner_tagger_output):
        """
        Given list of Stanford NER Tagger results in the format of
        ('name', 'type'), filter list and retrieve only those listed
        as 'type'='LOCATION'

        :param list stanford_ner_tagger_output: list of tuples in the
            format of ('name', 'type')

        :returns: list -- names of tuples with 'type'='LOCATION'
        """
        LOCATION = u'LOCATION'
        locations = []
        for name, typ in stanford_ner_tagger_output:
            if typ == LOCATION:
                locations.append(name.encode('ascii', 'ignore'))
        return locations

    def _RemoveDuplicates(self, strings):
        """
        Removes all duplicates from the given list

        :param list l: a list of strings
        """
        # Unicode to string, assuming there will be no characters that lie
        # outside of ascii range
        stringlist = [str(x) for x in strings]
        noduplicate_array = []
        list(set(stringlist))
        [noduplicate_array.append(item) for item in stringlist if item
         not in noduplicate_array]
        return noduplicate_array

    def TagLocations(self, text):
        """
        Given the text of a document, find and return all locations

        :param str text: text of a document

        :returns: list -- all locations in text
        """
        text = self._PreProcessText(text)
        tagged = self.Tagger.Tag(text)
        tagged = self._ReuniteSeparatedLocations(text, tagged)
        locations = self._IsolateLocations(tagged)
        noduplicates = self._RemoveDuplicates(locations)
        return noduplicates

    def __repr__(self):
        return "<LocationTagger(Tagger=%s)>" % (self.Tagger)
