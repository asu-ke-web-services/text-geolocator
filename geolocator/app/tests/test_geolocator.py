# tests/test_geolocator.py
"""
run with: sudo fig run web nosetests geolocator/app/tests/test_weighter.py
"""
from app.geolocator import LocationWrap, LocationHits, LocationHitsContainer
from app.weighter import LocationAdminNames
import unittest


class Location(object):
    def __init__(self, name, longitude, latitude, geonameid):
        self.name = name
        self.longitude = longitude
        self.latitude = latitude
        self.geonameid = geonameid


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
    def init(self, location):
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
        assert self.wrap.adminnames is None

    def test_LocationItems(self):
        """
        Tests the "getter" functions for the locationwrapper
        """
        loc = Location('Phoenix', 82.546, 36.111, 'phx')
        locwrap = LocationWrap(loc)
        COUNTRY = 'Jang'
        A1 = 'Bob'
        A2 = '1'
        A3 = '2'
        A4 = '3'
        l1 = LocationAdminNames(
            countryname='Jang',
            admin1name='Bob',
            admin2name='1',
            admin3name='2',
            admin4name='3')
        locwrap.set_adminnames(l1)
        locwrap._weight = 1

        assert locwrap.name() == 'Phoenix'
        assert locwrap.longitude() == 82.546
        assert locwrap.latitude() == 36.111
        assert locwrap.geonameid() == 'phx'
        assert locwrap.weight() == 1
        assert locwrap.countryname() == COUNTRY
        assert locwrap.admin1name() == A1
        assert locwrap.admin2name() == A2
        assert locwrap.admin3name() == A3
        assert locwrap.admin4name() == A4

        return

    def test__eq__fail_on_wrap(self):
        """
        Tests LocationWrap.__eq__ with two unequal wraps
        """
        l1 = LocationWrap('equal')
        l2 = 'i am a string and not a wrap'
        l1._weight = 8374
        l1.adminnames = [1, 2, 3, 4]
        assert l1 != l2

    def test__eq__fail_on_location(self):
        """
        Tests LocationWrap.__eq__ with two unequal wraps
        """
        l1 = LocationWrap('equal')
        l2 = LocationWrap('not equal')
        l1._weight = 8374
        l2._weight = 8374
        l1.adminnames = [1, 2, 3, 4]
        l2.adminnames = [1, 2, 3, 4]
        assert l1 != l2

    def test__eq__fail_on_weight(self):
        """
        Tests LocationWrap.__eq__ with two unequal wraps
        """
        l1 = LocationWrap('equal')
        l2 = LocationWrap('equal')
        l1._weight = 8374
        l2._weight = -8374
        l1.adminnames = [1, 2, 3, 4]
        l2.adminnames = [1, 2, 3, 4]
        assert l1 != l2

    def test__eq__fail_on_adminnames(self):
        """
        Tests LocationWrap.__eq__ with two unequal wraps
        """
        l1 = LocationWrap('equal')
        l2 = LocationWrap('equal')
        l1._weight = 8374
        l2._weight = 8374
        l1.adminnames = [1, 2, 3, 4]
        l2.adminnames = [1, 'not 2', 3, 4]
        assert l1 != l2

    def test__index_of_admin_name__4(self):
        """
        Tests LocationWrap.index_of_admin_name for admin4name
        """
        NAME = 'fruit'
        names = LocationAdminNames(countryname='banana', admin4name=NAME)
        wrap = LocationWrap(location=None, weight=0, adminnames=names)
        expected = 4
        actual = wrap.index_of_admin_name(NAME)
        assert expected == actual

    def test__index_of_admin_name__3(self):
        """
        Tests LocationWrap.index_of_admin_name for admin3name
        """
        NAME = 'fruit'
        names = LocationAdminNames(countryname='banana', admin3name=NAME)
        wrap = LocationWrap(location=None, weight=0, adminnames=names)
        expected = 3
        actual = wrap.index_of_admin_name(NAME)
        assert expected == actual

    def test__index_of_admin_name__2(self):
        """
        Tests LocationWrap.index_of_admin_name for admin2name
        """
        NAME = 'fruit'
        names = LocationAdminNames(countryname='banana', admin2name=NAME)
        wrap = LocationWrap(location=None, weight=0, adminnames=names)
        expected = 2
        actual = wrap.index_of_admin_name(NAME)
        assert expected == actual

    def test__index_of_admin_name__1(self):
        """
        Tests LocationWrap.index_of_admin_name for admin1name
        """
        NAME = 'fruit'
        names = LocationAdminNames(countryname='banana', admin1name=NAME)
        wrap = LocationWrap(location=None, weight=0, adminnames=names)
        expected = 1
        actual = wrap.index_of_admin_name(NAME)
        assert expected == actual

    def test__index_of_admin_name__0(self):
        """
        Tests LocationWrap.index_of_admin_name for countryname
        """
        NAME = 'banana'
        names = LocationAdminNames(countryname=NAME, admin4name='no')
        wrap = LocationWrap(location=None, weight=0, adminnames=names)
        expected = 0
        actual = wrap.index_of_admin_name(NAME)
        assert expected == actual

    def test__increment_weight_on_match__1(self):
        """
        Tests LocationWrap.increment_weight_on_match with admin1 match
        """
        NAME = 'orange'
        names = LocationAdminNames(countryname='not orange', admin4name=NAME)
        wrap = LocationWrap(location=None, weight=3, adminnames=names)
        actual = wrap.increment_weight_on_match(NAME)
        assert actual is True
        expected_weight = 4
        actual_weight = wrap._weight
        assert expected_weight == actual_weight

    def test__increment_weight_on_match__2(self):
        """
        Tests LocationWrap.increment_weight_on_match with admin2 match
        """
        NAME = 'orange'
        names = LocationAdminNames(countryname='not orange', admin2name=NAME)
        wrap = LocationWrap(location=None, weight=3, adminnames=names)
        actual = wrap.increment_weight_on_match(NAME)
        assert actual
        expected_weight = 4
        actual_weight = wrap._weight
        assert expected_weight == actual_weight

    def test__increment_weight_on_match__3(self):
        """
        Tests LocationWrap.increment_weight_on_match with admin3 match
        """
        NAME = 'orange'
        names = LocationAdminNames(countryname='not orange', admin3name=NAME)
        wrap = LocationWrap(location=None, weight=3, adminnames=names)
        actual = wrap.increment_weight_on_match(NAME)
        assert actual
        expected_weight = 4
        actual_weight = wrap._weight
        assert expected_weight == actual_weight

    def test__increment_weight_on_match__4(self):
        """
        Tests LocationWrap.increment_weight_on_match with admin4 match
        """
        NAME = 'orange'
        names = LocationAdminNames(countryname='not orange', admin4name=NAME)
        wrap = LocationWrap(location=None, weight=3, adminnames=names)
        actual = wrap.increment_weight_on_match(NAME)
        assert actual
        expected_weight = 4
        actual_weight = wrap._weight
        assert expected_weight == actual_weight

    def test__increment_weight_on_match__no_match(self):
        """
        Tests LocationWrap.increment_weight_on_match with no match
        """
        NAME = 'orange'
        names = LocationAdminNames(
            countryname='not orange',
            admin1name='banana',
            admin2name='strawberry',
            admin3name='carrot',
            admin4name='apple')
        wrap = LocationWrap(location=None, weight=3, adminnames=names)
        actual = wrap.increment_weight_on_match(NAME)
        assert not actual
        expected_weight = 3
        actual_weight = wrap._weight
        assert expected_weight == actual_weight

    def test__increment_weight_on_match__0(self):
        """
        Tests LocationWrap.increment_weight_on_match with country match
        """
        NAME = 'orange'
        names = LocationAdminNames(countryname=NAME, admin4name='not')
        wrap = LocationWrap(location=None, weight=0, adminnames=names)
        actual = wrap.increment_weight_on_match(NAME)
        assert actual
        expected_weight = 1
        actual_weight = wrap._weight
        assert expected_weight == actual_weight

    def test__names_list__pass(self):
        """
        Tests LocationWrap.names_list with a populated adminnames
        """
        A1 = 'orange'
        A2 = 'banana'
        A3 = 'cranberry'
        A4 = 'peach'
        CO = 'carrot'
        names = LocationAdminNames(
            countryname=CO,
            admin1name=A1,
            admin2name=A2,
            admin3name=A3,
            admin4name=A4)
        wrap = LocationWrap(location=None, weight=0, adminnames=names)
        expected = [A4, A3, A2, A1, CO]
        actual = wrap.names_list()
        assert expected == actual

    def test__names_list__empty(self):
        """
        Tests LocationWrap.names_list with an empty adminnames
        """
        wrap = LocationWrap(location=None, weight=0, adminnames=None)
        expected = []
        actual = wrap.names_list()
        assert expected == actual

    def test__names_list__not_adminnames(self):
        """
        Tests LocationWrap.names_list with an adminnames that is not the right
        type
        """
        wrap = LocationWrap(location=None, weight=0, adminnames=1)
        expected = []
        actual = wrap.names_list()
        assert expected == actual

    def test__eq__pass(self):
        """
        Tests LocationWrap.__eq__ with two unequal wraps
        """
        l1 = LocationWrap('equal')
        l2 = LocationWrap('equal')
        l1._weight = 8374
        l2._weight = 8374
        l1.adminnames = [1, 2, 3, 4]
        l2.adminnames = [1, 2, 3, 4]
        assert l1 == l2


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
        self.hits = LocationHits(name='testHits', locations=locations)
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
        s1 = LocationAdminNames(
            countryname='Jang',
            admin1name='Bob',
            admin2name=None,
            admin3name=None,
            admin4name=None)
        locwrap.set_adminnames(s1)
        loc2 = Location('Denver', 18.546, 44.111, 'den')
        locwrap2 = LocationWrap(loc2)
        s2 = s1
        locwrap2.set_adminnames(s2)
        l1 = [locwrap, locwrap2]
        self.init(l1)
        self.hits.increment_weight_on_match('Phoenix')

        f1 = self.hits.max_weight
        assert f1 != 1

    def test__len__pass(self):
        """
        Tests :func:`app.geolocator.LocationHits.__len__`
        """
        LOCATIONS = ['yes', 'no', 'maybe']
        expected = len(LOCATIONS)
        self.init(LOCATIONS)
        actual = len(self.hits)
        assert expected == actual

    def test__eq__fail_on_hits(self):
        """
        Tests __eq__ - fails on isinstance(other, LocationHits)
        """
        hits1 = LocationHits(name='hits1', locations=['l1', 'l2'])
        hits2 = 'not a LocationHits'
        assert hits1 != hits2

    def test__eq__fail_on_name(self):
        """
        Tests __eq__ - fails on name
        """
        hits1 = LocationHits(name='hits1', locations=['l1', 'l2'])
        hits2 = LocationHits(name='not hits1', locations=['l1', 'l2'])
        assert hits1 != hits2

    def test__eq__fail_on_locations(self):
        """
        Tests __eq__ - fails on locations
        """
        hits1 = LocationHits(name='hits1', locations=['l1', 'l2'])
        hits2 = LocationHits(name='hits1', locations=['l1', 'not l2'])
        assert hits1 != hits2

    def test__eq__pass(self):
        """
        Tests __eq__ expected to pass
        """
        hits1 = LocationHits(name='hits1', locations=['l1', 'l2'])
        hits2 = LocationHits(name='hits1', locations=['l1', 'l2'])
        assert hits1 == hits2

    def test__max_weight__empty(self):
        """
        Tests max_weight with an empty LocationHits
        """
        hits = LocationHits(name='hits', locations=[])
        expected = -1
        actual = hits.max_weight()
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
        # self.hits = LocationHitsContainer(locations)
        return

    # ----------------------- Tests ----------------------- #
    def test__init__pass(self):
        """
        Ensures that the app.geolocator.LocationHits successfully initializes
        """
        LOCATIONS = ['apple', 'banana', 'orange']
        self.init(LOCATIONS)
        # assert isinstance(self.hits, LocationHits)
        # assert self.hits.index == -1
        # assert self.hits.locations == LOCATIONS

    def test__eq__fail_on_container(self):
        """
        Test __eq__ - fails on isinstance(other, LocationHitsContainer)
        """
        c1 = LocationHitsContainer()
        c2 = "not a container"
        assert c1 != c2

    def test__eq__fail_on_hits(self):
        """
        Test __eq__ - fails on hits
        """
        c1 = LocationHitsContainer()
        c1.hits = 'yes'
        c2 = LocationHitsContainer()
        c2.hits = 'no'
        assert c1 != c2

    def test__eq__pass(self):
        """
        Test __eq__ - fails on isinstance(other, LocationHitsContainer)
        """
        c1 = LocationHitsContainer()
        c1.hits = [1, 2, 3]
        c2 = LocationHitsContainer()
        c2.hits = [1, 2, 3]
        assert c1 == c2

    def __len__(self):
        """
        Tests __len__
        """
        hits1 = LocationHits(name='hits1', locations=[1, 2])
        hits2 = LocationHits(name='hits2', locations=[1, 2, 3])
        container = LocationHitsContainer()
        container.append(hits1)
        container.append(hits2)
        expected = len(hits1) + len(hits2)
        actual = len(container)
        assert expected == actual
