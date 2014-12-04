# -*- coding: utf-8 -*-
from app import db


# from geoalchemy2.types import Geometry

class Location(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    # location = db.Column(Geometry(geometry_type='POINT', srid=4326))

    geonameid = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(250), nullable=False)
    countrycode = db.Column(db.String(80), nullable=False)
    featureclass = db.Column(db.String(80), nullable=False)
    featurecode = db.Column(db.String(80), nullable=False)
    featuretype = db.Column(db.String(80), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    initial_weight = db.Column(db.Float, default=0.0, nullable=False)

    def __init__(self, geonameid, name, countrycode, featureclass, featurecode,
                 featuretype, latitude, longitude, initial_weight):
        self.geonameid = geonameid
        self.name = name
        self.countrycode = countrycode
        self.featureclass = featureclass
        self.featurecode = featurecode
        self.featuretype = featuretype
        self.latitude = latitude
        self.longitude = longitude
        self.initial_weight = initial_weight

    def __repr__(self):
        return '<Location %r>' % self.name


class Feature(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    featureclass = db.Column(db.String(80), nullable=False)
    featurecode = db.Column(db.String(80), nullable=False)
    code = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(500), nullable=False)

    def __init__(self, featureclass, featurecode, code, name, description):
        self.featureclass = featureclass
        self.featurecode = featurecode
        self.code = '%s.%s' % (featureclass, featurecode)
        self.name = name
        self.description = description

    def __repr__(self):
        return '<Feature %r>' % self.name
