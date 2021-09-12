from flask_jwt_extended import JWTManager, create_access_token

from app.exceptions import Code401

jwt = JWTManager()


def create_jwt_token(ident):
    return create_access_token(identity=ident)


# https://flask-jwt-extended.readthedocs.io/en/latest/changing_default_behavior/
# https://flask-jwt-extended.readthedocs.io/en/stable/_modules/flask_jwt_extended/jwt_manager/
@jwt.invalid_token_loader
def reset_invalid_token_loader(jwt_payload):
    return Code401(msg="Token has expired")
