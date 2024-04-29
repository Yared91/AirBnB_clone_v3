#!/usr/bin/python3
"""
Creating index
"""

from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
from flask import request


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
        keys = ["Amenity", "City", "Place", "Review", "State", "User"]
        response = {key.lower(): storage.count(key) for key in keys}
        return jsonify(response)
