#!/usr/bin/python3
"""
Create a City objects that handles all default RESTFul API actions
"""

from flask import Flask, jsonify
from flask import request, abort
from api.v1.views import app_views, storage
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"])
def city_all():
    """
    Retrieves the list of all City objects
    """
    cities = [state.to_json() for state in storage.all("State").values()]
    return jsonify(cities)


@app_views.route("/cities/<city_id>", methods=["GET"])
def city_id():
    """
    Check if state_id is connected to City object
    """
    city_obj = storage.get("City", city_id)

    if city_obj:
        return jsonify(city_obj.to_json()), 200
    else:
        abort(404)


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def city_delete():
    """
    Deletes City objects that has state_id
    """
    city_obj = storage.get("City", city_id)

    if city_obj:
        storage.delete(city_obj)
        storage.save()

        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def city_post():
    """
    Creates or adds a new city
    """
    post = request.get_json()

    if post is None:
        abort(400, 'Not a JSON')
    elif post.get("name") is None:
        abort(400, 'Missing name')
    else:
        new_post = City(**post)
        new_post.save()

    return jsonify(new_post.to_json()), 201


@app_views.route("/cities/<city_id>",  methods=["PUT"])
def city_put():
    """
    Updates a City object by ID
    Args:
    city_id (str): The ID of the City object to update
    Returns:
    JSON: The updated City object (200) or error message
    """
    city_data = request.get_json()

    if not city_data:
        abort(400, 'Not a JSON')

    city_obj = storage.get("City", city_id)

    if not city_obj:
        abort(400)

    ct = city_data.items()
    keys = ["id", "created_at", "updated_at"]
    fields = {key: val for key, val in ct if key not in keys}

    """Update object attributes efficiently and save"""
    fetched_obj.__dict__.update(**fields)
    fetched_obj.save()

    return jsonify(fetched_obj.to_json()), 200
