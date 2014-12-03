#!/usr/bin/python
import geojson

#pip install geojson
#pip install --upgrade geojson
# to test: in terminal:
	#python
	#from geojson import Point


def FeaturePoint(lon, lat, weight, name):
	geometry = { "type": "Point", "coordinates": [lon, lat] }
	properties = { "weight": weight, "name": name }
	#Feature takes in: id= "", geometry json, property json
	feature = geojson.Feature(name, geometry, properties) 
	return feature


def MakeGeoJsonElement(location, existing_locations):
	#lookup x in database
	lon = 0.00
	lat = 0.00

	#weight calculations
	weight = 0
	for y in existing_locations:
		if location == y:
			weight = weight + 1
			print weight
	name = location

	return FeaturePoint(lon, lat, weight, name) 


def MakeGeoJsonCollection(locations):
	# --- turn locations into FeaturePoints
	feature_array = []
	for l in locations:
		feature_array.append(MakeGeoJsonElement(l, locations)) 
	# --- Convert FeaturePoints List to FeatureCollection
	return geojson.FeatureCollection(feature_array )
