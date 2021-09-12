import logging

from werkzeug.exceptions import HTTPException

from app import create_app
from app.exceptions import APIException, Code404

app = create_app()


@app.errorhandler(Exception)
def framework_error(e):
    app.logger.exception(e)
    if isinstance(e, APIException):
        return e
    if isinstance(e, HTTPException):
        return APIException()
    else:
        return Code404('try harder...')


if __name__ == '__main__':
    app.run(debug=True, port=5000)


if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
