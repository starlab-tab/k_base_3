import logging

from app import create_app
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError
from werkzeug.exceptions import HTTPException
from app.exceptions import APIException, Code401, Code404
from flask import request
app = create_app()


@app.errorhandler(Exception)
def framework_error(e):
    app.logger.exception(e)
    if isinstance(e, APIException):
        return e
    if isinstance(e, HTTPException):
        code = e.code
        msg = e.description
        return APIException(msg=msg, code=code)
    else:
        return Code404()

@app.before_request
def before_request_func():
    if not request.endpoint: return Code404()
    try:
        if 'static' not in request.endpoint and not getattr(app.view_functions[request.endpoint], 'is_public', False):
            verify_jwt_in_request()
    except NoAuthorizationError as e:
        raise Code401()


if __name__ == '__main__':
    app.run(debug=True, port=4000)


if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)