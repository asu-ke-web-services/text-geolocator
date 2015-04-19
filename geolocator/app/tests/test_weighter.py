# tests/test_weighter.py
"""
run with: sudo fig run web nosetests geolocator/app/tests/test_weighter.py
"""
from app.weighter import *
from app.geolocator import *
import unittest
from sqlalchemy import text
from nose.tools import nottest


class LocationAdminNamesTestCase(unittest.TestCase):
    """
    Tests app.weighter.LocationAdminNames
    """

    # ----------------------- Before/After ----------------------- #
    def setUp(self):
        """
        Executed at the start of every test
        Instantiates a new instance of weighter.LocationAdminNames()
        """
        self.names = LocationAdminNames()
        return

    def tearDown(self):
        """
        Executed at the end of every test
        """
        self.names = None
        return

    # ----------------------- Helpers ----------------------- #

    # ----------------------- Tests ----------------------- #
    def test__init__pass(self):
        """
        Ensures that the weighter.LocationAdminNames successfully initializes
        """
        assert isinstance(self.names, LocationAdminNames)
        assert self.names.geonameid == -1
        assert self.names.name is None
        assert self.names.admin4name is None
        assert self.names.admin3name is None
        assert self.names.admin2name is None
        assert self.names.admin1name is None
        assert self.names.countryname is None

    def test__list__pass(self):
        """
        Tests app.weighter.LocationAdminNames.list
        """
        expected = ['May', 'the', 'Force', 'be', 'with you!']
        self.names.admin4name = expected[0]
        self.names.admin3name = expected[1]
        self.names.admin2name = expected[2]
        self.names.admin1name = expected[3]
        self.names.countryname = expected[4]
        actual = self.names.list()
        assert expected == actual

    def test__match__admin1name(self):
        """
        Tests app.weighter.LocationAdminNames.match where name matches
        admin1name
        """
        NAME = 'Taiwan'
        self.names.admin1name = NAME
        assert self.names.match(NAME)

    def test__match__admin2name(self):
        """
        Tests app.weighter.LocationAdminNames.match where name matches
        admin2name
        """
        NAME = 'Yellow'
        self.names.admin1name = NAME
        assert self.names.match(NAME)

    def test__match__admin3name(self):
        """
        Tests app.weighter.LocationAdminNames.match where name matches
        admin3name
        """
        NAME = 'Blue'
        self.names.admin1name = NAME
        assert self.names.match(NAME)

    def test__match__admin4name(self):
        """
        Tests app.weighter.LocationAdminNames.match where name matches
        admin4name
        """
        NAME = 'Red'
        self.names.admin1name = NAME
        assert self.names.match(NAME)

    def test__match__countryname(self):
        """
        Tests app.weighter.LocationAdminNames.match where name matches
        countryname
        """
        NAME = 'China'
        self.names.admin1name = NAME
        assert self.names.match(NAME)

    def test__eq__pass(self):
        """
        Tests app.weighter.LocationAdminNames.__eq__ with two equal objects
        """
        A4 = 'apple'
        A2 = 'peanut butter'
        NAME = 'Joe'
        c1 = LocationAdminNames()
        c1.admin4name = A4
        c1.admin2name = A2
        c1.name = NAME
        c2 = LocationAdminNames()
        c2.admin4name = A4
        c2.admin2name = A2
        c2.name = NAME
        assert c1 == c2

    def test__eq__fail(self):
        """
        Tests app.weighter.LocationAdminNames.__eq__ with two different objects
        """
        A4 = 'apple'
        A2 = 'peanut butter'
        NAME = 'Frank'
        c1 = LocationAdminNames()
        c1.admin4name = A4
        c1.admin2name = A2
        c1.name = 'Joe'
        c2 = LocationAdminNames()
        c2.admin4name = A4
        c2.admin2name = A2
        c2.name = NAME
        assert c1 != c2

    def test__repr__good(self):
        """
        Tests app.weighter.LocationAdminNames.__repr__
        """
        self.names.name = 'Banana'
        self.names.countryname = 'United States'
        self.names.admin3name = 'Apple'
        # test if any exceptions fire
        s = self.names.__repr__()
        assert s is not None
        assert isinstance(s, str)


class LocationAdminCodesTestCase(unittest.TestCase):
    """
    Tests app.weighter.LocationAdminCodes
    """

    # ----------------------- Before/After ----------------------- #
    def setUp(self):
        """
        Executed at the start of every test
        Instantiates a new instance of weighter.LocationAdminCodes()
        """
        self.codes = LocationAdminCodes()
        return

    def tearDown(self):
        """
        Executed at the end of every test
        """
        self.codes = None
        return

    # ----------------------- Helpers ----------------------- #

    # ----------------------- Tests ----------------------- #
    def test__init__pass(self):
        """
        Ensures that the weighter.LocationAdminCodes successfully initializes
        """
        assert isinstance(self.codes, LocationAdminCodes)
        assert self.codes.geonameid == -1
        assert self.codes.name is None
        assert self.codes.featurecode is None
        assert self.codes.featureclass is None
        assert self.codes.admin4code is None
        assert self.codes.admin3code is None
        assert self.codes.admin2code is None
        assert self.codes.admin1code is None
        assert self.codes.countrycode is None

    def test__eq__pass(self):
        """
        Tests app.weighter.LocationAdminCodes.__eq__ with two equal objects
        """
        A4 = 'apple'
        A2 = 'peanut butter'
        FC = '5'
        NAME = 'Joe'
        c1 = LocationAdminCodes()
        c1.admin4code = A4
        c1.admin2code = A2
        c1.featurecode = FC
        c1.name = NAME
        c2 = LocationAdminCodes()
        c2.admin4code = A4
        c2.admin2code = A2
        c2.featurecode = FC
        c2.name = NAME
        assert c1 == c2

    def test__eq__fail(self):
        """
        Tests app.weighter.LocationAdminCodes.__eq__ with two different objects
        """
        A4 = 'apple'
        A2 = 'peanut butter'
        FC = '5'
        NAME = 'Joe'
        c1 = LocationAdminCodes()
        c1.admin4code = A4
        c1.admin2code = A4
        c1.featurecode = FC
        c1.name = FC
        c2 = LocationAdminCodes()
        c2.admin4code = A2
        c2.admin2code = A4
        c2.featurecode = NAME
        c2.name = NAME
        assert c1 != c2

    def test__repr__good(self):
        """
        Tests app.weighter.LocationAdminCodes.__repr__
        """
        self.codes.name = 'Banana'
        self.codes.featurecode = 'PPL'
        self.codes.featureclass = 'P'
        self.codes.countrycode = 'US'
        # test if any exceptions fire
        s = self.codes.__repr__()
        assert s is not None
        assert isinstance(s, str)


