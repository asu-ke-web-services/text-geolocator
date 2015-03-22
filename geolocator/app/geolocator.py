#!/usr/bin/python
import geojson
# import json
# import sets
import re
from ast import literal_eval


class LocationMatches(object):

    def __init__(self, locations):
        self.index = -1
        self.locations = locations

    def __iter__(self):
        self.index = -1
        return self

    def next(self):
        if self.index >= len(self.locations)-1:
            raise StopIteration
        else:
            return self.locations[self.index]

    def __repr__(self):
        return "<LocationMatches(len(locations)=%s, locations=%s)" % (
            str(len(self.locations)), str(self.locations))


class GeoJSONer(object):

    def __init__(self):
        self.features = []
        return

    def _convert_to_feature(self, location):
        """
        Converts the given app.models.Location object to a geojson.Feature
        object

        :param app.models.Location location: Location object to convert

        :returns: geojson.Feature
        """
        geometry = {
            'type': 'Point',
            'coordinates': [
                location.latitude,
                location.longitude
            ]
        }
        properties = {
            # 'weight': location.weight,
            'weight': 1,
            'name': location.name
        }

        feature = geojson.Feature(location.name, geometry, properties)
        return feature

    def append(self, location):
        """
        Converts the given Location object to a geojson.Feature object and
        appends it to the feature list

        :param app.models.Location location: Location object to append

        :returns: None
        """
        feature = self._convert_to_feature(location)
        self.features.append(feature)
        return

    def geojson(self):
        """
        Returns the features array as a geojson.FeatureCollection
        """
        return geojson.FeatureCollection(self.features)

    def __repr__(self):
        return "<GeoJSONer()>"


class Geocoder(object):

    FT = 'P.PPL'

    def __init__(self):
        return

    def geocode(self, location):
        """
        Queries the geonames database and retrieves all matching locations

        :param str location: name of location to query for

        :returns: app.geolocator.LocationMatches object
        """
        matches = Location.query.filter_by(
            name=location
            # featuretype=ft
        ).order_by('id').all()
        return LocationMatches(matches)

    def __repr__(self):
        return "<Geocoder()>"


class Geolocator(object):

    def __init__(self):
        self.geocoder = Geocoder()
        self.geojsoner = GeoJSONer()
        return

    def geolocate(self, locations):
        """
        Given a list of tagged locations from the NLP tagger, this will
        find the coordinates of each, apply weighting, and convert to geojson

        :param list locations: list of app.models.Location objects to geolocate

        :returns: None
        """
        for l in locations:
            matches = self.geocoder.geocode(l)
            self.geojsoner.append(matches)
        return

    def geojson(self):
        """
        Returns the geojson of all geolocated locations

        :returns: geojson.FeatureCollection
        """
        return self.geojsoner.geojson()

    def __repr__(self):
        return "<Geolocator()>"


#takes in geojson looks for coordinates
#keep track of what location = what location name
# new google.maps.Latlng(37.785, -122.443)
# geojson points need to be switched.

class LatLng():

    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng


def RetrieveLatLngs(feature_collection):
    p = re.findall(
        r"\[\-*\d+\.*\d*\,\s\-*\d+\.*\d*\]",
        str(feature_collection))
    coordinates_set = []
    #go through p list
    for n in p:
        m = literal_eval(n)
        coordinates_set.append(m)
        #push n to
    #now can access elements in coordinates_set as a set.
    print coordinates_set
    latlngs = []
    for n in coordinates_set:
        latlngs.append(LatLng(n[0], n[1]))
    return latlngs


def sam_MakeGeoJsonCollection(arg1):
    l = [u'Phoenix', u'Arizona', u'Austrailia', u'Flagstaff']
    coordinate_array = [[131.87, -25.76], [138.12, -25.04], [140.14, -21.04],
                        [144.14, -27.41]]
    stringlist = [str(x) for x in l]
    # unicode to string, assuming there will be no characters that lie
    # outside of ascii range
    feature_array = []
    nodublicate_array = []
    list(set(stringlist))
    coordinate_lat = 0
    coordinate_lon = 0
    [nodublicate_array.append(item) for item in stringlist if item not in nodublicate_array]
    for x in nodublicate_array:
       #lookup x in database
        lon = coordinate_array[coordinate_lon][coordinate_lat]
        coordinate_lat = coordinate_lat + 1
        lat = coordinate_array[coordinate_lon][coordinate_lat]
        coordinate_lon = coordinate_lon + 1
        coordinate_lat = coordinate_lat - 1
        #weight calculations
        weight = 0
        for y in stringlist:
            if x == y:
                weight = weight + 1
                print weight
        name = x

        feature_type = FeaturePoint(lon, lat, weight, name)
        feature_array.append(feature_type)
        #feature collection takes in an array
    feature_collection = geojson.FeatureCollection(feature_array)
    print feature_collection
    #print json.dumps(feature_collection, sort_keys=True,
    #   indent=4, separators=(',', ': '))
    #print  feature_collection
    return geojson_magicalparsing(feature_collection)
    print "\n\n\n\n"
    #print type(feature_collection)
    #print json.dumps(feature_collection, sort_keys=True,
    #   indent=4, separators=(',', ': '))

# if __name__ == '__main__':
#     main()

#pip install geojson
#pip install --upgrade geojson
# to test: in terminal:
    #python
    #from geojson import Point


# -*- coding: utf-8 -*-
# import geojson
from app.models import Location

def FeaturePoint(lon, lat, weight, name):
    geometry = {'type': 'Point', 'coordinates': [lat, lon]}
    properties = {'weight': weight, 'name': name}

    # Feature takes in: id= "", geometry json, property json

    feature = geojson.Feature(name, geometry, properties)
    return feature


def MakeGeoJsonElement(location, existing_locations):
    """Gets the first hit that it gets with the given location name.
    It only searches the name instead of the other parameters.
    Also because of first hit, the accuracy is not very good.
    Will need to add additional logic for checking"""

    """
    Right now these values are hard coded until the results can be improved.


    **************
    Sam's edit: commented out database queries for hard coded values.

    **************
    """
    # P.PPL a populated place like a city, town or village
    ft = 'P.PPL'
    loc = Location.query.filter_by(
        name=location).order_by('id').first()

    # lon = -111.932338
    # lat = 33.418669
    lon = 0
    lat = 0

    # If there is no match, the locations will be 0,0.....

    if loc is not None:
        lon = loc.longitude
        lat = loc.latitude

    # Weight calculations

    weight = 0
    for y in existing_locations:
        if location == y:
            weight = weight + 1
    name = location

    return FeaturePoint(lon, lat, weight, name)


def MakeGeoJsonCollection(locations):

    # Turn locations into FeaturePoints
    feature_array = []
    for l in locations:
        feature_array.append(MakeGeoJsonElement(l, locations))

    # Convert FeaturePoints List to FeatureCollection
    return geojson.FeatureCollection(feature_array)
