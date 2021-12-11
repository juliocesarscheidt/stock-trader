from flask_restful import Resource
from flask import make_response, jsonify


class BaseRoute(Resource):
    def get_status_from_code(self, status_code: int) -> str:
        if status_code == 200:
            return "OK"
        elif status_code == 201:
            return "Created"
        elif status_code == 202:
            return "Accepted"
        elif status_code == 204:
            return "No Content"
        elif status_code == 301:
            return "Moved Permanently"
        elif status_code == 302:
            return "Found"
        elif status_code == 400:
            return "Bad Request"
        elif status_code == 401:
            return "Unauthorized"
        elif status_code == 403:
            return "Forbidden"
        elif status_code == 404:
            return "Not Found"
        elif status_code == 422:
            return "Unprocessable Entity"
        elif status_code == 429:
            return "Too Many Requests"
        elif status_code == 500:
            return "Internal Server Error"

    def send_response(self, data, status_code: int = 200):
        response = jsonify(status=self.get_status_from_code(status_code), data=data)
        return make_response(response, status_code)
