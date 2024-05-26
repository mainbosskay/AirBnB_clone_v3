#!/usr/bin/python3
"""Outlines perspectives on managing states within the API"""
from api.v1.views import app_views
from flask import jsonify, make_response, request
from models import storage
from models.state import State
from werkzeug.exceptions import MethodNotAllowed, BadRequest, NotFound


@app_views.route("/states", methods=['GET', 'POST'])
@app_views.route("/states/<state_id>", methods=['GET', 'DELETE', 'PUT'])
def state_handler(state_id=None):
    """Function to handle the states endpoint"""
    handlers = {
            'GET': get_States,
            'DELETE': delete_States,
            'POST': post_States,
            'PUT': put_States
    }
    if request.method in handlers:
        return handlers[request.method](state_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def get_States(state_id=None):
    """Gets and retrieves all states or state based on ID"""
    state_objt = storage.all(State).values()
    if state_id:
        state_lists = list(filter(lambda k: k.id == state_id, state_objt))
        if state_lists:
            return make_response(jsonify(state_lists[0].to_dict()), 200)
        raise NotFound()
    state_objt = list(map(lambda k: k.to_dict(), state_objt))
    return make_response(jsonify(state_objt))


def delete_States(state_id=None):
    """Deleting a state object based on ID"""
    state_objt = storage.all(State).values()
    state_lists = list(filter(lambda k: k.id == state_id, state_objt))
    if state_lists:
        storage.delete(state_lists[0])
        storage.save()
        return make_response(jsonify({}), 200)
    raise NotFound()


def post_States(state_id=None):
    """Posting or adding new state to object list"""
    state_data = request.get_json()
    if type(state_data) is not dict:
        raise BadRequest(description="Not a JSON")
    if "name" not in state_data:
        raise BadRequest(description="Missing name")
    created_state = State(**state_data)
    created_state.save()
    return make_response(jsonify(created_state.to_dict()), 201)


def put_States(state_id=None):
    """Puttin or updating state based on ID"""
    immut_attrs = ("id", "created_at", "updated_at")
    state_objt = storage.all(State).values()
    state_lists = list(filter(lambda k: k.id == state_id, state_objt))
    if state_lists:
        state_data = request.get_json()
        if type(state_data) is not dict:
            raise BadRequest(description="Not a JSON")
        pre_state = state_list[0]
        for key, value in state_data.items():
            if key not in immut_attrs:
                setattr(pre_state, key, value)
        pre_state.save()
        return make_response(jsonify(pre_state.to_dict()), 200)
    raise NotFound()
