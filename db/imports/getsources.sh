#!/bin/sh
# Create the temp directorys
mkdir -p ~/geodata
cp -f ./importdata.sql ~/geodata/
cd ~/geodata

# Download the dump files
curl -O http://download.geonames.org/export/dump/featureCodes_en.txt 
curl -O http://download.geonames.org/export/dump/readme.txt 
curl -O http://download.geonames.org/export/dump/countryInfo.txt
curl -O http://download.geonames.org/export/dump/allCountries.zip

# Extract the compressed files
unzip allCountries.zip
rm allCountries.zip

# Create the tables
psql -h localhost -p 5432 -d app -U postgres -a -f ~/geodata/importdata.sql
