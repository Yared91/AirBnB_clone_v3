#!/usr/bin/python3
"""
Creating index
"""

from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
from flask import request
from .models import Amenity, City, Place, Review, State, User


@app_views.route('/status', methods=['GET'])
def status_ok():
    """
    returns status ok for the request GET
    """
    if request.method == 'GET':
        response = {
                "status": "OK"
                }
        output = jsonify(response)
        output.status_code = 200
        return output


@app_views.route('/stats', methods=['GET'])
def states():
    """
    Retrieves the count of all class objects and returns it as a JSON response
    Returns:
    JSON: A dictionary containing the count of each object type
    """

    if request.method == 'GET':
        response = {key.lower(): storage.count(cls) for key, cls in [
            ("amenity", Amenity), ("city", City), ("place", Place),
            ("review", Review), ("state", State), ("user", User)
            ]}
        return jsonify(response)
