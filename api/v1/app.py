#!/usr/bin/python3
"""The AirBnB API built with Flask web application"""
from os import getenv
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
from flask_cors import CORS


app = Flask(__name__)
"""Flask web application instance"""
app_host = getenv("HBNB_API_HOST", default="0.0.0.0")
app_port = int(getenv("HBNB_API_PORT", default=5000))
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
CORS(app, resources={"/*": {"origins": app_host}})


@app.teardown_appcontext
def close_storage(exception):
    """Closes SQLAlchemy connection in Flask context"""
    storage.close()


@app.errorhandler(404)
def page_404_error(error):
    """Handling page with error 404"""
    return jsonify(error="Not found"), 404


if __name__ == "__main__":
    app.run(host=app_host, port=app_port, threaded=True)
