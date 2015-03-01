#!/usr/bin/python
import geojson
# import json
# import sets
import re
from ast import literal_eval


#takes in geojson looks for coordinates
#keep track of what location = what location name
# new google.maps.Latlng(37.785, -122.443)
# geojson points need to be switched.


def send_web():
    return None


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


class LatLng():

    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng


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


def RemoveDuplicatesFromList(l):

    """Unicode to string, assuming there will be no characters that lie
    outside of ascii range"""

    stringlist = [str(x) for x in l]
    nodublicate_array = []
    list(set(stringlist))
    [nodublicate_array.append(item) for item in stringlist if item
     not in nodublicate_array]
    return nodublicate_array


def MakeGeoJsonElement(location, existing_locations):
    """Gets the first hit that it gets with the given location name.
    It only searches the name instead of the other parameters.
    Also because of first hit, the accuracy is not very good.
    Will need to add additional logic for checking""" 

    """
    Right now these values are hard coded until the results can be improved.
    """
    # P.PPL a populated place like a city, town or village
    ft = 'P.PPL'
    loc = Location.query.filter_by(name=location, featuretype=ft, countrycode='US') \
                        .order_by('id').first()

    lon = 0.00
    lat = 0.00

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
    # Remove duplicates
    noduplicates = RemoveDuplicatesFromList(locations)

    # Turn locations into FeaturePoints
    feature_array = []
    for l in noduplicates:
        feature_array.append(MakeGeoJsonElement(l, locations))

    # Convert FeaturePoints List to FeatureCollection
    return geojson.FeatureCollection(feature_array)
