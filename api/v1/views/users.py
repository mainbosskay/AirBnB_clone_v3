#!/usr/bin/python3
"""Outlines perspectives on managing users within API"""
from api.v1.views import app_views
from flask import make_response, request, jsonify
from models import storage
from models.user import User
from werkzeug.exceptions import MethodNotAllowed, BadRequest, NotFound


@app_views.route("/users", methods=['GET', 'POST'])
@app_views.route("/users/<user_id>", methods=['GET', 'DELETE', 'PUT'])
def user_handler(user_id=None):
    """Function to handle the userss endpoint"""
    handlers = {
            'GET': get_Users,
            'DELETE': delete_Users,
            'POST': post_Users,
            'PUT': put_Users
    }
    if request.method in handlers:
        return handlers[request.method](user_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def get_Users(user_id=None):
    """Gets and retrieves all users or user based on ID"""
    user_objt = storage.all(User).values()
    if user_id:
        user_lists = list(filter(lambda k: k.id == user_id, user_objt))
        if user_lists:
            return make_response(jsonify(user_lists[0].to_dict()))
        raise NotFound()
    user_objt = list(map(lambda k: k.to_dict(), user_objt))
    return make_response(jsonify(user_objt))


def delete_Users(user_id=None):
    """Deleting user object based on ID"""
    user_objt = storage.all(User).values()
    user_lists = list(filter(lambda k: k.id == user_id, user_objt))
    if user_lists:
        storage.delete(user_lists[0])
        storage.save()
        return make_response(jsonify({}), 200)
    raise NotFound()


def post_Users(user_id=None):
    """Posting/adding new user to object list"""
    user_data = request.get_json()
    if type(user_data) is not dict:
        raise BadRequest(description="Not a JSON")
    if "email" not in user_data:
        raise BadRequest(description="Missing email")
    if "password" not in user_data:
        raise BadRequest(description="Missing password")
    created_user = User(**user_data)
    created_user.save()
    return make_response(jsonify(created_user.to_dict()), 201)


def put_Users(user_id=None):
    """Putting/updating user based on ID"""
    immut_attrbs = ("id", "email", "created_at", "updated_at")
    user_objt = storage.all(User).values()
    user_lists = list(filter(lambda k: k.id == user_id, user_objt))
    if user_lists:
        user_data = request.get_json()
        if type(user_data) is not dict:
            raise BadRequest(description="Not a JSON")
        pre_user = user_lists[0]
        for key, value in user_data.items():
            if key not in immut_attrbs:
                setattr(pre_user, key, value)
        pre_user.save()
        return make_response(jsonify(pre_user.to_dict()), 200)
    raise NotFound()
