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
    """
    Checks if filename is of type geojson

    :param str filename: filename to check

    :returns: bool - True if filename ends with geojson; otherwise False
    """
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
    """
    This is a hidden url route not available through website GUI.

    It serves as a test for developer's to make sure that their
    database and environment are up and running correctly.

    If the dev does not get an error message when louding this URL,
    then it can be assumed that the environment is working.
    """
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
        accuracy = request.form.get('weight')
        if uploadedfile:

            filename = "%s_acc-%s" % (str(uploadedfile.filename),
                                      str(accuracy))

            if GeojsonCheck(uploadedfile.filename):
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
                    geojson_collection=geojson,
                    uploaded_file_name=uploadedfile.filename,
                    download_filename=filename,
                    display_file_stats=0,
                    distinct_locations=len(latlngs)
                )
            if AllowedFile(uploadedfile.filename):

                # this is supposed to save file to /tmp/uploads
                # ---------------------------------------------------------
                # filename = secure_filename(uploadedfile.filename)
                # uploadedfile_path =
                #     os.path.join(app.config['UPLOAD_FOLDER'],filename)
                # with open(uploadedfile_path, 'wb') as f:
                # ....f.write(uploadedfile.read())
                # return redirect(url_for('uploaded_file', filename=filename))
                text = uploadedfile.read()

                tagger = LocationTagger()
                wordcount = tagger.CountWords(text)
                locations = tagger.TagLocations(text)

                geolocator = Geolocator()
                try:
                    accuracy = int(accuracy)
                except:
                    accuracy = 0
                weights = (accuracy > 0)
                geolocator.geolocate(
                    locations,
                    weights=weights,
                    accuracy=accuracy)
                geojson = geolocator.geojson()
                geojson_jsonify = jsonify(**geojson)

                latlngs = RetrieveLatLngs(geojson)

                try:
                    text = text.encode('utf-8')
                except:
                    text = ("Cannot display file's contents as "
                            "non-unicode characters are present")

                return render_template(
                    'result.html',
                    latlngs=latlngs,
                    center=latlngs[0],
                    geojson_collection=geojson,
                    geojson_jsonify=geojson_jsonify,
                    uploaded_file_name=uploadedfile.filename,
                    display_file_stats=1,
                    word_count=wordcount,
                    tagged_locations=len(locations),
                    distinct_locations=len(latlngs),
                    accuracy=accuracy,
                    download_filename=filename,
                    filetext=text
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
    """
    Examples page of website.
    Provides links to several example outputs of the application.

    URL Routes:

        * '/examples'

    :returns: template 'examples.html'
    """
    return render_template('examples.html')


@app.route('/examples/weights_off')
def example_weights_off():
    """
    Example of application output with "weights" turned off.

    URL Routes:

        * '/weights_off'

    :returns: template 'example_weights_off.html'
    """
    return render_template('example_weights_off.html')


@app.route('/examples/weights_on_accuracy_1')
def example_weights_on_acc_1():
    """
    Example of application output with "weights" turned on and
    "accuracy" set to 1.

    URL Routes:

        * '/weights_on_accuracy_1'

    :returns: template 'example_weights_on_acc_1.html'
    """
    return render_template('example_weights_on_acc_1.html')


@app.route('/examples/weights_on_accuracy_2')
def example_weights_on_acc_2():
    """
    Example of application output with "weights" turned on and
    "accuracy" set to 2.

    URL Routes:

        * '/weights_on_accuracy_2'

    :returns: template 'example_weights_on_acc_2.html'
    """
    return render_template('example_weights_on_acc_2.html')


@app.route('/examples/weights_on_accuracy_3')
def example_weights_on_acc_3():
    """
    Example of application output with "weights" turned on and
    "accuracy" set to 3.

    URL Routes:

        * '/weights_on_accuracy_3'

    :returns: template 'example_weights_on_acc_3.html'
    """
    return render_template('example_weights_on_acc_3.html')


@app.route('/examples/weights_on_accuracy_4')
def example_weights_on_acc_4():
    """
    Example of application output with "weights" turned on and
    "accuracy" set to 4.

    URL Routes:

        * '/weights_on_accuracy_4'

    :returns: template 'example_weights_on_acc_4.html'
    """
    return render_template('example_weights_on_acc_4.html')


@app.route('/examples/weights_on_accuracy_5')
def example_weights_on_acc_5():
    """
    Example of application output with "weights" turned on and
    "accuracy" set to 5.

    URL Routes:

        * '/weights_on_accuracy_5'

    :returns: template 'example_weights_on_acc_5.html'
    """
    return render_template('example_weights_on_acc_5.html')
