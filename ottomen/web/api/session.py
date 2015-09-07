from flask import Blueprint, request, jsonify
from ...algorithm.session import new_batch, start_session
from . import route

bp = Blueprint('session', __name__, url_prefix='/session')


@route(bp, '/test')
def test():
    return "test"


@route(bp, '/', methods=['POST'])
def start():
    json = request.get_json(force=True)
    # Validation of the input data
    if 'turk_id' not in json['session']:
        return jsonify({'error': 'requires turk_id'})
    # if 'task_id' not in json["session"]:
    # return jsonify({'error': 'requires task_id'})

    response = start_session(json["session"]['turk_id'], '1000')
    if response is None:
        return jsonify({'error': 'task is closed'})

    return jsonify(response)


@route(bp, '/<session_id>', methods=['PUT'])
def get_questions(session_id):
    json = request.get_json()

    # Validation of the input data
    if 'turk_id' not in json['session']:
        return jsonify({'error': 'requires turk_id'})
    if 'task_id' not in json["session"]:
        return jsonify({'error': 'requires task_id'})
    if 'answers' not in json["session"]:
        return jsonify({'error': 'requires answers'})

    batch = new_batch(json["session"]['turk_id'],
                      json["session"]["answers"],
                      json["session"]["task_id"],
                      session_id)

    return jsonify(batch)