#!/usr/bin/python
"""
    Example Queries:
        * Returns all locations named Phoenix:
          SELECT l.name
          FROM location l
          WHERE l.name = 'Phoenix'
        * Returns all locations named Phoenix in the United States:
          SELECT l.name, l.featurecode, l.featureclass,
            l.admin4code, l.admin3code,
            l.admin2code, l.admin1code, l.countrycode
          FROM raw_locations l
          WHERE l.name = 'Phoenix'
            AND l.countrycode = 'US'
        * Returns just Arizona (the state):
          SELECT l.name, l.featurecode, l.featureclass,
            l.admin4code, l.admin3code,
            l.admin2code, l.admin1code, l.countrycode
          FROM raw_locations l
          WHERE l.admin1code = 'AZ'
            AND l.featurecode = 'ADM1'
            AND l.featureclass = 'A'
        * Returns just Maricopa County (in Arizona):
          SELECT l.name, l.featurecode, l.featureclass,
            l.admin4code, l.admin3code,
            l.admin2code, l.admin1code, l.countrycode
          FROM raw_locations l
          WHERE l.admin2code = '013'
            AND l.admin1code = 'AZ'
            AND l.featurecode = 'ADM2'

    The above queries can be executed like this:

        result = db.engine.execute(sql)
        hits = []
        for row in result:
            hits.append(row)
        return hits

        hits will then contain all the rows of the result of the query

"""
import geojson
import re
from ast import literal_eval
from app.models import Location
from app.weighter import Weightifier

ADMIN_FEATURE_CLASS = 'A'
ADMIN_FEATURE_CODES = [
    'ADM1',  # admin1
    'ADM2',  # admin2
    'ADM3',  # admin3
    'ADM4'   # admin4
]
POPULATED_PLACE_FEATURE_CLASS = 'P'
POPULATED_PLACE_FEATURE_CODES = [
    'PPLA',   # admin1
    'PPLA2',  # admin2
    'PPLA3',  # admin3
    'PPLA4'   # admin4
]


class LocationWrap(object):
    """
    Wrapper for an app.models.Location object. Adds needed weight attributes.
    """
    def __init__(self, location):
        self.location = location
        self._weight = 0
        self.adminnames = []

    def name(self):
        return self.location.name

    def latitude(self):
        return self.location.latitude

    def longitude(self):
        return self.location.longitude

    def weight(self):
        return self._weight

    def geonameid(self):
        return self.location.geonameid

    def set_adminnames(self, location_admin_names):
        self.adminnames = location_admin_names
        return

    def increment_weight_on_match(self, location_name):
        """
        If location_name matches either this location's name or any of this
        location's admin names, then weight += 1

        :param str location_name: a name of a location

        :returns: None
        """
        if (self.location.name == location_name or
                self.adminnames.match(location_name)):
            self._weight += 1
        return

    def names_list(self):
        """
        Returns location's name and all admin names as one list
        EDIT: Returns only admin names

        :returns: list of names
        """
        names = []
        # names.append(self.location.name)
        names.extend(self.adminnames.list())
        return names

    def __repr__(self):
        return "<LocationWrap(location=%s, weight=%s)" % (
            str(self.location.name), str(self._weight))


class LocationHits(object):
    """
    A wrapper for a list of app.geolocator.LocationWrap objects. Also serves as
    an iterator.
    """

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
            self.index += 1
            return self.locations[self.index]

    def increment_weight_on_match(self, location_name):
        """
        Checks each location to see if it or any of its admin names matches
        location_name. If it does, then it increments its weight.

        :param str location_name: name of a location

        :returns: None
        """
        for l in self.locations:
            l.increment_weight_on_match(location_name)
        return

    def __len__(self):
        length = 0
        if self.locations:
            length = len(self.locations)
        return length

    def __repr__(self):
        return "<LocationHits(len(locations)=%s, locations=%s)" % (
            str(len(self.locations)), str(self.locations))


