# tests/test_nlp.py
"""
run with: sudo fig run web nosetests geolocator
"""
from app import nlp
import unittest
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
            raise TypeError('list1 (%s) and list2 (%s) must be of equal'
                            'length' % (str(len(list1)), str(len(list2))))
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
            print tokens
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

    def test_Tag_3(self):
        """
        Tests the tagger's tagging ability.

        Input: "Sun City and Paradise Valley are both in Arizona"

        Expected output:

            [('Sun', 'LOCATION'), ('City', 'OTHER'), ('Grand', 'OTHER'),
            ('Canyon', 'OTHER'), ('Arizona', 'LOCATION'), ('Hong', 'LOCATION'),
            ('Kong', 'LOCATION'), ('China', 'LOCATION'),
            ('United', 'LOCATION'), ('States', 'LOCATION')]

        Note that it does not automatically group multi-word entities as a
        single entity. It separates them but still correctly labels them.
        """
        tokens = ("Sun City and Paradise Valley are both in Arizona").split()
        expected = self.makeTuples(
            tokens,
            [
                LOCATION,   # Sun
                LOCATION,   # City
                OTHER,      # and
                LOCATION,   # Paradise
                LOCATION,   # Valley
                OTHER,      # are
                OTHER,      # both
                OTHER,      # in
                LOCATION    # Arizona
            ]
        )
        actual = self.Tagger.Tag(tokens)
        print expected
        print actual
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


