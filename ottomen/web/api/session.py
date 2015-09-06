from flask import Blueprint
from . import route

bp = Blueprint('session', __name__, url_prefix='/session')


@route(bp, '/test')
def test():
    return "test"
