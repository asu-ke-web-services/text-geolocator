# -*- coding: utf-8 -*-

from flask import render_template, request, jsonify
from app import app

import nlp_magic
import geojson_maker


# add homepage handle

@app.route('/')
@app.route('/home')
def Index():
    return render_template('index.html', title='GeoCoding Magic')


# For a given file, return whether it's an allowed type or not

def AllowedFile(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] \
        in app.config['ALLOWED_EXTENSIONS']


# handle for uploading files

@app.route('/upload', methods=['GET', 'POST'])
def UploadFile():
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

            # tokens = nltk.word_tokenize(text)
            # return tokens
            # nlp_results = nlp_magic.nlp_geo_magic(text)

            locations = nlp_magic.FindLocations(text)
            geojson_collection = \
                geojson_maker.MakeGeoJsonCollection(locations)
            return jsonify(**geojson_collection)
    return '''<!doctype html><title>Upload new File</title><body>
           <p>No uploaded file detected.</p></body>'''
