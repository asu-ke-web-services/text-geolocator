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
    lat = location['geometry']['coordinates'][0]
    lon = location['geometry']['coordinates'][1]
    name = location['properties']['name']
    countryname = location['properties']['countryname']
    admin1name = location['properties']['admin1name']
    admin2name = location['properties']['admin2name']
    admin3name = location['properties']['admin3name']
    admin4name = location['properties']['admin4name']

    adminnames = unicode(
        "LocationAdminNames(\n\t\t\tcountryname='%s',"
        "\n\t\t\tadmin1name='%s',"
        "\n\t\t\tadmin2name='%s',\n\t\t\tadmin3name='%s',"
        "\n\t\t\tadmin4name='%s')" % (
            unicode(countryname), unicode(admin1name), unicode(admin2name),
            unicode(admin3name), unicode(admin4name)))
    location = unicode(
        '\n\tLocationWrap(\n'
        '\t\tLocation(\n\t\t\t%s,\n\t\t\t-1,\n\t\t\t%s,\n\t\t\t%s,'
        '\n\t\t\t%s,\n\t\t\t%s,\n\t\t\t%s,\n\t\t\t%s,\n\t\t\t%s,'
        '\n\t\t\t0),\n\t\tadminnames=%s),' % (
            unicode(name), unicode(name), UNKNOWN, UNKNOWN, UNKNOWN, UNKNOWN,
            unicode(lat), unicode(lon), unicode(adminnames))).encode(
        'ascii', 'ignore')
    # print location

    if name not in locations.keys():
        locations[name] = ''
    locations[name] += location

hits = list()

for key, value in locations.iteritems():
    hits.append(
        unicode(
            "LocationHits('%s', [%s])\n" % (unicode(key), value)))

output = unicode('container = LocationHitsContainer()\n')
for hit in hits:
    output += unicode('container.append(%s)\n') % unicode(hit)

with open('parsed_geojson.txt', 'w') as f:
    f.write(output.encode('UTF-8'))

print 'Operation Completed.'
