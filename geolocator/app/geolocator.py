#!/usr/bin/python
"""
Contains the following classes:

    * LocationWrap
    * LocationHits
    * LocationHitsContainer
    * GeoJSONer
    * Geocoder
    * Geolocator
    * LatLng

This file converts a given list of locations into geojson.

At a high-level, it does the following:

    * Retrieves lat/lng coordinates for each given location from
    geonames db
    * Applies weights (if weights is on)
    * Creates a geojson object from locations
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
    Wrapper for an app.models.Location object

    Adds needed weight and admin names attributes

    Used by geolocator and weighter
    """

    def __init__(self, location, weight=0, adminnames=None):
        self.location = location
        self._weight = weight
        self.adminnames = adminnames

    def name(self):
        """
        :returns: 'name' of wrapped location
        """
        return self.location.name

    def geonameid(self):
        """
        :returns: 'geonameid' of wrapped location
        """
        return self.location.geonameid

    def admin1name(self):
        """
        :returns: 'admin1name' of wrapped location
        """
        name = None
        if self.adminnames:
            name = self.adminnames.admin1name
        return name

    def admin2name(self):
        """
        :returns: 'admin2name' of wrapped location
        """
        name = None
        if self.adminnames:
            name = self.adminnames.admin2name
        return name

    def admin3name(self):
        """
        :returns: 'admin3name' of wrapped location
        """
        name = None
        if self.adminnames:
            name = self.adminnames.admin3name
        return name

    def admin4name(self):
        """
        :returns: 'admin4name' of wrapped location
        """
        name = None
        if self.adminnames:
            name = self.adminnames.admin4name
        return name

    def countryname(self):
        """
        :returns: 'countryname' of wrapped location
        """
        name = None
        if self.adminnames:
            name = self.adminnames.countryname
        return name

    def latitude(self):
        """
        :returns: 'latitude' of wrapped location
        """
        return self.location.latitude

    def longitude(self):
        """
        :returns: 'longitude' of wrapped location
        """
        return self.location.longitude

    def weight(self):
        """
        :returns: weight value of location
        """
        return self._weight

    def set_adminnames(self, location_admin_names):
        """
        :param app.weighter.LocationAdminNames location_admin_names:
        admin names

        :returns: None
        """
        self.adminnames = location_admin_names
        return

    def index_of_admin_name(self, admin_name):
        """
        :param str admin_name: a name of a Location

        :returns: the index of the admin name that matches admin_name;
        otherwise -1
        """
        adminNum = -1
        if self.admin4name():
            adminNum = 4
        elif self.admin3name():
            adminNum = 3
        elif self.admin2name():
            adminNum = 2
        elif self.admin1name():
            adminNum = 1
        elif self.countryname():
            adminNum = 0
        return adminNum

    def increment_weight_on_match(self, location_name):
        """
        If location_name matches any of this location's admin names,
        then weight += 1

        :param str location_name: name of a location

        :returns: bool -- True if match; otherwise False
        """
        matched = False
        if self.admin1name() == location_name:
            self._weight += 1
            matched = True
        if self.admin2name() == location_name:
            self._weight += 1
            matched = True
        if self.admin3name() == location_name:
            self._weight += 1
            matched = True
        if self.admin4name() == location_name:
            self._weight += 1
            matched = True
        if self.countryname() == location_name:
            self._weight += 1
            matched = True
        return matched

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

    def __eq__(self, other):
        """
        Compares two LocationWraps

        :param LocationWrap other: other LocationWrap

        :returns: True if equal; otherwise False
        """
        return (isinstance(other, LocationWrap) and
                self.location == other.location and
                self._weight == other.weight and
                self.adminnames == other.adminnames)

    def __repr__(self):
        return "<LocationWrap(location=%s, weight=%s)" % (
            str(self.location.name), str(self._weight))


