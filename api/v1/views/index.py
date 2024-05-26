#!/usr/bin/python3
"""API index view of the web application"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status")
def getStatus():
    """Getting and returns the status of API"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def getStats():
    """Getting and returns the number of objects based off type"""
    objt_types = {
            "amenities": 'Amenity',
            "cities": 'City',
            "places": 'Place',
            "reviews": 'Review',
            "states": 'State',
            "users": 'User'
    }
    for key, val in obj_types.items():
        objt_types[key] = storage.count(val)
    return jsonify(objt_types)