class LocationHitsContainer(object):
    """
    A container for a one or more app.geolocator.LocationHits objects
    """
    def __init__(self):
        self.hits = []

    def append(self, location_hits):
        """
        Appends the given LocationHits object to the hits list

        :param app.geolocator.LocationHits location_hits: object to append

        :returns: None
        """
        self.hits.append(location_hits)

    def increment_weight_on_match(self, location_name):
        """
        Checks each location to see if it or any of its admin names matches
        location_name. If it does, then it increments its weight.

        :param str location_name: name of a location

        :returns: None
        """
        for hits in self.hits:
            hits.increment_weight_on_match(location_name)
        return

    def __len__(self):
        """
        Returns total number of contained locations
        """
        length = 0
        for h in self.hits:
            length += len(h)
        return length

    def __repr__(self):
        return "<LocationHitsContainer(len(hits)=%s)>" % (str(len(self.hits)))


class GeoJSONer(object):
    """
    Responsible for geojson creation and manipulation.
    """

    def __init__(self):
        self.features = []
        return

    def _convert_to_feature(self, location):
        """
        Converts the given LocationWrap object to a geojson.Feature
        object

        :param app.geolocator.LocationWrap location: object to convert

        :returns: geojson.Feature
        """
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

        feature = geojson.Feature(location.name(), geometry, properties)
        return feature

    def append(self, location):
        """
        Converts the given LocationWrap object to a geojson.Feature object and
        appends it to the feature list

        :param app.geolocator.LocationWrap location: object to append

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
    """
    Used to find coordinates of tagged locations
    """

    FT = 'P.PPL'
    """feature type denoting a populated place (doesn't quite work)"""

    def __init__(self):
        return

    def _wrap_location(self, location):
        """
        Converts the given Location object to a LocationWrap

        :param app.models.Location location: location object to convert

        :returns: app.geolocator.LocationWrap
        """
        return LocationWrap(location)

    def geocode(self, location):
        """
        Queries the geonames database and retrieves all matching locations

        :param str location: location name to query for

        :returns: app.geolocator.LocationHits object
        """
        matches = Location.query.filter_by(
            name=location).order_by('id').all()
        matches = map(self._wrap_location, matches)
        return LocationHits(matches)

    def __repr__(self):
        return "<Geocoder()>"


class Geolocator(object):
    """
    Master geolocation class. Uses Geocoder and GeoJSONer and Weightifier to
    find coordinates for and apply weights to all tagged locations.
    """

    def __init__(self):
        self.geocoder = Geocoder()
        self.geojsoner = GeoJSONer()
        self.weightifier = Weightifier()
        return

    def geolocate(self, locations, weights=True, accuracy=1):
        """
        Given a list of tagged locations from the NLP tagger, this will convert
        each location to a app.geolocator.LocationWrap, find the coordinates of
        each, apply weighting, and convert to geojson

        :param list locations: list of app.models.Location objects to geolocate
        :param bool weights: flag indicating if weights should be calculated or
        not (defaults to True)
        :param int accuracy: level of accuracy to use when calculating weights
        (defaults to 1) (must be greater than 0 and less than or equal to 5)
            * 1 - weights will be found for all matches to countrycode
            * 2 - weights will be found for all matches to the above and
            admin1code
            * 3 - weights will be found for all matches to the above and
            admin2code
            * 4 - weights will be found for all matches to the above and
            admin3code
            * 5 - weights will be found for all matches to the above and
            admin4code

        :returns: None
        """
        container = LocationHitsContainer()
        for l in locations:
            container.append(self.geocoder.geocode(l))

        if weights:
            if accuracy > 5:
                accuracy = 5
            container = self.weightifier.weightify(container, accuracy)

        for hits in container.hits:
            for l in hits:
                self.geojsoner.append(l)
        return

    def geojson(self):
        """
        Returns the geojson of all geolocated locations

        :returns: geojson.FeatureCollection
        """
        return self.geojsoner.geojson()

    def __repr__(self):
        return "<Geolocator()>"


# takes in geojson looks for coordinates
# keep track of what location = what location name
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
    # go through p list
    for n in p:
        m = literal_eval(n)
        coordinates_set.append(m)
        # push n to
    # now can access elements in coordinates_set as a set.
    print coordinates_set
    latlngs = []
    for n in coordinates_set:
        latlngs.append(LatLng(n[0], n[1]))
    return latlngs
