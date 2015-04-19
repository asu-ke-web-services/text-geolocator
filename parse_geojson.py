# text-geolocator/parse_geojson.py
import json


PARSE_WEIGHTS = False

UNKNOWN = "'???'"
GEOJSON = ''
with open('geolocator/sample-data/'
          'I-live-in-Phoenix-Arizona_all-geoname-hits.geojson', 'rb') as f:
    GEOJSON = f.read()

locations = dict()

djson = json.loads(GEOJSON)
for location in djson['features']:
    lat = unicode(location['geometry']['coordinates'][0])
    lon = unicode(location['geometry']['coordinates'][1])
    name = unicode(location['properties']['name'])
    countryname = unicode(location['properties']['countryname'])
    admin1name = unicode(location['properties']['admin1name'])
    admin2name = unicode(location['properties']['admin2name'])
    admin3name = unicode(location['properties']['admin3name'])
    admin4name = unicode(location['properties']['admin4name'])

    location = unicode(
        '\n\tLocationWrap(\n'
        '\t\tLocation(\n\t\t\t%s, \n\t\t\t-1, \n\t\t\t%s, \n\t\t\t%s, '
        '\n\t\t\t%s, \n\t\t\t%s, \n\t\t\t%s, \n\t\t\t%s, \n\t\t\t%s, '
        '\n\t\t\t0))' % (
            name, name, UNKNOWN, UNKNOWN, UNKNOWN, UNKNOWN, lat, lon))
    location += unicode(
        "LocationAdminNames(countryname='%s', admin1name='%s', "
        "admin2name='%s', admin3name='%s', admin4name='%s')" % (
            countryname, admin1name, admin2name, admin3name,
            admin4name))
    print location

    if name not in locations.keys():
        locations[name] = list()
    locations[name].append(location)

hits = list()

for key, value in locations.iteritems():
    hits.append(
        unicode(
            'LocationHits(%s, %s)\n' % (key, value)))

output = unicode('container = LocationHitsContainer()\n')
for hit in hits:
    output += unicode('container.append(%s)\n') % hit

with open('parsed_geojson.txt', 'w') as f:
    f.write(output.encode('UTF-8'))

print 'Operation Completed.'
