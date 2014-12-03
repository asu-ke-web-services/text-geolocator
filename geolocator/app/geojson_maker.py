#!/usr/bin/python
import geojson
import json
import sets

#pip install geojson
#pip install --upgrade geojson
# to test: in terminal:
	#python
	#from geojson import Point

def FeaturePoint(lon, lat, weight, name):
	geometry = { "type" : "Point", "coordinates" : [lat, lon] }
	properties = { "weight" : weight, "name" : name }
	#Feature takes in: id= "", geometry json, property json
	feature = geojson.Feature(name, geometry, properties) 
	return feature

def MakeGeoJsonElement(location, existing_locations):
	#lookup x in database
	
	#necessary imports
	##should move these to a separate file so that we can reuse them without having to rewrite them.
	from sqlalchemy import create_engine
	from sqlalchemy.orm import sessionmaker
	from models import Location
	import os

	#engine pointing to the db
	engine = create_engine(os.getenv('DATABASE_URL','postgres://postgres@{0}/app'.format(os.getenv('DB_1_PORT_5432_TCP_ADDR'))), echo=True);
	Session = sessionmaker(bind=engine)
	session = Session()

	#Gets the first hit that it gets with the given location name. It only searches the name instead of the other parameters. Also because of first hit, the accuracy is not very good. Will need to add additional logic for checking

	loc = session.query(Location).filter(Location.name == location).first()
	lon = 0.00
	lat = 0.00
	#if there is no match, the locations will be 0,0.	
	if not (loc is None):  
		lon = loc.longitude
		lat = loc.latitude

	#weight calculations
	weight = 0
	for y in existing_locations:
		if location == y :
			weight = weight + 1
			print weight
	name = location

	return FeaturePoint(lon,lat,weight,name) 
	
def MakeGeoJsonCollection(locations):
	# --- turn locations into FeaturePoints
	feature_array = []
	for l in locations:
		feature_array.append(MakeGeoJsonElement(l, locations)) 
	# --- Convert FeaturePoints List to FeatureCollection
	return geojson.FeatureCollection(feature_array )
