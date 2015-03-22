# tests/test_weighter.py
"""
run with: sudo fig run web nosetests geolocator/app/tests/test_weighter.py
"""
from app.weighter import *
import unittest
from nose.tools import nottest


class AdminNameGetterTestCase(unittest.TestCase):
    """
    Tests for app.weighter.AdminNameGetter
    """

    # ----------------------- Before/After ----------------------- #
    def setUp(self):
        """
        Executed at the start of every test
        """
        self.getter = None
        return

    def tearDown(self):
        """
        Executed at the end of every test
        """
        self.getter = None
        return

    # ----------------------- Helpers ----------------------- #
    def init(self, admincodes=LocationAdminCodes()):
        self.getter = AdminNameGetter(admincodes)
        return

    @nottest
    def test_sql_func(self, func, attribute, value):
        """
        Tests any of the AdminNameGetter's _sql_* functions

        :param function func: function to test
        :param str attribute: attribute to plug into sql
        :param str value: value to plug into sql
        """
        expected = "l.%s = '%s'" % (attribute, value)
        actual = func()
        assert expected == actual

    # ----------------------- Tests ----------------------- #
    def test__init__pass(self):
        """
        Ensures that the app.weighter.AdminNameGetter successfully initializes
        """
        CODE = LocationAdminCodes()
        CODE.admin2code = 'testing'
        self.init(CODE)
        assert isinstance(self.getter, AdminNameGetter)
        assert self.getter.codes == CODE

    def test__sql_admin4code__pass(self):
        """
        Tests AdminNameGetter._sql_admin4code
        """
        attribute = 'admin4code'
        value = 'banana'
        # make codes
        codes = LocationAdminCodes()
        codes.admin4code = value
        # init getter
        self.init(codes)
        # get func
        func = self.getter._sql_admin4code
        # run test
        self.test_sql_func(func, attribute, value)

    def test__sql_admin3code__pass(self):
        """
        Tests AdminNameGetter._sql_admin3code
        """
        attribute = 'admin3code'
        value = 'world'
        # make codes
        codes = LocationAdminCodes()
        codes.admin3code = value
        # init getter
        self.init(codes)
        # get func
        func = self.getter._sql_admin3code
        # run test
        self.test_sql_func(func, attribute, value)

    def test__sql_admin2code__pass(self):
        """
        Tests AdminNameGetter._sql_admin2code
        """
        attribute = 'admin2code'
        value = 'hello'
        # make codes
        codes = LocationAdminCodes()
        codes.admin2code = value
        # init getter
        self.init(codes)
        # get func
        func = self.getter._sql_admin2code
        # run test
        self.test_sql_func(func, attribute, value)

    def test__sql_admin1code__pass(self):
        """
        Tests AdminNameGetter._sql_admin1code
        """
        attribute = 'admin1code'
        value = 'ice cream'
        # make codes
        codes = LocationAdminCodes()
        codes.admin1code = value
        # init getter
        self.init(codes)
        # get func
        func = self.getter._sql_admin1code
        # run test
        self.test_sql_func(func, attribute, value)

    def test__sql_countrycode__pass(self):
        """
        Tests AdminNameGetter._sql_countrycode
        """
        attribute = 'countrycode'
        value = 'country 1'
        # make codes
        codes = LocationAdminCodes()
        codes.countrycode = value
        # init getter
        self.init(codes)
        # get func
        func = self.getter._sql_countrycode
        # run test
        self.test_sql_func(func, attribute, value)

    def test__sql_featurecode__pass(self):
        """
        Tests AdminNameGetter._sql_featurecode
        """
        attribute = 'featurecode'
        # init getter
        self.init()
        # get value
        INDEX = 1
        value = self.getter.ADMIN_FEATURE_CODES[1]
        # run test
        expected = "l.%s = '%s'" % (attribute, value)
        actual = self.getter._sql_featurecode(INDEX)
        assert expected == actual

    def test__countryname__pass(self):
        """
        Tests AdminNameGetter._countryname
        """
        # make codes
        codes = LocationAdminCodes()
        codes.countrycode = 'US'
        # init getter
        self.init(codes)
        expected = 'United States'
        actual = self.getter._countryname()
        print actual
        print expected
        assert expected == actual

    def test__admin1name__pass(self):
        """
        Tests AdminNameGetter._admin1name
        """
        # make codes
        codes = LocationAdminCodes()
        codes.admin1code = 'AZ'
        codes.countrycode = 'US'
        # init getter
        self.init(codes)
        expected = 'Arizona'
        actual = self.getter._admin1name()
        print actual
        print expected
        assert expected == actual


