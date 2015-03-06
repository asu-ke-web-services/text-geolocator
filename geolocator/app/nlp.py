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
            app.config['SNER_JARFILE'])
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
            text = text.replace(p, ' ')
        return text

    def _Tokenize(self, text):
        """
        Tokenizes 'text' (aka splits text into individual words) by
        calling .split()

        Example:

            Text: "Hello, my name is Jack!"
            Result: ['Hello,', 'my', 'name', 'is', 'Jack!']

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

        :param str text: text to process

        :returns: str -- processed text
        """
        text = self._RemovePunctuations(text)
        text = self._Tokenize(text)
        return text

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
                locations.append(name)
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
        locations = self._IsolateLocations(tagged)
        noduplicates = self._RemoveDuplicates(locations)
        return noduplicates

    def __repr__(self):
        return "<LocationTagger(Tagger=%s)>" % (self.Tagger)
