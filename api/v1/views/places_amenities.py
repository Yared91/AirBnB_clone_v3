#!/usr/bin/python3
"""
Create a new view for the link between Place objects and Amenity objects
"""

from flask import jsonify, abort
from os import getenv
from api.v1.views import app_views, storage


@app_views.route("/places/<place_id>/amenities", methods=["GET"])
def amenity_place_id(place_id):
    """
    defines Amenity using place_id
    """
    fetched_obj = storage.get("Place", place_id)
    all_amenities = []

    if fetched_obj is None:
        abort(404)

    for obj in fetched_obj.amenities:
        all_amenities.append(obj.to_json())

    return jsonify(all_amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"])
def amenity_unlink(place_id, amenity_id):
    """
    unlinks an amenity in a place
    """
    if storage.get("Place", place_id) is None:
        abort(404)
    elif storage.get("Amenity", amenity_id) is None:
        abort(404)

    found = 0

    for obj in storage.get("Place", place_id).amenities:
        if obj.id == amenity_id:
            if getenv("HBNB_TYPE_STORAGE") == "db":
                storage.get("Place", place_id).amenities.remove(obj)
            else:
                storage.get("Place", place_id).amenity_ids.remove(obj.id)
            fetched_obj.save()
            found = 1
            break

    if found == 0:
        abort(404)
    else:
        output = jsonify({})
        output.status_code = 201
        return output


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"])
def amenity_link(place_id, amenity_id):
    """
    links a amenity with a place using the parameters place and amenity ids
    """

    amenity_obj = storage.get("Amenity", amenity_id)
    found_amenity = None

    if not storage.get("Place", place_id) or not amenity_obj:
        abort(404)

    for obj in storage.get("Place", place_id).amenities:
        if obj.id == amenity_id:
            found_amenity = obj
            break

    if found_amenity:
        return jsonify(found_amenity.to_json())

    if getenv("HBNB_TYPE_STORAGE") == "db":
        storage.get("Place", place_id).amenities.append(amenity_obj)
    else:
        storage.get("Place", place_id).amenities = amenity_obj

    storage.get("Place", place_id).save()

    resp = jsonify(amenity_obj.to_json())
    resp.status_code = 201

    return resp
