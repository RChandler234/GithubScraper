from flask import jsonify


def handle_custom_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def handle_not_found_error(error):
    response = jsonify({"error": "Not Found", "status_code": 404})
    response.status_code = 404
    return response


def handle_internal_exception(err):
    """Return JSON instead of HTML for any other server error"""
    if isinstance(err, ServerException):
        return None
    response = jsonify({"error": "Internal Server Error", "status_code": 500})
    response.status_code = 500
    return response


class ServerException(Exception):
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        return {"error": self.message, "status_code": self.status_code}