class WeightifierTestCase(unittest.TestCase):
    """
    Tests for app.weighter.Weightifier
    """

    # ----------------------- Before/After ----------------------- #
    def setUp(self):
        """
        Executed at the start of every test
        Instantiates a new instance of weighter.Weightifier()
        """
        self.weightifier = Weightifier()
        return

    def tearDown(self):
        """
        Executed at the end of every test
        """
        self.weightifier = None
        return

    # ----------------------- Helpers ----------------------- #
    def make_admin_codes_query_row(self, geonameid, name, featurecode,
                                   featureclass, countrycode=None,
                                   admin1code=None, admin2code=None,
                                   admin3code=None, admin4code=None):
        row = [geonameid, name, featurecode, featureclass]
        if countrycode is not None:
            row.append(countrycode)
        if admin1code is not None:
            row.append(admin1code)
        if admin2code is not None:
            row.append(admin2code)
        if admin3code is not None:
            row.append(admin3code)
        if admin4code is not None:
            row.append(admin4code)
        return row

    # ----------------------- Tests ----------------------- #
    def test__init__pass(self):
        """
        Ensures that the weighter.Weightifier successfully initializes
        """
        assert isinstance(self.weightifier, Weightifier)

    def test__make_admin_codes__pass_0(self):
        """
        Tests weighter.Weightifier._make_admin_codes with accuracy of 0
        """
        GEONAMEID = 5308655
        NAME = 'Phoenix'
        CODE = 'PPLA'
        CLASS = 'P'
        row = self.make_admin_codes_query_row(
            geonameid=GEONAMEID,
            name=NAME,
            featurecode=CODE,
            featureclass=CLASS)
        expected = LocationAdminCodes()
        expected.geonameid = GEONAMEID
        expected.name = NAME
        expected.featurecode = CODE
        expected.featureclass = CLASS
        actual = self.weightifier._make_admin_codes(row)
        assert expected == actual

    def test__make_admin_codes__pass_5(self):
        """
        Tests weighter.Weightifier._make_admin_codes with accuracy of 5
        """
        GEONAMEID = 5308655
        NAME = 'Phoenix'
        CODE = 'PPLA'
        CLASS = 'P'
        ADMIN4 = ''
        ADMIN3 = ''
        ADMIN2 = 'Maricopa County'
        ADMIN1 = 'Arizona'
        COUNTRY = 'United States'
        row = self.make_admin_codes_query_row(
            geonameid=GEONAMEID,
            name=NAME,
            featurecode=CODE,
            featureclass=CLASS,
            countrycode=COUNTRY,
            admin1code=ADMIN1,
            admin2code=ADMIN2,
            admin3code=ADMIN3,
            admin4code=ADMIN4)
        expected = LocationAdminCodes()
        expected.geonameid = GEONAMEID
        expected.name = NAME
        expected.featurecode = CODE
        expected.featureclass = CLASS
        expected.countrycode = COUNTRY
        expected.admin1code = ADMIN1
        expected.admin2code = ADMIN2
        expected.admin3code = ADMIN3
        expected.admin4code = ADMIN4
        actual = self.weightifier._make_admin_codes(row)
        print 'actual -> %s' % str(actual)
        print 'expected -> %s' % str(expected)
        assert expected == actual

    def test__get_admin_codes__pass(self):
        """
        """
        return
