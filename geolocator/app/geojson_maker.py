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


def RemoveDuplicatesFromList(l):
	#unicode to string, assuming there will be no characters that lie outside of ascii range
	stringlist = [str(x) for x in l] 
	nodublicate_array = []
	list(set(stringlist))
	[nodublicate_array.append(item) for item in stringlist if item not in nodublicate_array]
	return nodublicate_array


def MakeGeoJsonElement(location, existing_locations):
	#lookup x in database
	lon = 0.00
	lat = 0.00

	#weight calculations
	weight = 0
	for y in existing_locations:
		if location == y:
			weight = weight + 1
	name = location

	return FeaturePoint(lon, lat, weight, name) 


def MakeGeoJsonCollection(locations):
	# --- remove duplicates
	noduplicates = RemoveDuplicatesFromList(locations)
	# --- turn locations into FeaturePoints
	feature_array = []
	for l in noduplicates:
		feature_array.append(MakeGeoJsonElement(l, locations)) 
	# --- Convert FeaturePoints List to FeatureCollection
	return geojson.FeatureCollection(feature_array)
