
from flask import Blueprint
from app.api.v2 import art, blog, message, music, show, sec


def create_blueprint_v2():
    bp_v2 = Blueprint('v2', __name__)
    message.api.register(bp_v2)
    art.api.register(bp_v2)
    blog.api.register(bp_v2)
    music.api.register(bp_v2)
    show.api.register(bp_v2)
    sec.api.register(bp_v2)

    return bp_v2
