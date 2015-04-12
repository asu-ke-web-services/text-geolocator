#!/usr/bin/python
"""
Contains the following classes:

    * LocationAdminParent
    * LocationAdminNames
    * LocationAdminCodes
    * Query
    * AdminNameGetter
    * Weightifier

This file manages all weighting operations within this application
"""
from sqlalchemy import text
from app import db


class LocationAdminParent(object):
    """
    Serves only to be inherited by LocationAdminCodes and LocationAdminNames
    """

    def __init__(self):
        self.geonameid = -1
        self.name = None


class LocationAdminNames(LocationAdminParent):
    """
    Container object for a location's admin names
    Inherits from LocationAdminParent
    """

    def __init__(self):
        super(LocationAdminNames, self).__init__()
        self.admin4name = None
        self.admin3name = None
        self.admin2name = None
        self.admin1name = None
        self.countryname = None
        return

    def list(self):
        """
        Returns all names combined in a list

        :returns: list -- all names
        """
        l = []
        if self.admin4name:
            l.append(self.admin4name)
        if self.admin3name:
            l.append(self.admin3name)
        if self.admin2name:
            l.append(self.admin2name)
        if self.admin1name:
            l.append(self.admin1name)
        if self.countryname:
            l.append(self.countryname)
        return l

    def match(self, location_name):
        """
        Checks if location_name matches any of the contained names

        :param str location_name: name of a location

        :returns: True on match; otherwise False
        """
        return (location_name == self.admin4name or
                location_name == self.admin3name or
                location_name == self.admin2name or
                location_name == self.admin1name or
                location_name == self.countryname)

    def __eq__(self, other):
        return (isinstance(other, LocationAdminNames) and
                self.admin4name == other.admin4name and
                self.admin3name == other.admin3name and
                self.admin2name == other.admin2name and
                self.admin1name == other.admin1name and
                self.countryname == other.countryname)

    def __repr__(self):
        return ("<LocationAdminNames(geonameid=%s, name=%s, admin4name=%s, "
                "admin3name=%s, admin2name=%s, admin1name=%s, "
                "countryname=%s)>" % (
                    str(self.geonameid), str(self.name), str(self.admin4name),
                    str(self.admin3name), str(self.admin2name),
                    str(self.admin1name), str(self.countryname)))


class LocationAdminCodes(LocationAdminParent):
    """
    Container object for a location's admin codes
    Inherits from LocationAdminParent
    """

    def __init__(self):
        super(LocationAdminCodes, self).__init__()
        self.featurecode = None
        self.featureclass = None
        self.admin4code = None
        self.admin3code = None
        self.admin2code = None
        self.admin1code = None
        self.countrycode = None
        return

    def __eq__(self, other):
        """
        Determines if self is equal to other

        :param ? other: other object to compare to

        :returns: True if other is a LocationAdminCodes object and all fields
        match; otherwise False
        """
        return (isinstance(other, LocationAdminCodes) and
                self.geonameid == other.geonameid and
                self.name == other.name and
                self.featurecode == other.featurecode and
                self.featureclass == other.featureclass and
                self.countrycode == other.countrycode and
                self.admin1code == other.admin1code and
                self.admin2code == other.admin2code and
                self.admin3code == other.admin3code and
                self.admin4code == other.admin4code)

    def __repr__(self):
        return ("<LocationAdminCodes(geonameid=%s, name=%s, featurecode=%s, "
                "featureclass=%s, admin4code=%s, admin3code=%s, "
                "admin2code=%s, admin2code=%s, countrycode=%s)>" % (
                    str(self.geonameid), str(self.name), str(self.featurecode),
                    str(self.featureclass), str(self.admin4code),
                    str(self.admin3code), str(self.admin2code),
                    str(self.admin1code), str(self.countrycode)))


