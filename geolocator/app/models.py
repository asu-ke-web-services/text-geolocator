# -*- coding: utf-8 -*-
"""
Contains the following classes:

    * Location
    * # Feature

The models in this file serve as the interface between this application
and the geonames database
"""
from app import db
from geoalchemy2 import Geometry


class Location(db.Model):
    """
    Represents a single location on a map from the geonames database.

    Geonames: http://www.geonames.org/
    """
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(Geometry('POINT'), index=True)
    geonameid = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(250), nullable=False, index=True)
    countrycode = db.Column(db.String(80), nullable=False)
    featureclass = db.Column(db.String(80), nullable=False)
    featurecode = db.Column(db.String(80), nullable=False)
    featuretype = db.Column(db.String(80), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    initial_weight = db.Column(db.Float, default=0.0, nullable=False)
    # admin1code = db.Column(db.String(80), index=True)
    # admin2code = db.Column(db.String(80), index=True)
    # admin3code = db.Column(db.String(80))
    # admin4code = db.Column(db.String(80))
    # countryname = db.Column(db.String(80), index=True)

    # def __init__(self, location, geonameid, name, countrycode, featureclass,
    #              featurecode, featuretype, latitude, longitude,
    #              initial_weight, admin1code, admin2code, admin3code,
    #              admin4code, countryname):
    #     """
    #     Sets all of the Location's attributes.
    #     This is used when importing data from the geonames db.
    #     """
    #     self.location = location
    #     self.geonameid = geonameid
    #     self.name = name
    #     self.countrycode = countrycode
    #     self.featureclass = featureclass
    #     self.featurecode = featurecode
    #     self.featuretype = featuretype
    #     self.latitude = latitude
    #     self.longitude = longitude
    #     self.initial_weight = initial_weight
    #     self.admin1code = admin1code
    #     self.admin2code = admin2code
    #     self.admin3code = admin3code
    #     self.admin4code = admin4code
    #     self.countryname = countryname

    def __init__(self, location, geonameid, name, countrycode, featureclass,
                 featurecode, featuretype, latitude, longitude,
                 initial_weight):
        """
        Sets all of the Location's attributes.
        This is used when importing data from the geonames db.
        """
        self.location = location
        self.geonameid = geonameid
        self.name = name
        self.countrycode = countrycode
        self.featureclass = featureclass
        self.featurecode = featurecode
        self.featuretype = featuretype
        self.latitude = latitude
        self.longitude = longitude
        self.initial_weight = initial_weight

    def __eq__(self, other):
        """
        Operator function for '=='. Compares two Location objects.

        :param Location other: Location to compare to self

        :returns: True if equal; otherwise False
        """
        return (isinstance(other, Location) and
                self.id == other.id and
                self.location == other.location and
                self.geonameid == other.geonameid and
                self.name == other.name and
                self.countrycode == other.countrycode and
                self.featureclass == other.featureclass and
                self.featurecode == other.featurecode and
                self.featuretype == other.featuretype and
                self.latitude == other.latitude and
                self.longitude == other.longitude and
                self.initial_weight == other.initial_weight)

    def __repr__(self):
        return '<Location %r>' % self.name


# class Feature(db.Model):
#     """
#     Represents a Feature from the geonames db.
#     A Feature is a classification attribute.

#     For more info, see http://www.geonames.org/
#     """

#     id = db.Column(db.Integer, primary_key=True)
#     featureclass = db.Column(db.String(80), nullable=False)
#     featurecode = db.Column(db.String(80), nullable=False)
#     code = db.Column(db.String(80), nullable=False)
#     name = db.Column(db.String(250), nullable=False)
#     description = db.Column(db.String(500), nullable=False)

#     def __init__(self, featureclass, featurecode, code, name, description):
#         """
#         Sets all of the Feature's attributes.
#         This is used when importing data from the geonames db.
#         """
#         self.featureclass = featureclass
#         self.featurecode = featurecode
#         self.code = '%s.%s' % (featureclass, featurecode)
#         self.name = name
#         self.description = description

#     def __repr__(self):
#         return '<Feature %r>' % self.name
