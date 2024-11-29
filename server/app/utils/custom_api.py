from flask_restful import Api as _Api, HTTPException

class Api(_Api):
    """
    Overriden Custom Flask API class to keep Flask-RESTful
    from handling errors other than HTTPException ones.
    https://stackoverflow.com/questions/56049481/why-is-my-flask-error-handler-not-being-called
    """
    def error_router(self, original_handler, e):
        # Override original error_router to only handle HTTPExceptions.
        if self._has_fr_route() and isinstance(e, HTTPException):
            try:
                # Use Flask-RESTful's error handling method
                return self.handle_error(e) 
            except Exception:
                # Fall through to original handler (i.e. Flask)
                pass
        return original_handler(e)