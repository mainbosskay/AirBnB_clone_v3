#!/usr/bin/python3
"""Outlines the perspectives on managing reviews within the API"""
from api.v1.views import app_views
from flask import make_response, request, jsonify
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from werkzeug.exceptions import MethodNotAllowed, BadRequest, NotFound


@app_views.route("/places/place_id/reviews", methods=['GET', 'POST'])
@app_views.route("/reviews/<review_id>", methods=['GET', 'DELETE', 'PUT'])
def review_handler(place_id=None, review_id=None):
    """Function to handle the reviews endpoint"""
    handlers = {
            'GET': get_Reviews,
            'DELETE': delete_Reviews,
            'POST': post_Reviews,
            'PUT': put_Reviews
    }
    if request.method in handlers:
        return handlers[request.method](place_id, review_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def get_Reviews(place_id=None, review_id=None):
    """Gets and retrieves all reviews or review based on ID"""
    if place_id:
        place_objt = storage.get(Place, place_id)
        if place_objt:
            reveiw_dict = [review.to_dict() for review in place_objt.reviews]
            return make_response(jsonify(review_dict))
        raise NotFound()
    elif review_id:
        review_objt = storage.get(Review, review_id)
        if review_objt:
            return make_response(jsonify(review_objt.to_dict()))
        raise NotFound()
    raise NotFound()


def delete_Reviews(place_id=None, review_id=None):
    """Deleting review object based on ID"""
    review_objt = storage.get(Review, review_id)
    if review_objt:
        storage.delete(review_objs)
        storage.save()
        return make_response(jsonify({}), 200)
    raise NotFound()


def post_Reviews(place_id=None, review_id=None):
    """Posting/adding new review to the object list"""
    place_objt = storage.get(Place, place_id)
    if not place_objt:
        raise NotFound()
    review_data = request.get_json()
    if type(review_data) is not dict:
        raise BadRequest(description="Not a JSON")
    if "user_id" not in review_data:
        raise BadRequest(description="Missing user_id")
    user_objt = storage.get(User, review_data['user_id'])
    if not user_objt:
        raise NotFound()
    if "text" not in review_data:
        raise BadRequest(description="Missing text")
    review_data['place_id'] = place_id
    created_review = Review(**review_data)
    created_review.save()
    return make_response(jsonify(created_review.to_dict()), 201)


def put_Reviews(place_id=None, review_id=None):
    """Putting/updating review based on ID"""
    immut_attrbs = ("id", "user_id", "place_id", "created_at", "updated_at")
    review_objt = storage.get(Review, review_id)
    if review_objt:
        review_data = request.get_json()
        if type(review_data) is not dict:
            raise BadRequest(description="Not a JSON")
        for key, value in review_data.items():
            if key not in immut_attrbs:
                setattr(review_objt, key, value)
        review_objt.save()
        return make_response(jsonify(review_objt.to_dict()), 200)
    raise NotFound()
