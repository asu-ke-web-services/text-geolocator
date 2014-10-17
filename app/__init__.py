# configure and init app
from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

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
