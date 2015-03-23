# tests/test_geolocator.py
"""
run with: sudo fig run web nosetests geolocator/app/tests/test_weighter.py
"""
from app.geolocator import LocationWrap, LocationHits, LocationHitsContainer
from app.models import Location
import unittest
from nose.tools import nottest

class Location(object):
    def __init__(self, name, longitude, latitude, geonameid):
	self.name = name
	self.longitude = longitude
	self.latitude = latitude
	self.geonameid = geonameid

class admin(object):
    def __init__(self, s1, s2):
	l1 = []
	l1.extend(s1)
	l1.extend(s2)	
	self.adminnames = l1
    def list(self):
	return self.adminnames
    def match(self, something):
	return True

class LocationWrapTestCase(unittest.TestCase):
    """
    Tests for app.geolocator.LocationWrap
    """

    # ----------------------- Before/After ----------------------- #
    def setUp(self):
        """
        Executed at the start of every test
        """
        self.wrap = None
        return

    def tearDown(self):
        """
        Executed at the end of every test
        """
        self.wrap = None
        return

    # ----------------------- Helpers ----------------------- #
    def init(self, location):#=Location()):
        self.wrap = LocationWrap(location)
        return

    # ----------------------- Tests ----------------------- #
    def test__init__pass(self):
        """
        Ensures that the LocationWrap successfully initializes
        """
        LOCATION = 'banana'
        self.init(LOCATION)
        assert isinstance(self.wrap, LocationWrap)
        assert self.wrap.location == LOCATION
        assert self.wrap._weight == 0
        assert self.wrap.adminnames == []

    def test_LocationItems(self):
        """
        Tests the "getter" functions for the locationwrapper
        """
	loc = Location('Phoenix', 82.546, 36.111, 'phx')
	locwrap = LocationWrap(loc)
	locwrap.increment_weight_on_match('Phoenix')
	#l1 = ['Jang', 'Bob']
	l1 = admin('Jang', 'Bob')
	locwrap.set_adminnames(l1)
	names = locwrap.names_list()

	assert locwrap.name() == 'Phoenix'
	assert locwrap.longitude() == 82.546
	assert locwrap.latitude() == 36.111
	assert locwrap.geonameid() == 'phx'
	assert locwrap.weight() == 1

        return


class LocationHitsTestCase(unittest.TestCase):
    """
    Tests for app.geolocator.LocationHits
    """

    # ----------------------- Before/After ----------------------- #
    def setUp(self):
        """
        Executed at the start of every test
        """
        self.hits = None
        return

    def tearDown(self):
        """
        Executed at the end of every test
        """
        self.hits = None
        return

    # ----------------------- Helpers ----------------------- #
    def init(self, locations=[]):
        self.hits = LocationHits(locations)
        return

    # ----------------------- Tests ----------------------- #
    def test__init__pass(self):
        """
        Ensures that the app.geolocator.LocationHits successfully initializes
        """
        LOCATIONS = ['apple', 'banana', 'orange']
        self.init(LOCATIONS)
        assert isinstance(self.hits, LocationHits)
        assert self.hits.index == -1
        assert self.hits.locations == LOCATIONS

    def test__iter__pass(self):
        """
        Tests :func:`app.geolocator.LocationHits.__iter__`
        """
        LOCATIONS = [1, 2, 3]
        self.init(LOCATIONS)
        self.hits.index = 7
        iterator = self.hits.__iter__()
        assert isinstance(iterator, LocationHits)
        assert iterator.index == -1
        assert iterator.locations == LOCATIONS

    def test__next__pass(self):
        """
        Tests :func:`app.geolocator.LocationHits.next`
        """
        LOCATIONS = [1, 2, 3]
        self.init(LOCATIONS)
        count = 0
        for i, l in enumerate(self.hits):
            assert l == LOCATIONS[i]
            count += 1
        assert count == len(LOCATIONS)

    def test__increment_weight_on_match__pass(self):
        """
        Tests :func:`app.geolocator.LocationHits.increment_weight_on_match`
        """
	loc = Location('Phoenix', 82.546, 36.111, 'phx')
	locwrap = LocationWrap(loc)
	s1 = admin('Jang', 'Bob')
	locwrap.set_adminnames(s1)
	loc2 = Location('Denver', 18.546, 44.111, 'den')
	locwrap2 = LocationWrap(loc2)
	s2 = admin('Jang', 'Bob')
	locwrap2.set_adminnames(s2)
	l1 = [locwrap, locwrap2]
        self.init(l1)
	self.hits.increment_weight_on_match('Phoenix')

	f1 = self.hits.max_weight
	assert f1 != 1 	

        return

    def test__len__pass(self):
        """
        Tests :func:`app.geolocator.LocationHits.__len__`
        """
        LOCATIONS = ['yes', 'no', 'maybe']
        expected = len(LOCATIONS)
        self.init(LOCATIONS)
        actual = len(self.hits)
        assert expected == actual

    def test__repr__pass(self):
        """
        Tests :func:`app.geolocator.LocationHits.__repr__`
        """
        LOCATIONS = ['yes', 'no', 'maybe']
        self.init(LOCATIONS)
        s = str(self.hits)
        # any raised errors will cause test to fail
        assert s is not None
        assert len(s) > 10


class LocationHitsContainerTestCase(unittest.TestCase):
    """
    Tests for app.geolocator.LocationHitsContainer
    """

    # ----------------------- Before/After ----------------------- #
    def setUp(self):
        """
        Executed at the start of every test
        """
        self.hits = LocationHitsContainer()
        return

    def tearDown(self):
        """
        Executed at the end of every test
        """
        self.hits = None
        return

    # ----------------------- Helpers ----------------------- #
    def init(self, locations=[]):
        #self.hits = LocationHitsContainer(locations)
        return

    # ----------------------- Tests ----------------------- #
    def test__init__pass(self):
        """
        Ensures that the app.geolocator.LocationHits successfully initializes
        """
        LOCATIONS = ['apple', 'banana', 'orange']
        self.init(LOCATIONS)
        #assert isinstance(self.hits, LocationHits)
        #assert self.hits.index == -1
        #assert self.hits.locations == LOCATIONS


