# tests/test_nlp.py
"""
run with: sudo fig run web nosetests geolocator
"""
from app import nlp
import unittest
import csv
import os
from nltk.tag.stanford import NERTagger
from nltk.tokenize import word_tokenize
from nose.tools import nottest

LOCATION = u'LOCATION'
PERSON = u'PERSON'
ORG = u'ORGANIZATION'
OTHER = u'O'


class StanfordNerTaggerTests(unittest.TestCase):
    """
    Tests for app.nlp.StanfordNerTagger
    """

    # ----------------------- Before/After ----------------------- #
    def setUp(self):
        """
        Executed at the start of every test
        Instantiates a new instance of nlp.StanfordNerTagger()
        """
        self.Tagger = nlp.StanfordNerTagger()
        return

    def tearDown(self):
        """
        Executed at the end of every test
        """
        self.Tagger = None
        return

    # ----------------------- Helpers ----------------------- #
    def makeTuples(self, list1, list2):
        """
        Will take elements from list1 and pair them with the elements of
        list2 at the same indices

        :param list list1: list of items to match to list2
        :param list list2: list of items to match to list1

        :returns: list of tuples in the following format:

            [(list1[0], list2[0]), (list1[1], list2[1]), ...,
            (list1[n]), list2[n]] where n == len(list1) or len(list2)

        :raises: TypeError if list1 and list2 are not of equal length
        """
        if len(list1) != len(list2):
            raise TypeError('list1 and list2 must be of equal length')
        return zip(list1, list2)

    def tokenize(self, words):
        """
        Splits words by whitespace and removes punctation
        """
        return word_tokenize(words)

    @nottest
    def symbolTest(self, symbols, expect_stop=True, symbol_tuple=None):
        """
        Tests the StanfordNerTagger's behavior when tagging symbols. The
        tagger either

            * tags all tokens given to it
            * tags all tokens unless a 'stop' symbol is reached

        :param list symbols: a list of symbols to test
        :param bool expect_stop: if True, it is expected that the tagger will
            not tag any tokens beyond the symbol; otherwise, tagger will tag
            all tokens and not stop at the symbol
        :param tuple symbol_tuple: for special cases when the tagger converts
            a given symbol to a different textual representation (for example,
            the tagger converts '(' to '-LRB'); this tuple should contain the
            expected symbol's translation and tag type: [(translation, type)]

        :returns: None
        """
        chocolate_chip = "chocolate chip "
        cookies = " cookies"
        for mark in symbols:
            # sentence to test
            sentence = chocolate_chip + mark + cookies
            tokens = self.tokenize(sentence)
            if symbol_tuple is None:
                if expect_stop:
                    # if nlp is  expected to stop at punctuation mark
                    expected = self.makeTuples(
                        self.tokenize(chocolate_chip + mark),
                        [OTHER, OTHER, OTHER])
                else:
                    # if nlp is expected to tag all tokens in sentence
                    expected = self.makeTuples(
                        tokens,
                        [OTHER, OTHER, OTHER, OTHER])
            else:
                # if arg-supplied expected tuple is given, then replace
                # tuple #2 with arg tuple expected
                expected = [(tokens[0], OTHER), (tokens[1], OTHER),
                            symbol_tuple]
                if not expect_stop:
                    expected.append((tokens[3], OTHER))
            actual = self.Tagger.Tag(tokens)
            print 'actual -> ' + str(actual)
            print 'expected -> ' + str(expected)
            assert actual == expected

    # ----------------------- Tests ----------------------- #
    def test__init__success(self):
        """
        Ensures that the nlp.StanfordNerTagger successfully initializes
        it's nltk.tag.stanford.NERTagger member
        """
        assert isinstance(self.Tagger.Tagger, NERTagger)

    def test_repre(self):
        """
        Tests the __repr__ function for correct output
        """
        placeh = self.Tagger.__repr__()
        assert placeh == ("<StanfordNerTagger(Tagger=%s)>" %
                          (self.Tagger.Tagger))

    def test_Tag_symbols_stop(self):
        """
        Verifies that the tagger stops at the following symbols:

            * '!'
            * '.'
            * '?'
        """
        symbols = [u'!', u'.', u'?']
        self.symbolTest(symbols, expect_stop=True)

    def test_Tag_symbols_continue(self):
        """
        Verifies that the tagger does not stop at the following symbols:

            * ','
            * '-'
            * '"'
            * "'"
            * ':'
            * ';'
        """
        symbols = [u',', u'-', u'"', u"'", u':', u';']
        self.symbolTest(symbols, expect_stop=False)

    def test_Tag_symbols_parens(self):
        """
        Verifies that the tagger does not stop at parenthesises.
        Note that the tagger converts parenthesis to the following:

            * '(' -> '-LRB-'
            * ')' -> '-RRB-'
        """
        self.symbolTest(u'(', expect_stop=False,
                        symbol_tuple=(u'-LRB-', OTHER))
        self.symbolTest(u')', expect_stop=False,
                        symbol_tuple=(u'-RRB-', OTHER))

    def test_Tag_1(self):
        """
        Tests the tagger's tagging ability

        Input: "Jack lives in Phoenix"

        Expected output:

            [('Jack', 'PERSON'), ('lives', 'OTHER'), ('in', 'OTHER'),
            ('Phoenix', 'LOCATION')]
        """
        tokens = self.tokenize("Jack lives in Phoenix")
        expected = self.makeTuples(tokens, [PERSON, OTHER, OTHER, LOCATION])
        actual = self.Tagger.Tag(tokens)
        assert actual == expected

    def test_Tag_2(self):
        """
        Tests the tagger's tagging ability

        Input: "Arizona is a desert"

        Expected output:

            [('Arizona', 'LOCATION'), ('is', 'OTHER'), ('a', 'OTHER'),
            ('desert', 'OTHER')]
        """
        tokens = "Arizona is a desert".split()
        expected = self.makeTuples(tokens, [LOCATION, OTHER, OTHER, OTHER])
        actual = self.Tagger.Tag(tokens)
        assert actual == expected

    def test_Tag_empty(self):
        """
        Tests the tagger's behavior when given an empty set of tokens

        Input: ""
        Expected output: []
        """
        tokens = "".split()
        expected = []
        actual = self.Tagger.Tag(tokens)
        assert actual == expected


