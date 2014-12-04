# -*- coding: utf-8 -*-
import geojson
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