class Query(object):
    """
    Simplifies writing code for querying the geonames database
    """

    def __init__(self, selects, froms, wheres=None):
        if not isinstance(selects, list):
            raise TypeError('selects must be a list')
        if not isinstance(froms, list):
            raise TypeError('froms must be a list')
        if wheres is not None and not isinstance(wheres, list):
            raise TypeError('wheres must be a list')
        self.sql = ''
        self.selects = selects
        self.froms = froms
        self.wheres = wheres
        return

    def expand_list(self, list_to_be_expanded, separator=', '):
        """
        Given 'list_to_be_expanded', expands to format of

            'item1, item2, ..., itemN'

        Returns expanded str
        """
        separator = separator if separator is not None else ''
        if list_to_be_expanded is None:
            return ''
        expanded_list = ''
        for l in list_to_be_expanded:
            expanded_list += l + separator
        return expanded_list[0:len(expanded_list)-len(separator)]

    def _add_sql(self, statement):
        """
        Given an sql 'statement', add statement to end of self.sql
        """
        if statement is None:
            raise TypeError("statement cannot be None")
        self.sql += '' if self.sql is '' else ' '
        self.sql += statement
        return

    def to_sql(self):
        """
        Converts items in selects, froms, and wheres to a valid SQL statement
        """
        self._add_sql("select %s" % self.expand_list(self.selects))
        self._add_sql("from %s" % self.expand_list(self.froms))
        if self.wheres is not None:
            self._add_sql("where %s" % self.expand_list(self.wheres, ' AND '))
        return text(self.sql)

    def __repr__(self):
        return ('<Query(selects=%s, froms=%s, wheres=%s)>' % (
            self.selects, self.froms, self.wheres))


class AdminNameGetter(object):
    """
    Gets the names of locations according to given admin codes from the
    geonames db
    """

    ADMIN_FEATURE_CODES = [
        'ADM1',  # admin1
        'ADM2',  # admin2
        'ADM3',  # admin3
        'ADM4'   # admin4
    ]
    """feature codes of administration level locations in geonames"""
    SELECT = 'l.name'
    FROM = 'raw_locations l'

    def __init__(self, admincodes):
        """
        :param LocationAdminCodes admincodes: codes will be used when
        querying for names
        """
        self.codes = admincodes
        return

    def _query_one(self, sql):
        """
        Returns a single hit from the geonames database from the query
        defined in sql

        :param str sql: query to execute

        :returns: a 'hit' whatever that might be from the given query
        """
        result = db.engine.execute(sql)
        hit = None
        for row in result:
            hit = row
        return hit

    def _sql_admin4code(self):
        """
        Formats part of an sql query statement for matching the admin4code
        """
        return "l.admin4code = '%s'" % str(self.codes.admin4code)

    def _sql_admin3code(self):
        """
        Formats part of an sql query statement for matching the admin3code
        """
        return "l.admin3code = '%s'" % str(self.codes.admin3code)

    def _sql_admin2code(self):
        """
        Formats part of an sql query statement for matching the admin2code
        """
        return "l.admin2code = '%s'" % str(self.codes.admin2code)

    def _sql_admin1code(self):
        """
        Formats part of an sql query statement for matching the admin1code
        """
        return "l.admin1code = '%s'" % str(self.codes.admin1code)

    def _sql_countrycode(self):
        """
        Formats part of an sql query statement for matching the countrycode
        """
        return "l.countrycode = '%s'" % str(self.codes.countrycode)

    def _sql_featurecode(self, index):
        """
        Formats part of an sql query statement for matching the featurecode
        """
        return "l.featurecode = '%s'" % str(self.ADMIN_FEATURE_CODES[index])

    def _admin4name(self):
        """
        Finds the name of the admin4 location of the given admin codes
        if one exists

        :returns: name string of admin4 location
        """
        index = 4
        wheres = [
            self._sql_admin4code(),
            self._sql_admin3code(),
            self._sql_admin2code(),
            self._sql_admin1code(),
            self._sql_countrycode(),
            self._sql_featurecode(index-1)
        ]
        query = Query([self.SELECT], [self.FROM], wheres)
        sql = query.to_sql()
        result = self._query_one(sql)
        if result:
            return result[0]

    def _admin3name(self):
        """
        Finds the name of the admin3 location of the given admin codes
        if one exists

        :returns: name string of admin3 location
        """
        index = 3
        wheres = [
            self._sql_admin3code(),
            self._sql_admin2code(),
            self._sql_admin1code(),
            self._sql_countrycode(),
            self._sql_featurecode(index-1)
        ]
        query = Query([self.SELECT], [self.FROM], wheres)
        sql = query.to_sql()
        result = self._query_one(sql)
        if result:
            return result[0]

    def _admin2name(self):
        """
        Finds the name of the admin2 location of the given admin codes
        if one exists

        :returns: name string of admin2 location
        """
        index = 2
        wheres = [
            self._sql_admin2code(),
            self._sql_admin1code(),
            self._sql_countrycode(),
            self._sql_featurecode(index-1)
        ]
        query = Query([self.SELECT], [self.FROM], wheres)
        sql = query.to_sql()
        result = self._query_one(sql)
        if result:
            return result[0]

    def _admin1name(self):
        """
        Finds the name of the admin1 location of the given admin codes
        if one exists

        :returns: name string of admin1 location
        """
        index = 1
        wheres = [
            self._sql_admin1code(),
            self._sql_countrycode(),
            self._sql_featurecode(index-1)
        ]
        query = Query([self.SELECT], [self.FROM], wheres)
        sql = query.to_sql()
        result = self._query_one(sql)
        if result:
            return result[0]

    def _countryname(self):
        """
        Finds the name of the country of the given admin codes if one exists

        :returns: name string of country
        """
        selects = ['r.country']
        froms = ['raw_country_info r']
        wheres = ["ISO = '%s'" % str(self.codes.countrycode)]
        query = Query(selects, froms, wheres)
        sql = query.to_sql()
        result = self._query_one(sql)
        if result:
            return result[0]

    def adminnames(self):
        """
        Makes a LocationAdminNames object with given admin codes

        :returns: app.geolocator.LocationAdminNames object
        """
        names = LocationAdminNames()
        # countrycode name will only exist if countrycode code is populated
        if self.codes.countrycode:
            names.countryname = self._countryname()
            # admin1 name will only exist if countrycode code AND admin1 code
            # is populated
            if self.codes.admin1code:
                names.admin1name = self._admin1name()
                # ... you get the idea
                if self.codes.admin2code:
                    names.admin2name = self._admin2name()
                    # ... again
                    if self.codes.admin3code:
                        names.admin3name = self._admin3name()
                        # ... final one
                        if self.codes.admin4code:
                            names.admin4name = self._admin4name()
        return names

    def __repr__(self):
        return "<AdminNameGetter()>"


