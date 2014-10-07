from flask import Flask
from flask.ext import restful
from app.app import HelloWorld

app = Flask(__name__)
api = restful.Api(app)
api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