class LocationTaggerTests(unittest.TestCase):
    """
    Unit tests for app.nlp.LocationTaggerTests
    """

    # ----------------------- Before/After ----------------------- #
    def setUp(self):
        """
        Executed at the start of every test
        Instantiates a new instance of nlp.StanfordNerTagger()
        """
        self.Tagger = nlp.LocationTagger()
        return

    def tearDown(self):
        """
        Executed at the end of every test
        """
        self.Tagger = None
        return

    # ----------------------- Helpers ----------------------- #

    # ----------------------- Tests ----------------------- #
    def test__init__success(self):
        """
        Ensures that the nlp.LocationTagger successfully initializes
        it's nlp.StanfordNerTagger member
        """
        assert isinstance(self.Tagger.Tagger, nlp.StanfordNerTagger)

    def test_RemovePunctuations(self):
        """
        Tests :func:'app.nlp.LocationTagger._RemovePunctuations'

        Input: "Hola! Estoy bien. Y tu?"
        Expected output: "Hola  Estoy bien  Y tu "
        """
        text = "Hola! Estoy bien. Y tu?"
        expected = "Hola  Estoy bien  Y tu "
        actual = self.Tagger._RemovePunctuations(text)
        assert actual == expected

    def test_Tokenize(self):
        """
        Tests :func:'app.nlp.LocationTagger._Tokenize'
        """
        pretext = "Hello, my name is Jang."
        tokens = self.Tagger._Tokenize(pretext)
        assert tokens == ['Hello', ',', 'my', 'name', 'is', 'Jang', '.']

    def test_PreProcessText(self):
        """
        Tests preprocesstext function as well as tokenize and removepunctuation
        """
        pretext = "Hello, my name is Jang."
        process = self.Tagger._PreProcessText(pretext)
        assert process == ['Hello', ',', 'my', 'name', 'is', 'Jang']

    def test_TagLocations(self):
        """
        Tests the TagLocations function which utilizes and also tests the
        preprocess, tag, IsolateLocations, and RemoveDuplicates functions as
        well
        """
        pretext = (
            "Hello, my name is Jang and I am from Phoenix, Arizona. "
            "My hometown is in Chandler, AZ "
            "but I like Phoenix, Arizona better.")
        tagged = self.Tagger.TagLocations(pretext)
        assert tagged == ['Phoenix', 'Arizona', 'Chandler', 'AZ']

    def test_Repr(self):
        """
        Tests the __repr__ function for correct output
        """
        placeh = self.Tagger.__repr__()
        assert placeh == "<LocationTagger(Tagger=%s)>" % (self.Tagger.Tagger)
