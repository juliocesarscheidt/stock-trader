from flask_restful import Resource
from flask import make_response, jsonify


class Health(Resource):
    def get(self):
        response = jsonify(status="OK", data={"message": "Success"})
        return make_response(response, 200)