class QueryTestCase(unittest.TestCase):
    """
    Tests app.weighter.Query
    """

    # ----------------------- Before/After ----------------------- #
    def setUp(self):
        self.basic_query = self.init_basic()
        return

    def tearDown(self):
        self.db = None
        return

    # ----------------------- Helpers ----------------------- #
    def init_basic(self):
        return Query(selects=[], froms=[], wheres=[])

    # ----------------------- Tests ----------------------- #
    def test__init__success(self):
        """
        successful initialization
        """
        list1 = [1, 2, 3]
        list2 = ['fea', 'gagea', 'afeagt3']
        # --- 1 ---
        q = Query(selects=list1, froms=list2)
        assert q.selects == list1
        assert q.froms == list2
        assert q.wheres is None
        # --- 2 ---
        q = Query(selects=list1, froms=list2, wheres=list1)
        assert q.selects == list1
        assert q.froms == list2
        assert q.wheres == list1

    def test__init__no_list(self):
        """
        selects should be a list
        froms should be list
        wheres should be None or list
        """
        not_a_list = 1
        list1 = ['test list1', 'banana', 'apple']
        list2 = ['test list2', 'orange']
        self.assertRaises(TypeError, Query, not_a_list, list2, list1)
        self.assertRaises(TypeError, Query, list1, not_a_list, list2)
        self.assertRaises(TypeError, Query, list1, list2, not_a_list)
        q = Query(selects=list1, froms=list2, wheres=None)
        assert q.wheres is None

    def test__expand_list__success(self):
        result = self.basic_query.expand_list(['1', '2', '3', '4'])
        assert result == '1, 2, 3, 4'

    def test__expand_list__empty_list(self):
        result = self.basic_query.expand_list([])
        assert result == ''

    def test__expand_list__none_param(self):
        result = self.basic_query.expand_list(None)
        assert result == ''

    def test__expand_list__no_params(self):
        self.assertRaises(TypeError, self.basic_query.expand_list)

    def test__expand_list__list_of_length_1(self):
        result = self.basic_query.expand_list('1')
        assert result == '1'

    def test__expand_list__3_params(self):
        self.assertRaises(
            TypeError,
            self.basic_query.expand_list, ['1', '2'], 'param2', 'param3')

    def test__expand_list__unique_separator(self):
        result = self.basic_query.expand_list(['1', '2', '3', '4'], '--- ')
        assert result == '1--- 2--- 3--- 4'

    def test__expand_list__none_separator(self):
        result = self.basic_query.expand_list(['1', '2', '3', '4'], None)
        assert result == '1234'

    def test__expand_list__empty_separator(self):
        result = self.basic_query.expand_list(['1', '2', '3', '4'], '')
        assert result == '1234'

    def test__add_sql__success(self):
        s1 = 'With a love like that'
        s2 = 'You know should be glad!'
        self.basic_query._add_sql(s1)
        assert self.basic_query.sql == s1
        self.basic_query._add_sql(s2)
        assert self.basic_query.sql == (s1 + ' ' + s2)

    def test__add_sql__empty(self):
        s1 = ''
        self.basic_query._add_sql(s1)
        assert self.basic_query.sql == s1
        self.basic_query._add_sql(s1)
        assert self.basic_query.sql == ''

    def test__add_sql__none_param(self):
        self.assertRaises(TypeError, self.basic_query._add_sql, None)

    def test__add_sql__no_params(self):
        self.assertRaises(TypeError, self.basic_query._add_sql)

    def test__add_sql__two_params(self):
        self.assertRaises(
            TypeError,
            self.basic_query._add_sql, 'param1', 'param2')

    def test__to_sql__success_with_wheres(self):
        SELECTS = ['s0', 's1']
        FROMS = ['f0', 'f1']
        WHERES = ['w0=w1', 'w1<=2']
        q = Query(selects=SELECTS, froms=FROMS, wheres=WHERES)
        expected = (
            'select %s, %s from %s, %s where %s AND %s'
            % (SELECTS[0], SELECTS[1], FROMS[0], FROMS[1], WHERES[0],
               WHERES[1]))
        expected = text(expected)
        actual = q.to_sql()
        assert expected.text == actual.text

    def test__to_sql__success_without_wheres(self):
        SELECTS = ['s0', 's1']
        FROMS = ['f0', 'f1']
        q = Query(selects=SELECTS, froms=FROMS)
        expected = (
            'select %s, %s from %s, %s'
            % (SELECTS[0], SELECTS[1], FROMS[0], FROMS[1]))
        expected = text(expected)
        actual = q.to_sql()
        assert expected.text == actual.text

    def test__repr__(self):
        """
        Tests Query.__repr__
        """
        q = Query(selects=['selects1, selects2'], froms=['from1', 'from2'])
        try:
            print q
        except Exception, e:
            print '__repr__ resulted in Exception:%s' % (str(e))
            assert False
        else:
            assert True


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

    def test__admin2name__pass(self):
        """
        Tests AdminNameGetter._admin2name
        """
        # make codes
        codes = LocationAdminCodes()
        codes.admin4code = '8658294'
        codes.admin3code = '8644152'
        codes.admin2code = 'D8'
        codes.admin1code = 'C'
        codes.countrycode = 'UG'
        # init getter
        self.init(codes)
        expected = 'Mityana District'
        actual = self.getter._admin2name()
        print actual
        print expected
        assert expected == actual

    def test__admin3name__pass(self):
        """
        Tests AdminNameGetter._admin3name
        """
        # make codes
        codes = LocationAdminCodes()
        codes.admin4code = '8658294'
        codes.admin3code = '8644152'
        codes.admin2code = 'D8'
        codes.admin1code = 'C'
        codes.countrycode = 'UG'
        # init getter
        self.init(codes)
        expected = 'Mityana'
        actual = self.getter._admin3name()
        print actual
        print expected
        assert expected == actual

    def test__admin4name__pass(self):
        """
        Tests AdminNameGetter._admin4name
        """
        # make codes
        codes = LocationAdminCodes()
        codes.admin4code = '8658294'
        codes.admin3code = '8644152'
        codes.admin2code = 'D8'
        codes.admin1code = 'C'
        codes.countrycode = 'UG'
        # init getter
        self.init(codes)
        expected = 'Mityana Town Council'
        actual = self.getter._admin4name()
        print actual
        print expected
        assert expected == actual

    def test__adminnames__pass_acc3(self):
        """
        Tests AdminNameGetter.adminnames with accuracy of 3
        """
        ADM2 = '237'
        ADM1 = 'GA'
        COCO = 'US'
        codes = LocationAdminCodes()
        codes.featurecode = 'PPL'
        codes.featureclass = 'P'
        codes.featureclass = 'P'
        codes.admin4code = None
        codes.admin3code = None
        codes.admin2code = ADM2
        codes.admin1code = ADM1
        codes.countrycode = COCO
        self.init(codes)
        expected = LocationAdminNames()
        expected.admin4name = None
        expected.admin3name = None
        expected.admin2name = 'Putnam County'
        expected.admin1name = 'Georgia'
        expected.countryname = 'United States'
        actual = self.getter.adminnames()
        print 'expected -> ' + str(expected)
        print 'actual -> ' + str(actual)
        assert expected == actual

    def test__adminnames__pass_acc5(self):
        """
        Tests AdminNameGetter.adminnames with accuracy of 5
        """
        codes = LocationAdminCodes()
        codes.featurecode = 'PPL'
        codes.featureclass = 'P'
        codes.featureclass = 'P'
        codes.admin4code = '8658294'
        codes.admin3code = '8644152'
        codes.admin2code = 'D8'
        codes.admin1code = 'C'
        codes.countrycode = 'UG'
        self.init(codes)
        expected = LocationAdminNames()
        expected.admin4name = "Mityana Town Council"
        expected.admin3name = 'Mityana'
        expected.admin2name = 'Mityana District'
        expected.admin1name = 'Central Region'
        expected.countryname = 'Uganda'
        actual = self.getter.adminnames()
        print 'expected -> ' + str(expected)
        print 'actual -> ' + str(actual)
        assert expected == actual

    def test__repr__(self):
        """
        Tests AdminNameGetter.__repr__
        """
        ADM2 = '237'
        ADM1 = 'GA'
        COCO = 'US'
        codes = LocationAdminCodes()
        codes.featurecode = 'PPL'
        codes.featureclass = 'P'
        codes.featureclass = 'P'
        codes.admin4code = None
        codes.admin3code = None
        codes.admin2code = ADM2
        codes.admin1code = ADM1
        codes.countrycode = COCO
        self.init(codes)
        # test if any exceptions fire
        s = self.getter.__repr__()
        assert s is not None
        assert isinstance(s, str)


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

    def test__make_sql__pass(self):
        """
        Tests Weightifier._make_sql
        """
        selects = "o.orange, a.apple, b.banana"
        fromm = "FROM orange o, apple a, banana b"
        where = "o.orange == a.apple"
        expected = text(selects + '\n' + fromm + '\n' + where)
        actual = self._make_sql(selects, fromm, where)
        assert expected.text == actual.text

    def test__make_admin_codes_query__acc1(self):
        """
        Tests Weightifier._make_admin_codes_query with accuracy of 1
        """
        geonameid = 9001
        query = ("SELECT l.geonameid, l.name, l.featurecode, l.featureclass, "
                 "l.countrycode, "
                 "\nFROM raw_locations l\n"
                 "WHERE l.geonameid = '%s'" % str(geonameid))
        expected = text(query)
        actual = self._make_admin_codes_query(geonameid, 1)
        assert expected.text == actual.text

    def test__make_admin_codes_query__acc2(self):
        """
        Tests Weightifier._make_admin_codes_query with accuracy of 2
        """
        geonameid = 9001
        query = ("SELECT l.geonameid, l.name, l.featurecode, l.featureclass, "
                 "l.countrycode, l.admin1code, "
                 "\nFROM raw_locations l\n"
                 "WHERE l.geonameid = '%s'" % str(geonameid))
        expected = text(query)
        actual = self._make_admin_codes_query(geonameid, 2)
        assert expected.text == actual.text

    def test__make_admin_codes_query__acc3(self):
        """
        Tests Weightifier._make_admin_codes_query with accuracy of 3
        """
        geonameid = 9001
        query = ("SELECT l.geonameid, l.name, l.featurecode, l.featureclass, "
                 "l.countrycode, l.admin1code, l.admin2code, "
                 "\nFROM raw_locations l\n"
                 "WHERE l.geonameid = '%s'" % str(geonameid))
        expected = text(query)
        actual = self._make_admin_codes_query(geonameid, 3)
        assert expected.text == actual.text

    def test__make_admin_codes_query__acc4(self):
        """
        Tests Weightifier._make_admin_codes_query with accuracy of 4
        """
        geonameid = 9001
        query = ("SELECT l.geonameid, l.name, l.featurecode, l.featureclass, "
                 "l.countrycode, l.admin1code, l.admin2code, l.admin3code, "
                 "\nFROM raw_locations l\n"
                 "WHERE l.geonameid = '%s'" % str(geonameid))
        expected = text(query)
        actual = self._make_admin_codes_query(geonameid, 4)
        assert expected.text == actual.text

    def test__make_admin_codes_query__acc5(self):
        """
        Tests Weightifier._make_admin_codes_query with accuracy of 5
        """
        geonameid = 9001
        query = ("SELECT l.geonameid, l.name, l.featurecode, l.featureclass, "
                 "l.countrycode, l.admin1code, l.admin2code, l.admin3code, "
                 "l.admin4code\nFROM raw_locations l\n"
                 "WHERE l.geonameid = '%s'" % str(geonameid))
        expected = text(query)
        actual = self._make_admin_codes_query(geonameid, 5)
        assert expected.text == actual.text

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
        Tests weighter.Weightifier._get_admin_codes with accuracy of 5
        """
        expected = LocationAdminCodes()
        expected.geonameid = '8658294'
        expected.name = 'Mityana Town Council'
        expected.featurecode = 'ADM4'
        expected.featureclass = 'A'
        expected.admin4code = '8658294'
        expected.admin3code = '8644152'
        expected.admin2code = 'D8'
        expected.admin1code = 'C'
        expected.countrycode = 'UG'
        actual = self.weightifier._get_admin_codes(8658294, 5)
        print expected
        print actual
        assert expected == actual

    def test__get_admin_names__pass(self):
        """
        Tests weighter.Weightifier._get_admin_names with accuracy of 5
        """
        codes = LocationAdminCodes()
        codes.admin4code = '8658294'
        codes.admin3code = '8644152'
        codes.admin2code = 'D8'
        codes.admin1code = 'C'
        codes.countrycode = 'UG'
        expected = LocationAdminNames()
        expected.admin4name = "Mityana Town Council"
        expected.admin3name = 'Mityana'
        expected.admin2name = 'Mityana District'
        expected.admin1name = 'Central Region'
        expected.countryname = 'Uganda'
        actual = self.weightifier._get_admin_names(codes)
        assert expected == actual

    def test__gather_all_names__pass(self):
        """
        Tests weighter._gather_all_names with accuracy of 4
        """
        # container has None for all admin names
        # container = LocationHitsContainer()
        # container.append(LocationHits('Arizona', [
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             -35.72259,
        #             -65.31972,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             -23.11667,
        #             149.2,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             -21.66667,
        #             141.55,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             -19.53333,
        #             141.35001,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             -30.48236,
        #             116.867,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             -34.53529,
        #             117.88443,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             -33.30794,
        #             118.66646,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             -32.49089,
        #             151.40037,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             -35.0347,
        #             146.52509,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             -8.66667,
        #             -40.95,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             -6.45,
        #             -41.58333,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             -5.56667,
        #             -35.78333,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             -5.28333,
        #             -35.7,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             -16.21667,
        #             -40.06667,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             -12.8,
        #             -40.93333,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             -8.68222,
        #             -40.96139,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             -8.75436,
        #             -40.91927,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             49.82832,
        #             -99.02859,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             -24.58333,
        #             -70.0,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             -30.4,
        #             -70.16667,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             10.57197,
        #             -74.13696,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             10.48333,
        #             -75.43333,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             4.04375,
        #             -72.96845,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             2.72084,
        #             -72.28228,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             6.81806,
        #             -70.76,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             5.97167,
        #             -71.81694,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             5.93889,
        #             -70.97944,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             2.17809,
        #             -74.5573,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             3.32008,
        #             -73.50162,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             10.36374,
        #             -73.48162,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             10.19707,
        #             -84.95201,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             27.79,
        #             -15.7,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             13.95806,
        #             -90.82028,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             15.63333,
        #             -87.31667,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             15.68333,
        #             -87.33333,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             44.13157,
        #             12.48532,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             20.91744,
        #             -87.46447,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             30.45639,
        #             -109.46373,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             22.9128,
        #             -99.11055,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             17.03278,
        #             -92.34472,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             15.62028,
        #             -93.18833,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             21.42886,
        #             -87.70516,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             -23.2,
        #             16.03333,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             -27.73333,
        #             19.8,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             32.78904,
        #             -92.95766,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             30.78963,
        #             -95.468,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             41.81443,
        #             -96.13363,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             34.5003,
        #             -111.50098,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             -25.92325,
        #             22.79326,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             -19.21667,
        #             29.61667,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             -18.19478,
        #             31.63905,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Arizona',
        #             -1,
        #             'Arizona',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             -17.85918,
        #             31.98619,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None'))])
        # )
        # container.append(LocationHits('Phoenix', [
        #     LocationWrap(
        #         Location(
        #             'Phoenix',
        #             -1,
        #             'Phoenix',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             -34.96862,
        #             139.18517,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Phoenix',
        #             -1,
        #             'Phoenix',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             49.09979,
        #             -118.58562,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Phoenix',
        #             -1,
        #             'Phoenix',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             37.78651,
        #             20.89943,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Phoenix',
        #             -1,
        #             'Phoenix',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             6.90348,
        #             -58.45244,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Phoenix',
        #             -1,
        #             'Phoenix',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             6.46198,
        #             -57.64923,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Phoenix',
        #             -1,
        #             'Phoenix',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             -7.78178,
        #             110.37814,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Phoenix',
        #             -1,
        #             'Phoenix',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             18.42516,
        #             -77.72388,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Phoenix',
        #             -1,
        #             'Phoenix',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             18.36667,
        #             -78.28333,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Phoenix',
        #             -1,
        #             'Phoenix',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             35.09843,
        #             129.02964,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Phoenix',
        #             -1,
        #             'Phoenix',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             -20.28667,
        #             57.50222,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Phoenix',
        #             -1,
        #             'Phoenix',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             46.20074,
        #             21.28622,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Phoenix',
        #             -1,
        #             'Phoenix',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             1.30082,
        #             103.84015,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Phoenix',
        #             -1,
        #             'Phoenix',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             33.36597,
        #             -83.27766,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Phoenix',
        #             -1,
        #             'Phoenix',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             29.64605,
        #             -89.93979,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Phoenix',
        #             -1,
        #             'Phoenix',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             39.51649,
        #             -76.61608,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Phoenix',
        #             -1,
        #             'Phoenix',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             32.58125,
        #             -90.56287,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Phoenix',
        #             -1,
        #             'Phoenix',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             34.2935,
        #             -78.05833,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Phoenix',
        #             -1,
        #             'Phoenix',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             34.07735,
        #             -82.11095,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Phoenix',
        #             -1,
        #             'Phoenix',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             29.3819,
        #             -98.54168,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Phoenix',
        #             -1,
        #             'Phoenix',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             41.61115,
        #             -87.63477,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Phoenix',
        #             -1,
        #             'Phoenix',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             47.38881,
        #             -88.27761,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Phoenix',
        #             -1,
        #             'Phoenix',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             40.47788,
        #             -74.31293,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Phoenix',
        #             -1,
        #             'Phoenix',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             40.52983,
        #             -74.34098,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Phoenix',
        #             -1,
        #             'Phoenix',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             43.23118,
        #             -76.30076,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Phoenix',
        #             -1,
        #             'Phoenix',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             33.44838,
        #             -112.07404,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Phoenix',
        #             -1,
        #             'Phoenix',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             39.92689,
        #             -112.1105,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Phoenix',
        #             -1,
        #             'Phoenix',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             42.27541,
        #             -122.81809,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Phoenix',
        #             -1,
        #             'Phoenix',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             -29.71667,
        #             31.01667,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Phoenix',
        #             -1,
        #             'Phoenix',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             -29.70428,
        #             30.9761,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Phoenix',
        #             -1,
        #             'Phoenix',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             -26.07098,
        #             29.20451,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Phoenix',
        #             -1,
        #             'Phoenix',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             -28.3,
        #             26.81667,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Phoenix',
        #             -1,
        #             'Phoenix',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             -25.71076,
        #             23.04885,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None')),
        #     LocationWrap(
        #         Location(
        #             'Phoenix',
        #             -1,
        #             'Phoenix',
        #             '???',
        #             '???',
        #             '???',
        #             '???',
        #             -16.71667,
        #             29.78333,
        #             0),
        #         adminnames=LocationAdminNames(
        #             countryname='None',
        #             admin1name='None',
        #             admin2name='None',
        #             admin3name='None',
        #             admin4name='None'))])
        # )
        # expected has expected admin names (of accuracy 4)
        # with locations "Arizona" and "Phoenix"
        expected = LocationHitsContainer()
        expected.append(LocationHits('Arizona', [
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    -35.72259,
                    -65.31972,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Argentina',
                    admin1name='Provincia de San Luis',
                    admin2name='None',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    -23.11667,
                    149.2,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Australia',
                    admin1name='State of Queensland',
                    admin2name='Central Highlands',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    -21.66667,
                    141.55,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Australia',
                    admin1name='State of Queensland',
                    admin2name='McKinlay',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    -19.53333,
                    141.35001,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Australia',
                    admin1name='State of Queensland',
                    admin2name='McKinlay',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    -30.48236,
                    116.867,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Australia',
                    admin1name='State of Western Australia',
                    admin2name='Dalwallinu',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    -34.53529,
                    117.88443,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Australia',
                    admin1name='State of Western Australia',
                    admin2name='Plantagenet Shire',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    -33.30794,
                    118.66646,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Australia',
                    admin1name='State of Western Australia',
                    admin2name='Lake Grace',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    -32.49089,
                    151.40037,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Australia',
                    admin1name='State of New South Wales',
                    admin2name='Singleton',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    -35.0347,
                    146.52509,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Australia',
                    admin1name='State of New South Wales',
                    admin2name='Urana',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    -8.66667,
                    -40.95,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Brazil',
                    admin1name='Pernambuco',
                    admin2name='Afrnio',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    -6.45,
                    -41.58333,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Brazil',
                    admin1name='Piau',
                    admin2name='Lagoa do Stio',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    -5.56667,
                    -35.78333,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Brazil',
                    admin1name='Rio Grande do Norte',
                    admin2name='Joo Cmara',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    -5.28333,
                    -35.7,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Brazil',
                    admin1name='Rio Grande do Norte',
                    admin2name='Touros',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    -16.21667,
                    -40.06667,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Brazil',
                    admin1name='Minas Gerais',
                    admin2name='Salto da Divisa',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    -12.8,
                    -40.93333,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Brazil',
                    admin1name='Bahia',
                    admin2name='Boa Vista do Tupim',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    -8.68222,
                    -40.96139,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Brazil',
                    admin1name='Pernambuco',
                    admin2name='Afrnio',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    -8.75436,
                    -40.91927,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Brazil',
                    admin1name='Pernambuco',
                    admin2name='Afrnio',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    49.82832,
                    -99.02859,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Canada',
                    admin1name='Manitoba',
                    admin2name='None',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    -24.58333,
                    -70.0,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Chile',
                    admin1name='Antofagasta',
                    admin2name='Provincia de Antofagasta',
                    admin3name='Antofagasta',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    -30.4,
                    -70.16667,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Chile',
                    admin1name='Coquimbo',
                    admin2name='Provincia de Elqui',
                    admin3name='Paihuano',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    10.57197,
                    -74.13696,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Colombia',
                    admin1name='Departamento del Magdalena',
                    admin2name='None',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    10.48333,
                    -75.43333,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Colombia',
                    admin1name='Departamento de Bolvar',
                    admin2name='None',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    4.04375,
                    -72.96845,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Colombia',
                    admin1name='Departamento del Meta',
                    admin2name='None',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    2.72084,
                    -72.28228,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Colombia',
                    admin1name='Departamento del Guaviare',
                    admin2name='None',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    6.81806,
                    -70.76,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Colombia',
                    admin1name='Departamento de Arauca',
                    admin2name='None',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    5.97167,
                    -71.81694,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Colombia',
                    admin1name='Departamento de Casanare',
                    admin2name='None',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    5.93889,
                    -70.97944,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Colombia',
                    admin1name='Departamento de Casanare',
                    admin2name='None',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    2.17809,
                    -74.5573,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Colombia',
                    admin1name='Departamento del Meta',
                    admin2name='None',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    3.32008,
                    -73.50162,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Colombia',
                    admin1name='Departamento del Meta',
                    admin2name='None',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    10.36374,
                    -73.48162,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Colombia',
                    admin1name='Departamento del Cesar',
                    admin2name='None',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    10.19707,
                    -84.95201,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Costa Rica',
                    admin1name='Provincia de Guanacaste',
                    admin2name='None',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    27.79,
                    -15.7,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Spain',
                    admin1name='Canary Islands',
                    admin2name='Provincia de Las Palmas',
                    admin3name='Mogn',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    13.95806,
                    -90.82028,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Guatemala',
                    admin1name='Departamento de Escuintla',
                    admin2name='None',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    15.63333,
                    -87.31667,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Honduras',
                    admin1name='Departamento de Atlntida',
                    admin2name='None',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    15.68333,
                    -87.33333,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Honduras',
                    admin1name='Departamento de Atlntida',
                    admin2name='Arizona',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    44.13157,
                    12.48532,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Italy',
                    admin1name='Emilia-Romagna',
                    admin2name='Provincia di Rimini',
                    admin3name='Bellaria-Igea Marina',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    20.91744,
                    -87.46447,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Mexico',
                    admin1name='Estado de Quintana Roo',
                    admin2name='None',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    30.45639,
                    -109.46373,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Mexico',
                    admin1name='Estado de Sonora',
                    admin2name='None',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    22.9128,
                    -99.11055,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Mexico',
                    admin1name='Estado de Tamaulipas',
                    admin2name='None',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    17.03278,
                    -92.34472,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Mexico',
                    admin1name='Estado de Chiapas',
                    admin2name='Sital',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    15.62028,
                    -93.18833,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Mexico',
                    admin1name='Estado de Chiapas',
                    admin2name='Pijijiapan',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    21.42886,
                    -87.70516,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Mexico',
                    admin1name='Estado de Yucatn',
                    admin2name='None',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    -23.2,
                    16.03333,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Namibia',
                    admin1name='Khomas',
                    admin2name='None',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    -27.73333,
                    19.8,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Namibia',
                    admin1name='Karas',
                    admin2name='None',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    32.78904,
                    -92.95766,
                    0),
                adminnames=LocationAdminNames(
                    countryname='United States',
                    admin1name='Louisiana',
                    admin2name='Claiborne Parish',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    30.78963,
                    -95.468,
                    0),
                adminnames=LocationAdminNames(
                    countryname='United States',
                    admin1name='Texas',
                    admin2name='Walker County',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    41.81443,
                    -96.13363,
                    0),
                adminnames=LocationAdminNames(
                    countryname='United States',
                    admin1name='Nebraska',
                    admin2name='Burt County',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    34.5003,
                    -111.50098,
                    0),
                adminnames=LocationAdminNames(
                    countryname='United States',
                    admin1name='Arizona',
                    admin2name='None',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    -25.92325,
                    22.79326,
                    0),
                adminnames=LocationAdminNames(
                    countryname='South Africa',
                    admin1name='Province of North West',
                    admin2name='Dr Ruth Segomotsi Mompati District'
                               ' Municipality',
                    admin3name='Kagisano/Molopo',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    -19.21667,
                    29.61667,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Zimbabwe',
                    admin1name='None',
                    admin2name='None',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    -18.19478,
                    31.63905,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Zimbabwe',
                    admin1name='Mashonaland East Province',
                    admin2name='None',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Arizona',
                    -1,
                    'Arizona',
                    '???',
                    '???',
                    '???',
                    '???',
                    -17.85918,
                    31.98619,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Zimbabwe',
                    admin1name='Mashonaland East Province',
                    admin2name='None',
                    admin3name='None',
                    admin4name='None'))])
        )
        expected.append(LocationHits('Phoenix', [
            LocationWrap(
                Location(
                    'Phoenix',
                    -1,
                    'Phoenix',
                    '???',
                    '???',
                    '???',
                    '???',
                    -34.96862,
                    139.18517,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Australia',
                    admin1name='State of South Australia',
                    admin2name='Mid Murray',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Phoenix',
                    -1,
                    'Phoenix',
                    '???',
                    '???',
                    '???',
                    '???',
                    49.09979,
                    -118.58562,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Canada',
                    admin1name='British Columbia',
                    admin2name='None',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Phoenix',
                    -1,
                    'Phoenix',
                    '???',
                    '???',
                    '???',
                    '???',
                    37.78651,
                    20.89943,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Greece',
                    admin1name='Ionian Islands',
                    admin2name='Noms Zaknthou',
                    admin3name='Dimos Zakynthos',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Phoenix',
                    -1,
                    'Phoenix',
                    '???',
                    '???',
                    '???',
                    '???',
                    6.90348,
                    -58.45244,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Guyana',
                    admin1name='Essequibo Islands-West Demerara Region',
                    admin2name='None',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Phoenix',
                    -1,
                    'Phoenix',
                    '???',
                    '???',
                    '???',
                    '???',
                    6.46198,
                    -57.64923,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Guyana',
                    admin1name='Mahaica-Berbice Region',
                    admin2name='None',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Phoenix',
                    -1,
                    'Phoenix',
                    '???',
                    '???',
                    '???',
                    '???',
                    -7.78178,
                    110.37814,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Indonesia',
                    admin1name='Daerah Istimewa Yogyakarta',
                    admin2name='None',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Phoenix',
                    -1,
                    'Phoenix',
                    '???',
                    '???',
                    '???',
                    '???',
                    18.42516,
                    -77.72388,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Jamaica',
                    admin1name='Parish of Trelawny',
                    admin2name='None',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Phoenix',
                    -1,
                    'Phoenix',
                    '???',
                    '???',
                    '???',
                    '???',
                    18.36667,
                    -78.28333,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Jamaica',
                    admin1name='Parish of Hanover',
                    admin2name='None',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Phoenix',
                    -1,
                    'Phoenix',
                    '???',
                    '???',
                    '???',
                    '???',
                    35.09843,
                    129.02964,
                    0),
                adminnames=LocationAdminNames(
                    countryname='South Korea',
                    admin1name='Busan',
                    admin2name='None',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Phoenix',
                    -1,
                    'Phoenix',
                    '???',
                    '???',
                    '???',
                    '???',
                    -20.28667,
                    57.50222,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Mauritius',
                    admin1name='Plaines Wilhems District',
                    admin2name='None',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Phoenix',
                    -1,
                    'Phoenix',
                    '???',
                    '???',
                    '???',
                    '???',
                    46.20074,
                    21.28622,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Romania',
                    admin1name='Arad',
                    admin2name='None',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Phoenix',
                    -1,
                    'Phoenix',
                    '???',
                    '???',
                    '???',
                    '???',
                    1.30082,
                    103.84015,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Singapore',
                    admin1name='None',
                    admin2name='None',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Phoenix',
                    -1,
                    'Phoenix',
                    '???',
                    '???',
                    '???',
                    '???',
                    33.36597,
                    -83.27766,
                    0),
                adminnames=LocationAdminNames(
                    countryname='United States',
                    admin1name='Georgia',
                    admin2name='Putnam County',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Phoenix',
                    -1,
                    'Phoenix',
                    '???',
                    '???',
                    '???',
                    '???',
                    29.64605,
                    -89.93979,
                    0),
                adminnames=LocationAdminNames(
                    countryname='United States',
                    admin1name='Louisiana',
                    admin2name='Plaquemines Parish',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Phoenix',
                    -1,
                    'Phoenix',
                    '???',
                    '???',
                    '???',
                    '???',
                    39.51649,
                    -76.61608,
                    0),
                adminnames=LocationAdminNames(
                    countryname='United States',
                    admin1name='Maryland',
                    admin2name='Baltimore County',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Phoenix',
                    -1,
                    'Phoenix',
                    '???',
                    '???',
                    '???',
                    '???',
                    32.58125,
                    -90.56287,
                    0),
                adminnames=LocationAdminNames(
                    countryname='United States',
                    admin1name='Mississippi',
                    admin2name='Yazoo County',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Phoenix',
                    -1,
                    'Phoenix',
                    '???',
                    '???',
                    '???',
                    '???',
                    34.2935,
                    -78.05833,
                    0),
                adminnames=LocationAdminNames(
                    countryname='United States',
                    admin1name='North Carolina',
                    admin2name='Brunswick County',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Phoenix',
                    -1,
                    'Phoenix',
                    '???',
                    '???',
                    '???',
                    '???',
                    34.07735,
                    -82.11095,
                    0),
                adminnames=LocationAdminNames(
                    countryname='United States',
                    admin1name='South Carolina',
                    admin2name='Greenwood County',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Phoenix',
                    -1,
                    'Phoenix',
                    '???',
                    '???',
                    '???',
                    '???',
                    29.3819,
                    -98.54168,
                    0),
                adminnames=LocationAdminNames(
                    countryname='United States',
                    admin1name='Texas',
                    admin2name='Bexar County',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Phoenix',
                    -1,
                    'Phoenix',
                    '???',
                    '???',
                    '???',
                    '???',
                    41.61115,
                    -87.63477,
                    0),
                adminnames=LocationAdminNames(
                    countryname='United States',
                    admin1name='Illinois',
                    admin2name='Cook County',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Phoenix',
                    -1,
                    'Phoenix',
                    '???',
                    '???',
                    '???',
                    '???',
                    47.38881,
                    -88.27761,
                    0),
                adminnames=LocationAdminNames(
                    countryname='United States',
                    admin1name='Michigan',
                    admin2name='Keweenaw County',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Phoenix',
                    -1,
                    'Phoenix',
                    '???',
                    '???',
                    '???',
                    '???',
                    40.47788,
                    -74.31293,
                    0),
                adminnames=LocationAdminNames(
                    countryname='United States',
                    admin1name='New Jersey',
                    admin2name='Middlesex County',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Phoenix',
                    -1,
                    'Phoenix',
                    '???',
                    '???',
                    '???',
                    '???',
                    40.52983,
                    -74.34098,
                    0),
                adminnames=LocationAdminNames(
                    countryname='United States',
                    admin1name='New Jersey',
                    admin2name='Middlesex County',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Phoenix',
                    -1,
                    'Phoenix',
                    '???',
                    '???',
                    '???',
                    '???',
                    43.23118,
                    -76.30076,
                    0),
                adminnames=LocationAdminNames(
                    countryname='United States',
                    admin1name='New York',
                    admin2name='Oswego County',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Phoenix',
                    -1,
                    'Phoenix',
                    '???',
                    '???',
                    '???',
                    '???',
                    33.44838,
                    -112.07404,
                    0),
                adminnames=LocationAdminNames(
                    countryname='United States',
                    admin1name='Arizona',
                    admin2name='Maricopa County',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Phoenix',
                    -1,
                    'Phoenix',
                    '???',
                    '???',
                    '???',
                    '???',
                    39.92689,
                    -112.1105,
                    0),
                adminnames=LocationAdminNames(
                    countryname='United States',
                    admin1name='Utah',
                    admin2name='Juab County',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Phoenix',
                    -1,
                    'Phoenix',
                    '???',
                    '???',
                    '???',
                    '???',
                    42.27541,
                    -122.81809,
                    0),
                adminnames=LocationAdminNames(
                    countryname='United States',
                    admin1name='Oregon',
                    admin2name='Jackson County',
                    admin3name='None',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Phoenix',
                    -1,
                    'Phoenix',
                    '???',
                    '???',
                    '???',
                    '???',
                    -29.71667,
                    31.01667,
                    0),
                adminnames=LocationAdminNames(
                    countryname='South Africa',
                    admin1name='Province of KwaZulu-Natal',
                    admin2name='eThekwini Metropolitan Municipality',
                    admin3name='Ethekwini',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Phoenix',
                    -1,
                    'Phoenix',
                    '???',
                    '???',
                    '???',
                    '???',
                    -29.70428,
                    30.9761,
                    0),
                adminnames=LocationAdminNames(
                    countryname='South Africa',
                    admin1name='Province of KwaZulu-Natal',
                    admin2name='eThekwini Metropolitan Municipality',
                    admin3name='Ethekwini',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Phoenix',
                    -1,
                    'Phoenix',
                    '???',
                    '???',
                    '???',
                    '???',
                    -26.07098,
                    29.20451,
                    0),
                adminnames=LocationAdminNames(
                    countryname='South Africa',
                    admin1name='Mpumalanga',
                    admin2name='Nkangala District Municipality',
                    admin3name='Emalahleni',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Phoenix',
                    -1,
                    'Phoenix',
                    '???',
                    '???',
                    '???',
                    '???',
                    -28.3,
                    26.81667,
                    0),
                adminnames=LocationAdminNames(
                    countryname='South Africa',
                    admin1name='Free State',
                    admin2name='Lejweleputswa District Municipality',
                    admin3name='Masilonyana',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Phoenix',
                    -1,
                    'Phoenix',
                    '???',
                    '???',
                    '???',
                    '???',
                    -25.71076,
                    23.04885,
                    0),
                adminnames=LocationAdminNames(
                    countryname='South Africa',
                    admin1name='Province of North West',
                    admin2name='Dr Ruth Segomotsi Mompati District'
                               ' Municipality',
                    admin3name='Kagisano/Molopo',
                    admin4name='None')),
            LocationWrap(
                Location(
                    'Phoenix',
                    -1,
                    'Phoenix',
                    '???',
                    '???',
                    '???',
                    '???',
                    -16.71667,
                    29.78333,
                    0),
                adminnames=LocationAdminNames(
                    countryname='Zimbabwe',
                    admin1name='None',
                    admin2name='None',
                    admin3name='None',
                    admin4name='None'))])
        )
        # actual is application-generated admin names
        actual = self.weightifier._gather_all_names(container, 4)
        assert expected == actual

    def test__filter_by_weight(self):
        """
        Tests weighter._filter_by_weight
        """
        container = LocationHitsContainer()
        Hits1 = 'Hits1'
        Hits2 = 'Hits2'
        L2 = LocationWrap(
            Location(
                'L2',
                -1,
                'L2',
                '???',
                '???',
                '???',
                '???',
                -35.72259,
                -65.31972,
                0),
            weight=16,
            adminnames=LocationAdminNames(
                countryname='None',
                admin1name='None',
                admin2name='None',
                admin3name='None',
                admin4name='None')),
        L10 = LocationWrap(
            Location(
                'L10',
                -1,
                'L10',
                '???',
                '???',
                '???',
                '???',
                -35.72259,
                -65.31972,
                0),
            weight=1,
            adminnames=LocationAdminNames(
                countryname='None',
                admin1name='None',
                admin2name='None',
                admin3name='None',
                admin4name='None'))
        # Hits1 - max weight is 16 from L2
        container.append(LocationHits(Hits1, [
            LocationWrap(
                Location(
                    'L1',
                    -1,
                    'L1',
                    '???',
                    '???',
                    '???',
                    '???',
                    -35.72259,
                    -65.31972,
                    0),
                weight=7,
                adminnames=LocationAdminNames(
                    countryname='None',
                    admin1name='None',
                    admin2name='None',
                    admin3name='None',
                    admin4name='None')),
            L2,
            LocationWrap(
                Location(
                    'L3',
                    -1,
                    'L3',
                    '???',
                    '???',
                    '???',
                    '???',
                    -35.72259,
                    -65.31972,
                    0),
                weight=3,
                adminnames=LocationAdminNames(
                    countryname='None',
                    admin1name='None',
                    admin2name='None',
                    admin3name='None',
                    admin4name='None'))]))
        # Hits2 - max weight is 1 from L10
        container.append(LocationHits(Hits2, [
            L10,
            LocationWrap(
                Location(
                    'L11',
                    -1,
                    'L11',
                    '???',
                    '???',
                    '???',
                    '???',
                    -35.72259,
                    -65.31972,
                    0),
                weight=0,
                adminnames=LocationAdminNames(
                    countryname='None',
                    admin1name='None',
                    admin2name='None',
                    admin3name='None',
                    admin4name='None'))]))

        expected = LocationHitsContainer()
        expected.append(LocationHits(Hits1, L2))
        expected.append(LocationHits(Hits2, L10))
        actual = self.weightifier._filter_by_weight(container)
        assert expected == actual

    def test__back_weight(self):
        """
        Tests weighter.back_weight
        """

    def test__weightify__pass(self):
        """
        Tests weighter.weightify with accuracy of 4
        """
        assert False


# def test_admin4named_locations():
#     """
#     Returns a giant list of all locations in geonames that have
#     a populated admin4name field
#     """
#     accuracy = 7
#     select = ('SELECT l.geonameid, l.name, l.featurecode, l.featureclass')
#     if accuracy > 0:
#         select += ', l.countrycode'
#     if accuracy > 1:
#         select += ', l.admin1code'
#     if accuracy > 2:
#         select += ', l.admin2code'
#     if accuracy > 3:
#         select += ', l.admin3code'
#     if accuracy > 4:
#         select += ', l.admin4code'
#     fromm = 'FROM raw_locations l'
#     where = 'WHERE NOT l.admin4code = \'\''
#     sql = text('%s\n%s\n%s' % (select, fromm, where))
#     # should return only 1
#     result = db.engine.execute(sql)
#     admincodes = []
#     for row in result:
#         admincodes.append(row)
#     print admincodes
#     assert False
