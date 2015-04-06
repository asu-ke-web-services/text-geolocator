# -*- coding: utf-8 -*-
"""
Provides various URLs handles for the website
"""
from flask import render_template, render_template_string, request, jsonify
from app import app

from nlp import LocationTagger
from geolocator import Geolocator, RetrieveLatLngs


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


def GeojsonCheck(filename):
    if filename.endswith('.geojson'):
        return True
    else:
        return False


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
    from app.weighter import Weightifier
    from app.geolocator import LocationWrap
    weightifier = Weightifier()
    location = Location.query.filter_by(
        name='Phoenix',
        countrycode='US').order_by('id').first()
    feature = Feature.query.first()
    wrap = LocationWrap(location)
    codes = weightifier._get_admin_codes(wrap, 5)
    names = weightifier._get_admin_names(codes)
    # wrap.set_adminnames(names)
    return render_template(
        'dbtest.html',
        first_location=location,
        admin_codes=codes,
        admin_names=names,
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
        if uploadedfile and GeojsonCheck(uploadedfile.filename):
            # checks for a geojson upload
            geojson = uploadedfile.read()
            latlngs = RetrieveLatLngs(geojson)
            if not latlngs:
                return render_template_string("""
                    {% extends "base.html" %}
                    {% block content %}
                    <div class="center">
                        <h1>File formatted incorrectly.</h1>
                    </div>
                    {% endblock %}""")
            return render_template(
                'result.html',
                latlngs=latlngs,
                center=latlngs[0],
                geojson_collection=geojson
            )
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

            geolocator = Geolocator()
            geolocator.geolocate(locations, weights=False, accuracy=1)
            geojson = geolocator.geojson()
            geojson_jsonify = jsonify(**geojson)

            latlngs = RetrieveLatLngs(geojson)

            return render_template(
                'result.html',
                latlngs=latlngs,
                center=latlngs[0],
                geojson_collection=geojson,
                geojson_jsonify=geojson_jsonify
            )
    return render_template_string("""
        {% extends "base.html" %}
        {% block content %}
        <div class="center">
            <h1>No uploaded file detected.</h1>
        </div>
        {% endblock %}""")


@app.route('/examples')
def examples():
    return render_template('examples.html')


@app.route('/examples/weights_off')
def example_weights_off():
    return render_template('example_weights_off.html')


@app.route('/examples/weights_on_accuracy_1')
def example_weights_on_acc_1():
    return render_template('example_weights_on_acc_1.html')


@app.route('/examples/weights_on_accuracy_2')
def example_weights_on_acc_2():
    return render_template('example_weights_on_acc_2.html')
