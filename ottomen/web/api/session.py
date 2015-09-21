from flask import Blueprint, request, jsonify
from ...algorithm.session import new_batch, start_session
from ...core import json_schema
from . import route

bp = Blueprint('session', __name__, url_prefix='/session')


@route(bp, '/', methods=['POST'])
@json_schema.validate('session', 'start')
def start():
    json = request.get_json(force=True)
    print json
    worker_id = json["session"]['worker_id'].encode('ascii', 'ignore')
    if worker_id != json["session"]['worker_id'].encode('ascii', 'replace'):
        raise ValueError

    response = start_session(worker_id, '1337')
    if response is None:
        return {'error': 'task is closed'}

    return response


@route(bp, '/<session_id>', methods=['PUT'])
@json_schema.validate('session', 'get_questions')
def get_questions(session_id):
    json = request.get_json()
    print json
    batch = new_batch(json["session"]['worker_id'],
                      json["answers"],
                      json["session"]["task_id"],
                      session_id)

    return batch