class LocationHits(object):
    """
    A wrapper for a list of app.geolocator.LocationWrap objects

    This is used as a container to store all hits for a specific Location
    from the geonames db.

    For Example:

        * Location = 'Phoenix'
        * Geonames returns 15 Phoenixes
        * All Phoenixes will be put into a LocationHits object

    Also serves as an iterator
    """

    def __init__(self, name, locations):
        self.index = -1
        self.name = name
        self.locations = locations

    def __iter__(self):
        """
        This makes the LocationHits class an iterator
        """
        self.index = -1
        return self

    def next(self):
        """
        Called when LocationHits is used as the iterator of a for loop

        For example:

        ` for hit in LocationHits:
        `     # calls LocationHits.next each iterator

        :returns: the location at self.index or None if iteration is complete
        """
        if self.index >= len(self.locations)-1:
            raise StopIteration
        else:
            self.index += 1
            return self.locations[self.index]

    def increment_weight_on_match(self, location_name):
        """
        Checks each location to see if any of its admin names matches
        location_name. If it does, then it increments its weight.

        :param str location_name: name of a location

        :returns: list of LocationWraps that match location_name
        """
        matched_locations = []
        for l in self.locations:
            matched = l.increment_weight_on_match(location_name)
            if matched:
                matched_locations.append(l)
        return matched_locations

    def max_weight(self):
        """
        Returns the max weight value within all locations

        :returns: int
        """
        weights = list()
        for wrap in self.locations:
            weights.append(wrap.weight())
        if len(weights) > 0:
            return max(weights)
        else:
            return -1

    def __len__(self):
        """
        length == number of locations within LocationHits object

        :returns: int
        """
        length = 0
        if self.locations:
            length = len(self.locations)
        return length

    def __eq__(self, other):
        """
        Compares two LocationHits

        :param LocationHits other: other LocationHits

        :returns: True if equal; otherwise False
        """
        return (isinstance(other, LocationHits) and
                self.name == other.name and
                self.locations == other.locations)

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

    def increment_weight_on_match(self, location_admin_names):
        """
        Checks each location to see if it or any of its admin names matches
        location_name. If it does, then it increments its weight.

        :param app.weighter.LocationAdminNames location_admin_names: admin
        names of a location

        :returns: None
        """
        for hits in self.hits:
            hits.increment_weight_on_match(location_admin_names)
        return

    def __len__(self):
        """
        Returns total number of contained locations

        NOTE: does NOT return number of LocationHits

        :returns: int
        """
        length = 0
        for h in self.hits:
            length += len(h)
        return length

    def __eq__(self, other):
        """
        Compares two LocationHitsContainer objects

        :param LocationHitsContainer other: other LocationHitsContainer

        :returns: True if equal; otherwise False
        """
        return (isinstance(other, LocationHitsContainer) and
                self.hits == other.hits)

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
            'name': location.name(),
            'countryname': location.countryname(),
            'admin1name': location.admin1name(),
            'admin2name': location.admin2name(),
            'admin3name': location.admin3name(),
            'admin4name': location.admin4name(),
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
        return LocationHits(location, matches)

    def __repr__(self):
        return "<Geocoder()>"


class Geolocator(object):
    """
    Master geolocation class

    Uses Geocoder and GeoJSONer and Weightifier to find coordinates for and
    apply weights to all tagged locations.
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


class LatLng():
    """
    A small container class that represents a Latitude/Longitude coordinate
    pair
    """

    def __init__(self, identity, lat, lng):
        self.identity = identity
        self.lat = lat
        self.lng = lng

    def __repr__(self):
        return "<LatLng(identity=%s, lat=%s, lng=%s)>" % (
            str(self.identity), str(self.lat), str(self.lng))


def RetrieveLatLngs(feature_collection):
    """
    Retrieves all the LatLng coordinates from a given geojson object

    By doing this with a regex, the operation of retrieving latlngs is
    very flexible and we are not strictly limited to geojson of the
    geojson library
    """
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
    for i, n in enumerate(coordinates_set):
        latlngs.append(LatLng(i, n[0], n[1]))
    return latlngs
