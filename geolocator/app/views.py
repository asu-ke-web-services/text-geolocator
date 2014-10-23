from flask import render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
from app import app

import os
import nlp_magic


# add homepage handle
@app.route('/')
@app.route('/home')
def index():
	return render_template('index.html', title='GeoCoding Magic')

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# handle for uploading files
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		uploadedfile = request.files['file']
		if uploadedfile and allowed_file(uploadedfile.filename):
			# this is supposed to save file to /tmp/uploads
			# ---------------------------------------------------------------
			# filename = secure_filename(uploadedfile.filename)
			# uploadedfile_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			# with open(uploadedfile_path, 'wb') as f:
			# 	f.write(uploadedfile.read())
			# return redirect(url_for('uploaded_file', filename=filename)) 
			text = uploadedfile.read()
			# tokens = nltk.word_tokenize(text)
			# return tokens
			# nlp_results = nlp_magic.nlp_geo_magic(text)
			nlp_results = nlp_magic.stanford_nlp_location_magic(text)
			return nlp_results
	return '''
	<!doctype html>
	<title>Upload new File</title>
	'''
