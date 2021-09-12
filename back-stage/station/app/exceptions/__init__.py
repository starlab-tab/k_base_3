from flask import request, json, jsonify
from werkzeug.exceptions import HTTPException


class APIException(HTTPException):
    code = 404
    msg = 'Oops, Something Went Wrong'

    def __init__(self, msg=None, code=None, headers=None):
        if code:
            self.code = code
        if msg:
            self.msg = msg
        super(APIException, self).__init__(msg, None)

    def get_body(self, environ=None):
        body = dict(
            msg=self.msg,
        )
        return json.dumps(body)

    def get_headers(self, environ=None):
        return [('Content-Type', 'application/json')]


class FakeCode200(APIException):
    code = 200
    msg = 'oops'


class Code400(APIException):
    code = 400
    msg = 'invalid param'


class Code401(APIException):
    code = 401
    msg = 'Permission Denied'


class Code404(APIException):
    code = 404
    msg = 'Not Found'


class Code500(APIException):
    code = 500
    msg = 'Oops, Something Went Wrong'
