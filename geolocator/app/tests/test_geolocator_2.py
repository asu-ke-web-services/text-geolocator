# tests/test_geolocator.py
"""
run with: sudo fig run web nosetests geolocator/app/tests/test_1.py
"""
from app.geolocator import *
from app.models import Location
import unittest
from nose.tools import nottest



class validCoordinateTestCase(unittest.TestCase):
    """
    Tests for app.geolocator.LatLng
    """

    # ----------------------- Before/After ----------------------- #
    def setUp(self):
        """
        Executed at the start of every test
        """
        self.LatLng = None
        return

    def tearDown(self):
        """
        Executed at the end of every test
        """
        self.LatLng = None
        return

    # ----------------------- Helpers ----------------------- #
    def init(self, identity, lat, lng):
        
        self.LatLng = LatLng(identity,lat,lng)
        return

    # ----------------------- Tests ----------------------- #
    def test__init__pass(self):
        """
        Ensures that the LatLng successfully initializes
        """
        IDENTITY = 'Phoenix'
        LAT = '82.546'
        LNG = '36.111'
        self.init(IDENTITY,LAT,LNG) 

        assert self.LatLng.identity == IDENTITY
        assert self.LatLng.lat == LAT
        assert self.LatLng.lng == LNG


        return

    def test_LatLngFunction(self):
        """
        Tests the LatLng function
        """
        return

    def reprTest(self):
        """
        Tests the repr function to check for existence of strings
        """
        IDENTITY = " "
        LAT = " "
        LNG = " "
        self.init(IDENTITY,LAT,LNG)
        actual = self.LatLng.__repr__()
        assert isinstance(actual, str)


        return


            

class GeoJsonSyntaxTestCase(unittest.TestCase):
    """
    Tests for app.geolocator.GeoJSONer
    """

     # ----------------------- Before/After ----------------------- #
    def setUp(self):
        """
        Executed at the start of every test
        """
        self.GeoJSONer = GeoJSONer()
        return

    def tearDown(self):
        """
        Executed at the end of every test
        """
        self.GeoJSONer = None
        return

    def init(self):
        self.GeoJSONer = GeoJSONer(self,features)
        return


    def test__init__pass(self):
        """
        Ensures that the GeoJSON object successfully initializes
        """
        assert self.GeoJSONer.features == []
        assert isinstance(self.GeoJSONer,GeoJSONer)
        return

    def test_convert_to_feature(self):
        l = Location("Phoenix", "a", "Phoenix", "a", 'a', 'a', 'a', 5.0, -10.0, 0)
        location = LocationWrap(l)
        geometry = {
            'type': 'Point',
            'coordinates': [
                location.latitude(),
                location.longitude()
            ]
        }
        properties = {
            'weight': location.weight(),
            'name': location.name()
        }

        expected = geojson.Feature(location.name(), geometry, properties)
        actual = self.GeoJSONer._convert_to_feature(location)
        assert expected == actual
        return

        #test statements to check for correct syntax:
        #assert that geometry = a test point and test coordinates?
        #assert that properties = weight and name
        assert geometry ==  {
            'type': 'Point',
            'coordinates': [82.546,36.111]
        }

        assert properties == {
            'weight': 1,
            'name': 'Phoenix'
        }


        return feature

    def append_helper(self,name,lat,lng):
        l = Location(name, "hello", name, "hello", "hello",
                 "hello", "hello", lat, lng,
                 "hello")
        location = LocationWrap(l)
        return location


    def test_append_(self):

        f1 = self.append_helper("location1", 1.0, -2.0)
        f2 = self.append_helper("location2", 2.0, -3.0)
        f3 = self.append_helper("location3", 3.0, -4.0)
        tempf1 = self.GeoJSONer._convert_to_feature(f1)
        tempf2 = self.GeoJSONer._convert_to_feature(f2)
        tempf3 = self.GeoJSONer._convert_to_feature(f3)

        list1 = [tempf1, tempf2, tempf3]
        self.GeoJSONer.append(f1)
        self.GeoJSONer.append(f2)
        self.GeoJSONer.append(f3)
        
        print list1
        print self.GeoJSONer.features
        assert list1 == self.GeoJSONer.features



# class locationHitsTestCase(unittest.TestCase):
#     """
#     Tests for app.geolocator.LocationHits
#     """

#     # ----------------------- Before/After ----------------------- #
#     def setUp(self):
#         """
#         Executed at the start of every test
#         """
#         self.hits = None
#         return

#     def tearDown(self):
#         """
#         Executed at the end of every test
#         """
#         self.hits = None
#         return

#     # ----------------------- Helpers ----------------------- #
#     def init(self, locations=[]):
#         self.hits = LocationHits(locations)
#         return

#     def test__init__pass(self):
#         """
#         Ensures that the app.geolocator.LocationHits successfully initializes
#         """
#         LOCATIONS = ['Phoenix', 'Tucson', 'Flagstaff']
#         self.init(LOCATIONS)
#         assert isinstance(self.hits, LocationHits)
#         assert self.hits.index == -1
#         assert self.hits.locations == LOCATIONS

#     def test__len__pass(self): 
#         """
#         Tests :func:`app.geolocator.LocationHits.__len__`
#         """
#         LOCATIONS = [] #no locations
#         expected = len(LOCATIONS)
#         self.init(LOCATIONS)
#         actual = len(self.hits)
#         assert expected == actual
