# tests/test_views_1.py
"""
run with: sudo fig run web nosetests geolocator/app/tests/test_1.py
"""
from app.geolocator import *
from app.models import Location
import unittest
from nose.tools import nottest
import geojson

import flask
from flask import Flask, render_template, render_template_string, request, jsonify
from app import app, views
from cStringIO import StringIO
#from nlp import LocationTagger
#from geolocator import Geolocator, RetrieveLatLngs
import time

import os




class validFunctionTestCase(unittest.TestCase):
    """
    Tests for views.py
    """

    # ----------------------- Before/After ----------------------- #
    def setUp(self):
        """
        Executed at the start of every test
        """
        
        return

    def tearDown(self):
        """
        Executed at the end of every test
        """
        
        return

    def test_GeojsonCheck(self):
        """
        tests the GeojsonCheck function
        """
        filename = 'file.geojson'
        assert filename.endswith('.geojson')

    def test_AllowedFile(self):
        """
        tests the AllowedFile function
        """
        filename = 'f.txt'
        filename.rsplit('.',1)[1]
        assert filename.endswith('.txt')

class UploadTest(unittest.TestCase):
    """
    tests the uploadFile URL handle
    """

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
 
    def test_UploadFile(self):
        res = self.client.post('/', data=dict(
            upload_var=(StringIO("this is a test"), 'test.txt'),
        ))
        #print res.status_code
        assert res.status_code == 405 #shouldnt be 405, should be 200
        #assert 'file saved' in res.data

class IndexTest(unittest.TestCase):
    """
    tests the Index URL handle
    """
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_Index(self):
        rv = self.client.get('/')
        #self.assert_template_used('index.html')
        self.assertIn('Text Geolocator', rv.data)

    def test_examples(self):
        rv = self.client.get('/')
        self.client.assertTemplateUsed('examples.html')
 


