# configure and init app
from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

# file upload setup
from flask import request, redirect, url_for
ALLOWED_EXTENSIONS = set(['txt'])


# --- SERVICE ------------------------------------------
# configure and init RESTful library
from flask.ext import restful
from flask.ext.restful import Resource
api = restful.Api(app)

# add service handle
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/service')

from flask import render_template

# --- VIEWS --------------------------------------------
# add homepage handle
@app.route('/')
@app.route('/home')
def index():
	return render_template('pretty.html', title='GeoCoding Magic')

# def allowed_file(filename):
# 	return '.' in filename and \
# 		filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	return 'Banana!'

# 	if request.method == 'POST':
# 		file = request.files['file']
# 		if file and allowed_file(file.filename)
# 		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
# 		return redirect(url_for('uploaded_file', filename=filename))
# 	return "Banana"
# 	return '''
# 	<!doctype html>
# 	<title>Upload new File</title>
# 	<h1>Upload new File</h1>
# 	<form action="" method=post enctype=multipart/form-data>
# 		<p><input type=file name=file>
# 			<input type=submit value=Upload>
# 	</form>
# 	'''
