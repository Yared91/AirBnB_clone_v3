#!/usr/bin/python3
"""
Create a Amenity objects that handles all default RESTFul API actions
"""

from flask import Flask, jsonify
from flask import request, abort
from api.v1.views import app_views, storage
from models.amenity import Amentity


@app_views.route("/amenities", methods=["GET"])
def amenity_all():
    """
    Retrieves the list of all Amenity objects
    """
    amenities = [amenity.to_json() for amenity in storage.all("Amenity").values()]
    return jsonify(amenities)


@app_views.route("/amenities/<amenity_id>", methods=["GET"])
def amenity_id():
    """
    Check if amenity_id is connected to State object
    """
    amenity_obj = storage.get("Amenity", amenity_id)

    if amenity_obj:
        return jsonify(amenity_obj.to_json()), 200
    else:
        abort(404)


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"])
def amenity_delete():
    """
    Deletes Amenity objects that has amenity_id
    """
    amenity_obj = storage.get("Amenity", amenity_id)

    if amenity_obj:
        storage.delete(amenity_obj)
        storage.save()

        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/amenities", methods=["POST"])
def amenity_post():
    """
    Creates or adds a new amenity
    """
    post = request.get_json()

    if post is None:
        abort(400, 'Not a JSON')
    elif post.get("name") is None:
        abort(400, 'Missing name')
    else:
        new_post = Amenity(**post)
        new_post.save()

    return jsonify(new_post.to_json()), 201


@app_views.route("/amenities/<amenity_id>",  methods=["PUT"])
def amenity_put():
    """
    Updates a Amenity object by ID
    Args:
    amenity_id (str): The ID of the Amenity object to update
    Returns:
    JSON: The updated Amenity object (200) or error message
    """
    amenity_data = request.get_json()

    if not amenity_data:
        abort(400, 'Not a JSON')

    amenity_obj = storage.get("Amenity", amenity_id)

    if not amenity_obj:
        abort(400)

    am = amenity_data.items()
    keys = ["id", "created_at", "updated_at"]
    fields = {key: val for key, val in am if key not in keys}

    """Update object attributes efficiently and save"""
    fetched_obj.__dict__.update(**fields)
    fetched_obj.save()

    return jsonify(fetched_obj.to_json()), 200
