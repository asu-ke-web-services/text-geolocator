# tests/test_nlp.py
"""
run with: sudo fig run web nosetests geolocator
"""
from app import nlp
import unittest
import csv
import os
from nose.tools import nottest


class TaggerValidationTests(unittest.TestCase):

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
    def getFromIvanPath(self, dirname, filename):
        """
        Helper function to retrieve from-ivan input or output files
        """
        home = os.getcwd()
        path = ('%s/geolocator/sample-data/from-ivan/%s/%s' % (
            str(home), str(dirname), str(filename)))
        return path

    def getInputText(self, filename):
        """
        Helper function, returns text of specified file in from-ivan
        input directory
        """
        path = self.getFromIvanPath('input', filename)
        text = ''
        with open(path, 'r') as f:
            text = f.read()
        return text

    def getOutputList(self, filename):
        """
        Helper function, returns list of locations in specified file in
        from-ivan output directory
        """
        path = self.getFromIvanPath('output', filename)
        locations = []
        with open(path, 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                locations.append(row[0])
        return locations

    def getAllLocations(self, text):
        """
        Helper Function to tag locations but not remove duplicates
        """
        text = self.Tagger._ConvertToAscii(text)
        text = self.Tagger._PreProcessText(text)
        tagged = self.Tagger.Tagger.Tag(text)
        locations = self.Tagger._IsolateLocations(tagged)
        return locations

    def appendTXT(self, s):
        """
        Appends '.txt' to s
        """
        return s + '.txt'

    def appendCSV(self, s):
        """
        Appends '.csv' to s
        """
        return s + '.csv'

    @nottest
    def runTestForFilesWithName(self, name):
        """
        Helper test to reduce duplicate code.

        Given name, will retrieve text of name.txt and locations in
        name.csv and see if the Tagger's locations retrieved from name.txt
        match the locations in name.csv
        """
        input_txt = self.appendTXT(name)
        output_csv = self.appendCSV(name)
        text = self.getInputText(input_txt)
        expected = self.getOutputList(output_csv)
        actual = self.getAllLocations(text)
        print expected
        print actual
        assert expected == actual

    # ----------------------- Tests ----------------------- #
    def test__Agric_Hum_Values(self):
        """
        Checks that the tagger produces the expected locations when tested
        with geolocator/sample-data/from-ivan/Agric_Hum_Values.txt
        """
        name = 'Agric_Hum_Values'
        self.runTestForFilesWithName(name)