class Weightifier(object):
    """
    Applies a weighting algorithm to all tagged locations to improve the
    app's accuracy when displaying locations in the heatmap
    """

    SQL_RAW_LOCATIONS = 'raw_locations'

    def __init__(self):
        return

    def _make_sql(self, select, fromm, where):
        """
        Makes an sql string from the given sql components

        :param str select: sql select statement
        :param str fromm: sql from statement
        :param str where: sql where statement

        :returns: sql string
        """
        sql = text('%s\n%s\n%s' % (select, fromm, where))
        return sql

    def _make_admin_codes_query(self, geonameid, accuracy):
        """
        Returns the sql for a query to find admin names

        :param int geonameid: geoname location to query for
        :param int accuracy: level of accuracy when assigning weights (see
        app.geolocator.Geolocator.geolocate for information on accuracy
        settings)

        :returns: sql string
        """
        select = ('SELECT l.geonameid, l.name, l.featurecode, l.featureclass')
        if accuracy > 0:
            select += ', l.countrycode'
        if accuracy > 1:
            select += ', l.admin1code'
        if accuracy > 2:
            select += ', l.admin2code'
        if accuracy > 3:
            select += ', l.admin3code'
        if accuracy > 4:
            select += ', l.admin4code'
        fromm = 'FROM %s l' % self.SQL_RAW_LOCATIONS
        where = 'WHERE l.geonameid = \'%s\'' % (str(geonameid))
        return self._make_sql(select, fromm, where)

    def _make_admin_codes(self, query_result):
        """
        Given the result of a query made in _get_admin_names, this  will
        return a a LocationAdminCodes object containing all the query data

        :param list query_result: list of attributes retrieved by query

        :returns: appl.geolocator.LocationAdminCodes
        """
        length = len(query_result)
        admincodes = LocationAdminCodes()
        admincodes.geonameid = query_result[0]
        admincodes.name = query_result[1]
        admincodes.featurecode = query_result[2]
        admincodes.featureclass = query_result[3]
        index = 4
        if length > index:
            admincodes.countrycode = query_result[index]
        index += 1
        if length > index:
            admincodes.admin1code = query_result[index]
        index += 1
        if length > index:
            admincodes.admin2code = query_result[index]
        index += 1
        if length > index:
            admincodes.admin3code = query_result[index]
        index += 1
        if length > index:
            admincodes.admin4code = query_result[index]
        return admincodes

    def _get_admin_codes(self, location, accuracy):
        """
        Finds the codes for each administration level for the given location

        Each geonames location has the following attributes:

            * countrycode (country -- example: US)
            * admin1code (state -- example: Arizona)
            * admin2code (region -- example: Maricopa County)
            * admin3code (unsure)
            * admin4code (unsure)

        This function finds the codes for each for use in weighting

        :param app.geolocator.LocationWrap: location to find admin codes for
        :param int accuracy: level of accuracy when assigning weights (see
        app.geolocator.Geolocator.geolocate for information on accuracy
        settings)

        :returns: app.geolocator.LocationAdminCodes
        """
        # get admin data from raw_locations table
        sql = self._make_admin_codes_query(location.geonameid(), accuracy)
        # should return only 1
        result = db.engine.execute(sql)
        admincodes = None
        for row in result:
            admincodes = self._make_admin_codes(row)
        return admincodes

    def _get_admin_names(self, admincodes):
        """
        Finds the names for each administration level in the given codes using
        the AdminNameGetter

        :param app.geolocator.LocationAdminCodes: codes to find names for

        :returns: app.geolocator.LocationAdminNames
        """
        namegetter = AdminNameGetter(admincodes)
        return namegetter.adminnames()

    def _gather_all_names(self, container, accuracy):
        """
        Iterates through all locations in container, finds their admin names,
        and sets the names in their location wrap

        :param app.geolocator.LocationHitsContainer: contains the locations
        :param int accuracy: level of accuracy when assigning weights (see
        app.geolocator.Geolocator.geolocate for information on accuracy
        settings)

        :returns: app.geolocator.LocationHitsContainer with admin names
        """
        for hits in container.hits:
            for l in hits:
                codes = self._get_admin_codes(l, accuracy)
                names = self._get_admin_names(codes)
                l.set_adminnames(names)
        return container

    def weightify(self, container, accuracy):
        """
        Assigns a weight value to each LocationWrap within the container

        :param app.geolocator.LocationHitsContainer container: container
        containing locations to weight
        :param int accuracy: level of accuracy when assigning weights (see
        app.geolocator.Geolocator.geolocate for information on accuracy
        settings)

        :returns: app.geolocator.LocationHitsContainer with weighted locations
        """
        container = self._gather_all_names(container, accuracy)
        # TODO - room for OO and performance improvement here
        # -------------
        # iterate over all names and increments all location wraps
        # that either have the same name or matches their admin names
        # names_attempted = list()
        for hits in container.hits:
            for loc_wrap in hits:
                container.increment_weight_on_match(loc_wrap.adminnames)
                # names = loc_wrap.names_list()
                # for name in names:
                #     names_attempted.append(name)
                #     container.increment_weight_on_match(name)
        # -------------
        # iterate over all hits remove all location wraps that are
        # less than the max weight for those wraps
        for i, hits in enumerate(container.hits):
            max_weight = hits.max_weight()
            if max_weight > -1:
                removes = list()
                for l in hits:
                    if l.weight() < max_weight:
                        removes.append(l)
                for l in removes:
                    container.hits[i].locations.remove(l)
        return container

    def __repr__(self):
        return "<Weightifier()>"
