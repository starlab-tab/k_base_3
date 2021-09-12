import base64
import secrets
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from flask import jsonify, request
from flask_jwt_extended import get_jwt
from app.exceptions import Code404
from app.forms import AuthForm
from app.libs.m2print import M2print
from app.libs.redis import redis_client, ip_limiter
from app.models import Neddle, db, TokenBlocklist, MalIp
from app.token import create_jwt_token

api = M2print('auth')


def public_endpoint(function):
    function.is_public = True
    return function

@api.route('/init', methods=['GET'])
@ip_limiter()
@public_endpoint
def init_auth():
    ip = request.remote_addr
    pub_key = redis_client.get(f'{ip}_pub_key')
    if not pub_key:
        pri_key, pub_key = generate_asymmetric()
        redis_client.set(f'{ip}_pub_key', pub_key, ex=30)
        redis_client.set(f'{ip}_pri_key', pri_key, ex=30)
    return jsonify(key=base64.b64encode(pub_key).decode()), 200


@api.route('', methods=['POST'])
@ip_limiter()
@public_endpoint
def auth():
    valid_form = AuthForm().validate_for_api()
    ip = request.remote_addr
    pri_key = redis_client.get(f'{ip}_pri_key')
    if pri_key:
        raw_ident = valid_asymmetric(pri_key, valid_form['ident'])
        raw_auth = valid_asymmetric(pri_key, valid_form['auth'])
        neddle = Neddle.query.filter(Neddle.ident == raw_ident).first_or_404()
        if neddle.valid_auth(raw_auth):
            redis_client.delete(ip, f'{ip}_pri_key', f'{ip}_pub_key')
            return jsonify(access_token=create_jwt_token(neddle.id), language=secrets.token_urlsafe(8)), 200
    return Code404()


def valid_asymmetric(raw_key, encrypted):
    try:
        encrypted = base64.b64decode(encrypted)
        private_key = serialization.load_pem_private_key(
            raw_key,
            password=None,
            backend=default_backend()
        )
        decrypted = private_key.decrypt(
            encrypted,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return str(decrypted, "utf-8")
    except ValueError as e:
        raise Code404()


def generate_asymmetric():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    pri_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    pub_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return pri_key, pub_key


@api.route('', methods=['GET'])
def de_auth():
    jti = get_jwt()["jti"]
    with db.auto_commit():
        db.session.add(TokenBlocklist(jti=jti))
        return jsonify(msg='done'), 200
