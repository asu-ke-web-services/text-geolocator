#!/bin/sh
echo "Creating app database..."
gosu postgres postgres --single <<- EOSQL
	CREATE DATABASE app TEMPLATE template_postgis;
EOSQL
echo "Done creating database..."
