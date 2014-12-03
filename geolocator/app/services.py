from flask.ext import restful
from flask.ext.restful import Resource
from app import app


api = restful.Api(app)


# add service handle
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/service')
