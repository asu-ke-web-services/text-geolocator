# -*- coding: utf-8 -*-

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Configure java with python

os.environ['JAVAHOME'] = '/usr/lib/jvm/java-1.7.0-openjdk-amd64/bin'

# file used to store specific config parameters

CSRF_ENABLED = True

DATABASE_CONNECT_OPTIONS = {}

DEBUG = os.getenv('DEBUG', False)
PORT = os.getenv('PORT', 5000)

SQLALCHEMY_DATABASE_URI = os.getenv(
    'DATABASE_URL',
    'postgres://postgres@{0}/app'.format(os.getenv('DB_1_PORT_5432_TCP_ADDR')))

SECRET_KEY = os.getenv('SECRET_KEY', None)

# This is the path to the upload directory

UPLOAD_FOLDER = 'tmp/uploads'

# These are the extension that we are accepting to be uploaded

ALLOWED_EXTENSIONS = set(['txt'])

# Stanford NER Configuration

SNER_CLASSIFIERS = \
    (BASE_DIR + '/app/static/stanford-ner-2014-08-27/classifiers/english.all.'
     '3class.distsim.crf.ser.gz')
SNER_JARFILE = \
    BASE_DIR + '/app/static/stanford-ner-2014-08-27/stanford-ner.jar'
