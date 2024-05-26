#!/usr/bin/python3
"""Outlines perspectives on managing cities within API"""
from api.v1.views import app_views
from flask import jsonify, make_response, request
from models.city import City
from models.state import State
from models import storage, storage_t
from werkzeug.exceptions import MethodNotAllowed, BadRequest, NotFound


@app_views.route("/states/<state_id>/cities", methods=['GET', 'POST'])
@app_views.route("/cities/<city_id>", methods=['GET', 'DELETE', 'PUT'])
def city_handler(state_id=None, city_id=None):
    """Function to handle the cities endpoint"""
    handlers = {
            'GET': get_Cities,
            'DELETE': delete_Cities,
            'POST': post_Cities,
            'PUT': put_Cities
    }
    if request.method in handlers:
        return handlers[request.method](state_id, city_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def get_Cities(state_id=None, city_id=None):
    """Gets and retrieves cities or city based on ID"""
    if state_id:
        state_lists = storage.get(State, state_id)
        if state_lists:
            cty_in_stts = list(map(lambda k: k.to_dict(), state_lists.cities))
            return make_response(jsonify(cty_in_stts))
    elif city_id:
        city_lists = storage.get(City, city_id)
        if city_lists:
            return make_response(jsonify(city_lists.to_dict()))
    raise NotFound()


def delete_Cities(state_id=None, city_id=None):
    """Deleting state object based on ID"""
    if city_id:
        city_lists = storage.get(City, city_id)
        if city_lists:
            storage.delete(city_lists)
            storage.save()
            return make_response(jsonify({}), 200)
    raise NotFound()


def post_Cities(state_id=None, city_id=None):
    """Posting/adding new city to object list"""
    state_lists = storage.get(State, state_id)
    if not state_lists:
        raise NotFound()
    city_data = request.get_json()
    if type(city_data) is not dict:
        raise BadRequest(description="Not a JSON")
    if "name" not in city_data:
        raise BadRequest(description="Missing name")
    city_data["state_id"] = state_id
    created_city = City(**city_data)
    created_city.save()
    return make_response(jsonify(created_city.to_dict()), 201)


def put_Cities(state_id=None, city_id=None):
    """Putting or updating state based on ID"""
    immut_attrbs = ("id", "state_id", "created_id", "updated_at")
    if city_id:
        city_list = storage.get(City, city_id)
        if city_lists:
            city_data = request.get_json()
            if type(city_data) is not dict:
                raise BadRequest(description="Not a JSON")
            for key, value in city_data.items():
                if key not in immut_attrbs:
                    setattr(city_lists, key, value)
            city_lists.save()
            return make_response(jsonify(city_lists.to_dict()), 200)
    raise NotFound()
