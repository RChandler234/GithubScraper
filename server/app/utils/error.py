from flask import jsonify


def handle_custom_exception(error):
    """
    Error Handler for Custom Server Exceptions
    """
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def handle_not_found_error(error):
    """
    Error Handler for 404 Exceptions, so JSON is returned instead of HTML
    """
    response = jsonify({"error": "Not Found", "status_code": 404})
    response.status_code = 404
    return response


def handle_internal_exception(err):
    """
    Error Handler for 500 Exceptions, so JSON is returned instead of HTML
    """
    if isinstance(err, ServerException):
        return None
    response = jsonify({"error": "Internal Server Error", "status_code": 500})
    response.status_code = 500
    return response


class ServerException(Exception):
    """
    Custom Server Exception for Error Handling
    """

    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        return {"error": self.message, "status_code": self.status_code}
