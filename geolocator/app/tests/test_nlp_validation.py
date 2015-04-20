# tests/test_nlp_validation.py
"""
run with:

    sudo fig run web nosetests geolocator/app/tests/test_nlp_validation.py

To produce XML output:

    sudo fig run web nosetests
    geolocator/app/tests/test_nlp_validation.py:TaggerValidationTests
    --with-xunit --xunit-file=test_output.xml

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
                if row[1] == '1':
                    locations.append(row[0])
        return locations

    def getAllLocations(self, text):
        """
        Helper Function to tag locations but not remove duplicates
        """
        text = self.Tagger._PreProcessText(text)
        tagged = self.Tagger.Tagger.Tag(text)
        tagged = self.Tagger._ReuniteSeparatedLocations(text, tagged)
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

    def doesPass(self, expected, actual):
        """
        Helper function to determine if results are above pass rate
        of 80 percent (pass rate determined by Ivan)

        :param list expected: expected test results
        :param list actual: actual test results

        :returns: True or False
        """
        print 'expected -> %s\n' % str(expected)
        print 'actual -> %s\n' % str(actual)
        missed = []
        for e in expected:
            if not (e in actual):
                missed.append(e)
        print 'missed -> %s\n' % str(missed)
        # assert len(missed) == 0
        percent_hit = float(1 - (float(len(missed)) / float(len(expected))))
        print 'percent_hit = %s' % str(percent_hit)
        assert percent_hit >= 0.80

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
        self.doesPass(expected, actual)

    # ----------------------- Tests ----------------------- #
    def test__Agric_Hum_Values(self):
        """
        Agric_Hum_Values: checks tagger results

        input and output from
        geolocator/sample-data/from-ivan/Agric_Hum_Values.txt
        """
        name = 'Agric_Hum_Values'
        self.runTestForFilesWithName(name)

    def test__Bhattachan_etal_2014_Ecosphere(self):
        """
        Bhattachan_etal_2014_Ecosphere: checks tagger results

        input and output from geolocator/sample-data/from-ivan/
        Bhattachan_etal_2014_Ecosphere.txt
        """
        name = 'Bhattachan_etal_2014_Ecosphere'
        self.runTestForFilesWithName(name)

    def test__Eby_etal_2014_Oecologia(self):
        """
        Eby_etal_2014_Oecologia: checks tagger results

        input and output data
        geolocator/sample-data/from-ivan/Eby_etal_2014_Oecologia.txt
        """
        name = 'Eby_etal_2014_Oecologia'
        self.runTestForFilesWithName(name)

    def test__Ecological_Modelling(self):
        """
        Ecological_Modelling: checks tagger results

        input and output data
        geolocator/sample-data/from-ivan/Ecological_Modelling.txt
        """
        name = 'Ecological_Modelling'
        self.runTestForFilesWithName(name)

    def test__Ecology_Letters(self):
        """
        Ecology_Letters: checks tagger results

        input and output data
        geolocator/sample-data/from-ivan/Ecology_Letters.txt
        """
        name = 'Ecology_Letters'
        self.runTestForFilesWithName(name)

    def test__Journal_of_Agrarian_Change(self):
        """
        Journal_of_Agrarian_Change: checks tagger results

        input and output data
        geolocator/sample-data/from-ivan/Journal_of_Agrarian_Change.txt
        """
        name = 'Journal_of_Agrarian_Change'
        self.runTestForFilesWithName(name)

    def test__Journal_of_Arid_Environments(self):
        """
        Journal_of_Arid_Environments: checks tagger results

        input and output data
        geolocator/sample-data/from-ivan/Journal_of_Arid_Environments.txt
        """
        name = 'Journal_of_Arid_Environments'
        self.runTestForFilesWithName(name)

    def test__Koerner_etal_2014_Ecology(self):
        """
        Koerner_etal_2014_Ecology: checks tagger results

        input and output data
        geolocator/sample-data/from-ivan/Koerner_etal_2014_Ecology.txt
        """
        name = 'Koerner_etal_2014_Ecology'
        self.runTestForFilesWithName(name)

    def test__Ladwig_etal_2014_REM(self):
        """
        Ladwig_etal_2014_REM: checks tagger results

        input and output data
        geolocator/sample-data/from-ivan/Ladwig_etal_2014_REM.txt
        """
        name = 'Ladwig_etal_2014_REM'
        self.runTestForFilesWithName(name)

    def test__REVIEWS_REVIEWS_REVIEWS(self):
        """
        REVIEWS_REVIEWS_REVIEWS: checks tagger results

        input and output data
        geolocator/sample-data/from-ivan/REVIEWS_REVIEWS_REVIEWS.txt
        """
        name = 'REVIEWS_REVIEWS_REVIEWS'
        self.runTestForFilesWithName(name)

    def test__Vicca_etal_2014_Biogeosciences_0(self):
        """
        Vicca_etal_2014_Biogeosciences_0: checks tagger results

        input and output data
        geolocator/sample-data/from-ivan/Vicca_etal_2014_Biogeosciences_0.txt
        """
        name = 'Vicca_etal_2014_Biogeosciences_0'
        self.runTestForFilesWithName(name)
