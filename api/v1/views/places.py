#!/usr/bin/python3
"""
Create a Place objects that handles all default RESTFul API actions
"""

from flask import Flask, jsonify
from flask import request, abort
from api.v1.views import app_views, storage
from models.place import Place


@app_views.route("/cities/<city_id>/places", methods=["GET"])
def place_all():
    """
    Retrieves the list of all Place objects
    """
    places = [place.to_json() for place in storage.all("Place").values()]
    return jsonify(places)


@app_views.route("/places/<place_id>", methods=["GET"])
def place_id():
    """
    Check if place_id is connected to Place object
    """
    place_obj = storage.get("Place", place_id)

    if place_obj:
        return jsonify(place_obj.to_json()), 200
    else:
        abort(404)


@app_views.route("/places/<place_id>", methods=["DELETE"])
def place_delete():
    """
    Deletes Place objects that has place_id
    """
    place_obj = storage.get("Place", place_id)

    if place_obj:
        storage.delete(place_obj)
        storage.save()

        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/cities/<city_id>/places", methods=["POST"])
def place_post():
    """
    Creates or adds a new place
    """
    post = request.get_json()

    if post is None:
        abort(400, 'Not a JSON')
    elif post.get("name") is None:
        abort(400, 'Missing name')
    else:
        new_post = Place(**post)
        new_post.save()

    return jsonify(new_post.to_json()), 201


@app_views.route("/places/<place_id>",  methods=["PUT"])
def place_put():
    """
    Updates a Place object by ID
    Args:
    place_id (str): The ID of the Place object to update
    Returns:
    JSON: The updated Place object (200) or error message
    """
    place_data = request.get_json()

    if not place_data:
        abort(400, 'Not a JSON')

    place_obj = storage.get("Place", place_id)

    if not place_obj:
        abort(400)

    pl = place_data.items()
    keys = ["id", "created_at", "updated_at"]
    fields = {key: val for key, val in pl if key not in keys}

    """Update object attributes efficiently and save"""
    fetched_obj.__dict__.update(**fields)
    fetched_obj.save()

    return jsonify(fetched_obj.to_json()), 200
