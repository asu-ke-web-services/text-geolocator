/* Create the temp tables to import the data to */
DROP TABLE raw_country_info;
DROP TABLE raw_feature_codes;
DROP TABLE raw_locations;

CREATE TABLE raw_country_info (
	ISO varchar,
	ISO3 varchar,
	ISONumeric varchar,
	fips varchar,
	country varchar,
	capital varchar,
	area varchar,
	population varchar,
	continent varchar,
	tld varchar,
	currencycode varchar,
	currencyname varchar,
	phone varchar,
	postalcodeformat varchar,
	postalcoderegex varchar,
	languages varchar,
	geonameid varchar,
	neighbours varchar,
	equivalentfipscode varchar
);

CREATE TABLE raw_feature_codes (
	code varchar,
	name varchar,
	description varchar
);
CREATE TABLE raw_locations (
	geonameid varchar,
	name varchar,
	asciiname varchar,
	alternamtename varchar,
	latitude varchar,
	longitude varchar,
	featureclass varchar,
	featurecode varchar,
	countrycode varchar,
	cc2 varchar,
	admin1code varchar,
	admin2code varchar,
	admin3code varchar,
	admin4code varchar,
	population varchar,
	elevation varchar,
	dem varchar,
	timezone varchar,
	modificationdate varchar
);


/* Import the data */
\COPY raw_country_info FROM '~/geodata/countryInfo.txt';
\COPY raw_feature_codes FROM '~/geodata/featureCodes_en.txt';
\COPY raw_locations FROM '~/geodata/allCountries.txt';

/* Put the data into the new tables */
INSERT INTO location
(geonameid, name, countrycode, featureclass, featurecode, featuretype, latitude, longitude, initial_weight)
SELECT cast(geonameid as numeric),
       name,
       countrycode,
       featureclass,
       featurecode,
       featureclass || '.' || featurecode,
       cast(latitude as float),
       cast(longitude as float),
       0.0
FROM raw_locations;

INSERT INTO feature
(featureclass, featurecode, code, name, description)
SELECT substring(code FROM 1 FOR 1),
       substring(code FROM 3 FOR (char_length(code) - 2)),
       code,
       name,
       description
FROM raw_feature_codes;
