#!/usr/bin/python3
"""Outlines the perspectives on managing places within the API"""
from api.v1.views import app_views
from flask import make_response, request, jsonify
from models import storage, storage_t
from models.place import Place
from models.city import City
from models.user import User
from werkzeug.exceptions import MethodNotAllowed, BadRequest, NotFound


@app_views.route("/cities/city_id/places", methods=['GET', 'POST'])
@app_views.route("/places/<place_id>", methods=['GET', 'DELETE', 'PUT'])
def place_handler(city_id=None, place_id=None):
    """Function to handle the places endpoint"""
    handlers = {
            'GET': get_Places,
            'DELETE': delete_Places,
            'POST': post_Places,
            'PUT': put_Places
    }
    if request.method in handlers:
        return handlers[request.method](city_id, place_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def get_Places(city_id=None, place_id=None):
    """Gets and retrieves all places or place based on ID"""
    if city_id:
        city_objt = storage.get(City, city_id)
        if city_objt:
            place_lists = list(city_objt.places)
            place_dict = list(map(lambda k: k.to_dict(), place_lists))
            return make_response(jsonify(place_dict), 200)
        raise NotFound()
    elif place_id:
        place_objt = storage.get(Place, place_id)
        if place_objt:
            return make_response(jsonify(place_objt.to_dict()), 200)
        raise NotFound()
    raise NotFound()


def delete_Places(city_id=None, place_id=None):
    """Deleting a place object based on ID"""
    if place_id:
        place_objt = storage.get(Place, place_id)
        if place_objt:
            storage.delete(place_objt)
            storage.save()
            return make_response(jsonify({}), 200)
    raise NotFound()


def post_Places(city_id=None, place_id=None):
    """Posting/adding new place to the object list"""
    city_objt = storage.get(City, city_id)
    if not city_objt:
        raise NotFound()
    place_data = request.get_json()
    if type(place_data) is not dict:
        raise BadRequest(description="Not a JSON")
    if "user_id" not in place_data:
        raise BadRequest(description="Missing user_id")
    user_objt = storage.get(User, place_data['user_id'])
    if not user_objt:
        raise NotFound()
    if "name" not in place_data:
        raise BadRequest(description="Missing name")
    place_data['city_id'] = city_id
    created_place = Place(**place_data)
    created_place.save()
    return make_response(jsonify(created_place.to_dict()), 201)


def put_Places(city_id=None, place_id=None):
    """Putting/updating place based on ID"""
    immut_attrbs = ("id", "user_id", "city_id", "created_at", "updated_at")
    place_objt = storage.get(Place, place_id)
    if place_objt:
        place_data = request.get_json()
        if type(place_data) is not dict:
            raise BadRequest(description="Not a JSON")
        for key, value in place_data.items():
            if key not in immut_attrbs:
                setattr(place_objt, key, value)
        place_objt.save()
        return make_response(jsonify(place_objt.to_dict()), 200)
    raise NotFound()


@app_views.route("/places_search", methods=['POST'])
def post_Places_Search():
    """Posting/adding place based on IDs of state, city or amenity"""
    reqdata = request.get_json()
    if type(reqdata) is not dict:
        raise BadRequest(description="Not a JSON")
    places_objt = storage.all(Place).values()
    places = []
    places_id = []
    data_stat = (
            all([
                "states" in reqdata and type(reqdata["states"]) is list,
                "states" in reqdata and len(reqdata["states"])
            ]),
            all([
                "cities" in reqdata and type(reqdata["cities"]) is list,
                "cities" in reqdata and len(reqdata["cities"])
            ]),
            all([
                "amenities" in reqdata and type(reqdata["amenities"]) is list,
                "amenities" in reqdata and len(reqdata["amenities"])
            ])
    )
    if data_stat[0]:
        for state_id in reqdata["states"]:
            if not state_id:
                continue
            state_objt = storage.get(State, state_id)
            if not state_objt:
                continue
            for city_objt in state_objt.cities:
                filtr_places = []
                if storage_t == 'db':
                    filtr_places = list(
                            filter(lambda k: k.id not in places_id,
                                   city_objt.places)
                    )
                else:
                    filtr_places = []
                    for place in places_objt:
                        if place.id in places_id:
                            continue
                        if place.city_id == city_objt.id:
                            filtr_places.append(place)
                places.extend(filtr_places)
                places_id.extend(list(map(lambda k: k.id, filtr_places)))
    if data_stat[1]:
        for city_id in reqdata["cities"]:
            if not city_id:
                continue
            city_objt = storage.get(City, city_id)
            if city_objt:
                filtr_places = []
                if storage_t == 'db':
                    filtr_places = list(
                            filter(lambda k: k.id not in places_id,
                                   city_objt.places)
                    )
                else:
                    filtr_places = []
                    for place in places_objt:
                        if place.id in places_id:
                            continue
                        if place.city_id == city_objt.id:
                            filtr_places.append(place)
                places.extend(filtr_places)
    del places_id
    if all([not data_stat[0], not data_stat[1]]) or not reqdata:
        places = places_objt
    if data_stat[2]:
        amenity_ids = []
        for amenity_id in reqdata["amenities"]:
            if not amenity_id:
                continue
            amenity_objt = storage.get(Amenity, amenity_id)
            if amenity_objt and amenity.id not in amenity_ids:
                amenity_ids.append(amenity_objt.id)
        delete_places = []
        for place in places:
            place_amenities_ids = list(map(lambda k: k.id, place.amenities))
            if not amenity_ids:
                continue
            for amenity_id in amenity_ids:
                if amenity_id not in place_amenities_ids:
                    delete_places.append(place.id)
                    break
        places = list(filter(lambda k: k.id not in delete_places, places))
    places_data = []
    for place in places:
        place_dict = place.to_dict()
        if "amenities" in place_dict:
            del place_dict["amenities"]
        places_data.append(place_dict)
    return make_response(jsonify(places_data))
