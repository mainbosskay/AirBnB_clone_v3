#!/usr/bin/python3
"""Outlines the perspectives on managing Amenity within the API"""
from api.v1.views import app_views
from flask import make_response, jsonify, request
from models import storage
from models.amenity import Amenity
from werkzeug.exceptions import MethodNotAllowed, BadRequest, NotFound


@app_views.route("/amenities", methods=['GET', 'POST'])
@app_views.route("/amenities/<amenity_id>", methods=['GET', 'DELETE', 'POST'])
def amenity_handler(amenity_id=None):
    """Function to handle the Amenity endpoint"""
    handlers = {
            'GET': get_Amenities,
            'DELETE': delete_Amenities,
            'POST': post_Amenities,
            'PUT': put_Amenities
    }
    if request.method in handlers:
        return handlers[request.method](amenity_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def get_Amenities(amenity_id=None):
    """Gets and retrieves all amenities or amenity based on ID"""
    amenity_objt = storage.all(Amenity).values()
    if amenity_id:
        amenity_lsts = list(filter(lambda k: k.id == amenity_id, amenity_objt))
        if amenity_list:
            return make_response(jsonify(amenity_lsts[0].to_dict()))
        raise NotFound()
    amenity_objt = list(map(lambda k: k.to_dict(), amenity_objt))
    return make_response(jsonify(amenity_objt))


def delete_Amenities(amenity_id=None):
    """Deleting amenity object based on amenity ID"""
    amenity_objt = storage.all(Amenity).values()
    amenity_lists = list(filter(lambda k: k.id == amenity_id, amenity_objt))
    if amenity_lists:
        storage.delete(amenity_list[0])
        storage.save()
        return make_response(jsonify({}), 200)
    raise NotFound()


def post_Amenities(amenity_id=None):
    """Posting and adding new amenity to object list"""
    amenity_data = request.get_json()
    if type(amenity_data) is not dict:
        raise BadRequest(description="Not a JSON")
    if "name" not in amenity_data:
        raise BadRequest(description="Missing name")
    created_amenity = Amenity(**amenity_data)
    created_amenity.save()
    return make_response(jsonify(created_amenity.to_dict()), 201)


def put_Amenities(amenity_id=None):
    """Putting/updating amenity based on ID"""
    immut_attrbs = ("id", "created_at", "updated_at")
    amenity_objt = storage.all(Amenity).values()
    amenity_lists = list(filter(lambda k: k.id == amenity_id, amenity_objt))
    if amenity_lists:
        amenity_data = request.get_json()
        if type(amenity_data) is not dict:
            raise BadRequest(description="Not a JSON")
        pre_amenity = amenity_lists[0]
        for key, value in amenity_data.items():
            if key not in immut_attrbs:
                setattr(pre_amenity, key, value)
        pre_amenity.save()
        return make_response(jsonify(pre_amenity.to_dict()), 200)
    raise NotFound()
