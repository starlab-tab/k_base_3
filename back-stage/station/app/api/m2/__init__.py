from flask import Blueprint
from app.api.m2 import auth, blog, crawler, message, sec


def create_blueprint_m2():
    bp_m2 = Blueprint('m2', __name__)
    auth.api.register(bp_m2)
    blog.api.register(bp_m2)
    crawler.api.register(bp_m2)
    message.api.register(bp_m2)
    sec.api.register(bp_m2)

    return bp_m2