class MultiWordLocationStitcherTests(unittest.TestCase):
    """
    Unit tests for app.nlp.MultiWordLocationStitcher

    Note that this class has no tests for StitchMultiWordLocations.
    That function is tested in LocationTaggerTests for
    LocationTagger._ReuniteSeparatedLocations
    """

    # ----------------------- Before/After ----------------------- #
    def setUp(self):
        """
        Executed at the start of every test
        Instantiates a new instance of nlp.MultiWordLocationStitcher()
        """
        self.Stitcher = nlp.MultiWordLocationStitcher()
        return

    def tearDown(self):
        """
        Executed at the end of every test
        """
        self.Stitcher = None
        return

    # ----------------------- Helpers ----------------------- #

    # ----------------------- Tests ----------------------- #
    def test__IsLocation__pass(self):
        """
        Tests _IsLocation function with a 'LOCATION'
        """
        expected = True
        actual = self.Stitcher._IsLocation(('Beijing', 'LOCATION'))
        assert expected == actual

    def test__IsLocation__None(self):
        """
        Tests _IsLocation function with a param of None
        """
        expected = False
        actual = self.Stitcher._IsLocation(None)
        assert expected == actual

    def test__IsLocation__not_a_tuple(self):
        """
        Tests _IsLocation function with a  param that is not a tuple
        """
        expected = False
        actual = self.Stitcher._IsLocation('not a tuple')
        assert expected == actual

    def test__IsLocation__length_less_than_2(self):
        """
        Tests _IsLocation function with a tuple of length 1
        """
        expected = False
        actual = self.Stitcher._IsLocation(tuple('1'))
        assert expected == actual

    def test__GetListIndex__pass(self):
        """
        Tests _GetListIndex with a list containing the targeted element

        Returns the index of element in list_to_search

        :param ? element: element to search list for
        :param list list_to_search: list to search in

        :returns: int (0 or greater) if found; otherwise -1
        """
        element = 'apple'
        list_to_search = ['banana', element, 'orange']
        expected = 1
        actual = self.Stitcher._GetListIndex(element, list_to_search)
        assert expected == actual

    def test__GetListIndex__None_param1(self):
        """
        Tests _GetListIndex with a first param of None
        """
        element = 'apple'
        list_to_search = None
        expected = -1
        actual = self.Stitcher._GetListIndex(element, list_to_search)
        assert expected == actual

    def test__GetListIndex__None_param2(self):
        """
        Tests _GetListIndex with a second param of None
        """
        element = None
        list_to_search = ['banana', 'frog', 'orange']
        expected = -1
        actual = self.Stitcher._GetListIndex(element, list_to_search)
        assert expected == actual

    def test__GetListIndex__not_found(self):
        """
        Tests _GetListIndex with a list not containing the targeted element
        """
        element = 'apple'
        list_to_search = ['banana', 'frog', 'orange']
        expected = -1
        actual = self.Stitcher._GetListIndex(element, list_to_search)
        assert expected == actual

    def test__GetListIndex__not_a_list(self):
        """
        Tests _GetListIndex with a list_to_search that is not a list
        """
        element = 'apple'
        # not a list! it is a tuple
        list_to_search = ('banana', element, 'orange')
        expected = -1
        actual = self.Stitcher._GetListIndex(element, list_to_search)
        assert expected == actual

    def test__GetNextLocationIndex__pass1(self):
        """
        Tests _GetNextLocationIndex where there is another location after start
        """
        tuples = [('Russia', LOCATION), ('ASU', ORG), ('Moscow', LOCATION)]
        start = 0
        expected = 2
        actual = self.Stitcher._GetNextLocationIndex(tuples, start)
        assert expected == actual

    def test__GetNextLocationIndex__None_param1(self):
        """
        Tests _GetNextLocationIndex where 'ner_tuples' is None
        """
        tuples = None
        start = 5
        expected = -1
        actual = self.Stitcher._GetNextLocationIndex(tuples, start)
        assert expected == actual

    def test__GetNextLocationIndex__None_param2(self):
        """
        Tests _GetNextLocationIndex where 'start' is None
        """
        tuples = [('England', LOCATION), ('Berlin', LOCATION),
                  ('Congress', ORG), ('in', OTHER)]
        start = None
        expected = -1
        actual = self.Stitcher._GetNextLocationIndex(tuples, start)
        assert expected == actual

    def test__GetNextLocationIndex__no_next_location(self):
        """
        Tests _GetNextLocationIndex where there is not another location after
        start
        """
        tuples = [('England', LOCATION), ('Berlin', LOCATION),
                  ('Congress', ORG), ('in', OTHER)]
        start = 1
        expected = -1
        actual = self.Stitcher._GetNextLocationIndex(tuples, start)
        print actual
        print tuples[actual]
        assert expected == actual

    def test__GetNextLocationIndex__start_too_large(self):
        """
        Tests _GetNextLocationIndex where start is greater than len(ner_tuples)
        """
        tuples = [('England', LOCATION), ('Berlin', LOCATION),
                  ('Congress', ORG), ('in', OTHER)]
        start = 4
        expected = -1
        actual = self.Stitcher._GetNextLocationIndex(tuples, start)
        assert expected == actual

    def test__repr__(self):
        """
        Tests __repr__ to make sure that it returns a str without error
        """
        s = self.Stitcher.__repr__()
        assert isinstance(s, str)


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
        expected = ("Hola %s Estoy bien %s Y tu %s" %
                    (nlp.NLP_PUNCTUATION_TOKEN, nlp.NLP_PUNCTUATION_TOKEN,
                        nlp.NLP_PUNCTUATION_TOKEN))
        actual = self.Tagger._RemovePunctuations(text)
        print expected
        print actual
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
        assert process == ['Hello', ',', 'my', 'name', 'is', 'Jang',
                           nlp.NLP_PUNCTUATION_TOKEN]

    def test_ReuniteSeparatedLocations1(self):
        """
        Tests _ReuniteSeparatedLocations
        """
        originals = ['Fountain', 'Hills', 'has', 'a', 'fountain']
        tagged = [
            (originals[0], LOCATION),
            (originals[1], LOCATION),
            (originals[2], OTHER),
            (originals[3], OTHER),
            (originals[4], OTHER)]
        expected = [('Fountain Hills', LOCATION)]
        actual = self.Tagger._ReuniteSeparatedLocations(originals, tagged)
        print 'expected -> %s' % str(expected)
        print 'actual -> %s' % str(actual)
        assert expected == actual

    def test_ReuniteSeparatedLocations2(self):
        """
        Tests _ReuniteSeparatedLocations with two locations separated by '.'
        """
        originals = ['I', 'went', 'to', 'Chicago', nlp.NLP_PUNCTUATION_TOKEN,
                     'Phoenix', 'is', 'hotter']
        tagged = [
            (originals[0], OTHER),      # I
            (originals[1], OTHER),      # went
            (originals[2], OTHER),      # to
            (originals[3], LOCATION),   # Chicago
            (originals[4], OTHER),      # NLP_PUNCTUATION_TOKEN
            (originals[5], LOCATION),   # Phoenix
            (originals[6], OTHER),      # is
            (originals[7], OTHER)]      # hotter
        expected = [('Chicago', 'LOCATION'), ('Phoenix', 'LOCATION')]
        actual = self.Tagger._ReuniteSeparatedLocations(originals, tagged)
        print 'expected -> %s' % str(expected)
        print 'actual -> %s' % str(actual)
        assert expected == actual

    def test_ReuniteSeparatedLocations3(self):
        """
        Tests _ReuniteSeparatedLocations with a three word location
        """
        originals = ['I', 'went', 'to', 'Half', 'Moon', 'Bay', 'in',
                     'California']
        tagged = [
            (originals[0], OTHER),      # I
            (originals[1], OTHER),      # went
            (originals[2], OTHER),      # to
            (originals[3], LOCATION),   # Half
            (originals[4], LOCATION),   # Moon
            (originals[5], LOCATION),   # Bay
            (originals[6], OTHER),      # in
            (originals[7], LOCATION)]   # California
        expected = [('Half Moon Bay', LOCATION), ('California', LOCATION)]
        actual = self.Tagger._ReuniteSeparatedLocations(originals, tagged)
        print 'expected -> %s' % str(expected)
        print 'actual -> %s' % str(actual)
        assert expected == actual

    def test_ReuniteSeparatedLocations4(self):
        """
        Tests _ReuniteSeparatedLocations with several multi-word locations
        """
        originals = ['I', 'went', 'to', 'Half', 'Moon', 'Bay', 'in',
                     'California', nlp.NLP_PUNCTUATION_TOKEN, "I've", 'never',
                     'been', 'to', 'Hong', 'Kong', ',', 'China',
                     nlp.NLP_PUNCTUATION_TOKEN, 'Have', 'you', 'been', 'to',
                     'San', 'Luis', 'Obispo', ',', 'California',
                     nlp.NLP_PUNCTUATION_TOKEN]
        tagged = [
            (originals[0], OTHER),      # I
            (originals[1], OTHER),      # went
            (originals[2], OTHER),      # to
            (originals[3], LOCATION),   # Half
            (originals[4], LOCATION),   # Moon
            (originals[5], LOCATION),   # Bay
            (originals[6], OTHER),      # in
            (originals[7], LOCATION),   # California
            (originals[8], OTHER),      # .
            (originals[9], OTHER),      # I've
            (originals[10], OTHER),     # never
            (originals[11], OTHER),     # been
            (originals[12], OTHER),     # to
            (originals[13], LOCATION),  # Hong
            (originals[14], LOCATION),  # Kong
            (originals[15], OTHER),     # ,
            (originals[16], LOCATION),  # China
            (originals[17], OTHER),     # .
            (originals[18], OTHER),     # Have
            (originals[19], OTHER),     # you
            (originals[20], OTHER),     # been
            (originals[21], OTHER),     # to
            (originals[22], LOCATION),  # San
            (originals[23], LOCATION),  # Luis
            (originals[24], LOCATION),  # Obispo
            (originals[25], OTHER),     # ,
            (originals[26], LOCATION),  # California
            (originals[27], OTHER)]     # ?
        # print tagged
        expected = [
            ('Half Moon Bay', LOCATION),
            ('California', LOCATION),
            ('Hong Kong', LOCATION),
            ('China', LOCATION),
            ('San Luis Obispo', LOCATION),
            ('California', LOCATION)
        ]
        actual = self.Tagger._ReuniteSeparatedLocations(originals, tagged)
        print 'expected -> %s' % str(expected)
        print 'actual -> %s' % str(actual)
        assert expected == actual

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

    def test_TagLocations2(self):
        """
        Tests TagLocations with multi-word location sentence from
        Agric_Hum_Values.txt
        """
        text = ("We draw from the rich history of hazards research to explore "
                "how evolving livelihood strategies and the consequent shift "
                "in the role of agriculture in the Upper Lerma Valley may "
                "provide insights into the meaning of flood losses to rural "
                "populations, and thus new opportunities for flood management."
                )
        expected = ['Upper Lerma Valley']
        actual = self.Tagger.TagLocations(text)
        assert expected == actual

    def test_Repr(self):
        """
        Tests the __repr__ function for correct output
        """
        placeh = self.Tagger.__repr__()
        assert placeh == "<LocationTagger(Tagger=%s)>" % (self.Tagger.Tagger)
