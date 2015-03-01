import unittest

from app import geojson_maker
from app import app
from app import nlp_magic


class nlpMagicTestCase(unittest.TestCase):

    def setUp(self):
        return

    def tearDown(self):
        return

# def IsolateLocations(stanford_list):
#     """
#     Given list of Stanford NER Tagger results in the format of
#     ('name', 'type'). Filter list and retrieve only those listed
#     as 'type'='LOCATION'
#     """
#     locations = []
#     LOCATION = u'LOCATION'
#     for x in xrange(len(stanford_list)):
#         if stanford_list[x][1] == LOCATION:
#             if len(stanford_list) < (x + 1):
#                 if stanford_list[x + 1][1] == LOCATION:
#                     locations.append(stanford_list[x][0] + ' '
#                                      + stanford_list[x + 1][0])
#                     x += 1
#                 else:
#                     locations.append(stanford_list[x][0])
#     return locations

    def testIsolateLocations_BoundaryStart(self, title, completed=False):
        stanford_list = [
            ('yes1', 'LOCATION')
            ('no1', 'no'),
            ('no2', 'no'),
        ]
        result = nlp_magic.IsolateLocations(stanford_list)
        assert result == ['yes1']
