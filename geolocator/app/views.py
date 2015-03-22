# -*- coding: utf-8 -*-
"""
Provides various URLs handles for the website
"""
from flask import render_template, render_template_string, request, jsonify
from app import app

from nlp import LocationTagger
import geolocator


@app.route('/')
@app.route('/home')
def Index():
    """
    Home page of website

    URL Routes:

        * '/'
        * '/home'

    :returns: template 'index.html'
    """
    # form = OutputFormatForm()
    # if form.validate_on_submit():
    #     x = 1 / 0
    #     return UploadFile(form.geojson, form.heatmap)
        # return redirect('/index')
    return render_template(
        'index.html',
        title='Text Geolocator')


def AllowedFile(filename):
    """
    Validates file type upon upload from user

    Allowed file types:

        * .txt

    :param str filename: name of file (with extension)

    :returns: bool - True if file type is allowed; false otherwise
    """
    return '.' in filename and filename.rsplit('.', 1)[1] \
        in app.config['ALLOWED_EXTENSIONS']


@app.route('/dbtest')
def dbtest():
    from app.models import Location, Feature
    location = Location.query.first()
    feature = Feature.query.first()
    return render_template(
        'dbtest.html',
        first_location=location,
        first_feature=feature)


@app.route('/upload', methods=['GET', 'POST'])
def UploadFile():
    """
    Receives the uploaded text of a document via POST and returns the
        geojson collection data along with a heatmap

    URL Routes:

        * '/upload'

    :returns: heatmap and pretty-printed geojson collection if file is
        uploaded via POST and is of correct file type; otherwise
        prints "No uploaded file detected"
    """
    if request.method == 'POST':
        uploadedfile = request.files['file']
        if uploadedfile and AllowedFile(uploadedfile.filename):

            # this is supposed to save file to /tmp/uploads
            # ---------------------------------------------------------------
            # filename = secure_filename(uploadedfile.filename)
            # uploadedfile_path =
            #     os.path.join(app.config['UPLOAD_FOLDER'],filename)
            # with open(uploadedfile_path, 'wb') as f:
            # ....f.write(uploadedfile.read())
            # return redirect(url_for('uploaded_file', filename=filename))

            text = uploadedfile.read()

            tagger = LocationTagger()
            locations = tagger.TagLocations(text)

            geojson_collection = \
                geolocator.MakeGeoJsonCollection(locations)

            latlngs = geolocator.RetrieveLatLngs(geojson_collection)
            geojson_jsonify =  jsonify(**geojson_collection)

            return render_template(
                'result.html',
                geojson_jsonify =  geojson_jsonify,
                latlngs=latlngs,
                center=latlngs[0],
                geojson_collection=geojson_collection
            )
    return '''<!doctype html><title>Upload new File</title><body>
           <p>No uploaded file detected.</p></body>'''
