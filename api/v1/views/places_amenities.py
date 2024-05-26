#!/usr/bin/python3
"""Outlines perspectives on managing places_amenitiess within API"""
from api.v1.views import app_views
from flask import make_response, request, jsonify
from models import storage, storage_t
from models.amenity import Amenity
from models.place import Place
from werkzeug.exceptions import MethodNotAllowed, BadRequest, NotFound


@app_views.route("/places/place_id/amenities", methods=['GET'])
@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=['DELETE', 'POST'])
def places_amenities_handler(place_id=None, amenity_id=None):
    """Function to handle the places_amenities endpoint"""
    handlers = {
            'GET': get_Places_Amenities,
            'DELETE': delete_Places_Amenities,
            'POST': post_Places_Amenities
    }
    if request.method in handlers:
        return handlers[request.method](place_id, amenity_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def get_Places_Amenities(place_id=None, amenity_id=None):
    """Gets and retrieves amenity or amenities of place based on ID"""
    if place_id:
        place_objt = storage.get(Place, place_id)
        if place_objt:
            amenities_list = list(map(lambda k: k.to_dict(),
                                      place_objt.amenities))
            return make_response(jsonify(amenities_lists))
    raise NotFound()


def delete_Places_Amenities(place_id=None, amenity_id=None):
    """Deleting amenity from a place based on ID"""
    if place_id and amenity_id:
        place_objt = storage.get(Place, place_id)
        amenity_objt = storage.get(Amenity, amenity_id)
        if not place_objt or not amenity_objt:
            raise NotFound()
        place_link_amenity = list(
                filter(lambda k: k.id == amenity_id, place_objt.amenities)
        )
        if not place_link_amenity:
            raise NotFound()
        if storage_t == 'db':
            amenity_link_place = list(
                    filter(lambda k: k.id == place_id,
                           amenity_objt.place_amenites)
            )
            if not amenity_link_place:
                raise NotFound()
            place_objt.amenities.remove(amenity_objt)
            place_objt.save()
            return make_response(jsonify({}), 200)
        else:
            amenity_indx = place_objt.amenity_ids.index(amenity_id)
            place_objt.amenity_ids.pop(amenity_indx)
            place_objt.save()
            return make_response(jsonify({}), 200)
    raise NotFound()


def post_Places_Amenities(place_id=None, amenity_id=None):
    """Posting/adding amenity from a place based on ID"""
    if place_id and amenity_id:
        place_objt = storage.get(Place, place_id)
        amenity_objt = storage.get(Amenity, amenity_id)
        if not place_objt or not amenity_objt:
            raise NotFound()
        if storage_t == 'db':
            place_link_amenity = list(
                    filter(lambda k: k.id == amenity_id, place_objt.amenities)
            )
            amenity_link_place = list(
                    filter(lambda k: k.id == place_id,
                           amenity_objt.place_amenites)
            )
            if amenity_link_place and place_link_amenity:
                amenity_dict = amenity_objs.to_dict()
                del amenity_dict['place_amenities']
                return make_response(jsonify(amenity_dict), 200)
            place_objt.amenities.append(amenity_objs)
            place_objt.save()
            amenity_dict = amenity_objs.to_dict()
            del amenity_dict['place_amenities']
            return make_response(jsonify(amenity_dict), 201)
        else:
            if amenity_id in place_objt.amenity_ids:
                return make_response(jsonify(amenity_objt.to_dict()), 200)
            place_objt.amenity_ids.push(amenity_id)
            place_objt.save()
            return make_response(jsonify(amenity_objt.to_dict()), 201)
    raise NotFound()
