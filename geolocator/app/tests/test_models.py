# tests/test_models.py
"""
run with: sudo fig run web nosetests geolocator
"""
from app.models import Location
import unittest
# from nose.tools import nottest


class LocationTests(unittest.TestCase):
    """
    Tests for app.models.Location
    """

    # ----------------------- Before/After ----------------------- #
    def setUp(self):
        """
        Executed at the start of every test
        """
        self.Loc = None
        return

    def tearDown(self):
        """
        Executed at the end of every test
        """
        self.Loc = None
        return

    # ----------------------- Helpers ----------------------- #
    def init(self, location, geonameid, name, countrycode, featureclass,
             featurecode, featuretype, latitude, longitude, initial_weight):
        """
        Shortcut Helper Function
        Initializes self.Loc and sets all of its attributes.
        """
        self.Loc = Location(location, geonameid, name, countrycode,
                            featureclass, featurecode, featuretype, latitude,
                            longitude, initial_weight)

    # ----------------------- Tests ----------------------- #
    def test__init__success(self):
        """
        Tests models.Location init method
        """
        location = 'Banana'
        geonameid = 4000
        name = 'Banana'
        countrycode = 'Banana Tree'
        featureclass = 'Fruit'
        featurecode = 'FT'
        featuretype = 'Food'
        latitude = -9
        longitude = 89
        initial_weight = 25135431
        self.init(location, geonameid, name, countrycode, featureclass,
                  featurecode, featuretype, latitude, longitude,
                  initial_weight)
        assert isinstance(self.Loc, Location)
        assert self.Loc.location == location
        assert self.Loc.geonameid == geonameid
        assert self.Loc.name == name
        assert self.Loc.countrycode == countrycode
        assert self.Loc.featureclass == featureclass
        assert self.Loc.featurecode == featurecode
        assert self.Loc.latitude == latitude
        assert self.Loc.longitude == longitude
        assert self.Loc.initial_weight == initial_weight

    def test_repre(self):
        """
        Tests the __repr__ function for correct output
        """
        self.init(
            location='Mos Eisley',
            geonameid=33,
            name='Mos Eisley',
            countrycode='Tatooine',
            featureclass='dangerous',
            featurecode='dg',
            featuretype='City',
            latitude=43,
            longitude=34,
            initial_weight=1)
        s = self.Loc.__repr__()
        assert isinstance(s, str)
