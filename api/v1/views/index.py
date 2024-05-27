#!/usr/bin/python3
"""API index view of the web application"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status")
def getStatus():
    """Getting and returns the status of API"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def getStats():
    """Getting and returns the number of objects based off type"""
    objects = {
            "amenities": 'Amenity',
            "cities": 'City',
            "places": 'Place',
            "reviews": 'Review',
            "states": 'State',
            "users": 'User'
    }
    for key, val in objects.items():
        objects[key] = storage.count(val)
    return jsonify(objects)
