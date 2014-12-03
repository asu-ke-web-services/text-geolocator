from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_raises
from nose.tools import raises

from app import geojson_maker
from app import app
from app import nlp_magic


def test_removeduplicates():
	l = ['Phoenix', 'Phoenix', 'Arizona']
	correct = ['Phoenix', 'Arizona']
	test = geojson_maker.RemoveDuplicatesFromList(l)
	assert_equal(correct, test)


# can't find jar file (might need to test with Flask)
# def test_nlp():
# 	test = 'I live in Phoenix, Arizona.\nI live in Phoenix, Arizona.\nI live in Phoenix, Arizona.'
# 	# Use Flask's test client for our test.
# 	self.test_app = app.test_client()
 
#     # Make a test request to the conference app, supplying a fake From phone number
# 	response = self.test_app.post('/upload', data=test)
# 	correct = [u'Phoenix', u'Arizona', u'Phoenix', u'Arizona', u'Phoenix', u'Arizona']
# 	result = nlp_magic.FindLocations(test)
# 	assert_equal(result, correct)


# is looking for application on not localhost
# def test_geojson_maker():
# 	test = [u'Phoenix', u'Arizona', u'Phoenix', u'Arizona', u'Phoenix', u'Arizona']
# 	result = geojson_maker.MakeGeoJsonCollection(test)
# 	correct = ("""{
# 	    "features": [
# 	        {
# 	            "geometry": {
# 	                "coordinates": [
# 	                    0.0,
# 	                    0.0
# 	                ],
# 	                "type": "Point"
# 	            },
# 	            "id": "Phoenix",
# 	            "properties": {
# 	                "name": "Phoenix",
# 	                "weight": 3
# 	            },
# 	            "type": "Feature"
# 	        },
# 	        {
# 	            "geometry": {
# 	                "coordinates": [
# 	                    0.0,
# 	                    0.0
# 	                ],
# 	                "type": "Point"
# 	            },
# 	            "id": "Arizona",
# 	            "properties": {
# 	                "name": "Arizona",
# 	                "weight": 3
# 	            },
# 	            "type": "Feature"
# 	        }
# 	    ],
# 	    "type": "FeatureCollection"
# 		}""")
# 	assert_equal(str(result), correct)
