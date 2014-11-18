from app import db
from geoalchemy2.types import Geometry

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    #location = db.Column(Geometry(geometry_type='POINT', srid=4326))
    initial_weight = db.Column(db.Float, nullable=False, default=0.0)

    def __init__(self, name, latitude, longitude, point, weight):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.point = point
        self.initial_weight = weight

    def __repr__(self):
        return '<Location %r>' % self.name
