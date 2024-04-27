#!/usr/bin/python3
"""
Create a Review objects that handles all default RESTFul API actions
"""

from flask import Flask, jsonify
from flask import request, abort
from api.v1.views import app_views, storage
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=["GET"])
def place_review():
    """
    Retrieves the list of all place review
    """
    place_rev = [review.to_json() for reviews in storage.all("Place").values()]
    return jsonify(place_rev)


@app_views.route("/reviews/<review_id>", methods=["GET"])
def review_id():
    """
    Check if review_id is connected to place object
    """
    review_obj = storage.get("Review", review_id)

    if review_obj:
        return jsonify(review_obj.to_json())
    else:
        abort(404)


@app_views.route("/reviews/<review_id>", methods=["DELETE"])
def review_delete():
    """
    Deletes Review objects that has review_id
    """
    review_obj = storage.get("Review", review_id)

    if review_obj:
        storage.delete(review_obj)
        storage.save()

        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/places/<place_id>/reviews", methods=["POST"])
def review_post():
    """
    Creats or adds a new review
    """
    post = request.get_json()

    if post is None:
        abort(400, 'Not a JSON')
    elif post.get("name") is None:
        abort(400, 'Missing name')
    elif not storage.get("Place", place_id):
        abort(400)
    elif post.get("user_id") is None:
        abort(400, 'Missing user_id')
    elif post.get("text") is None:
        abort(400, 'Missing text')
    elif not storage.get("User", review_json["user_id"]):
        abort(404)
    else:
        new_post = Review(**post)
        new_post.save()

    return jsonify(new_post.to_json()), 201


@app_views.route("/reviews/<review_id>",  methods=["PUT"])
def review_put():
    """
    Updates a review object by ID
    Args:
    review_id (str): The ID of the review object to update
    Returns:
    JSON: The updated review object (200) or error message
    """
    review_data = request.get_json()

    if not review_data:
        abort(400, 'Not a JSON')

    review_obj = storage.get("Review", review_id)

    if not review_obj:
        abort(400)

    rv = review_data.items()
    keys = ["id", "created_at", "updated_at"]
    fields = {key: val for key, val in rv if key not in keys}

    """Update object attributes efficiently and save"""
    fetched_obj.__dict__.update(**fields)
    fetched_obj.save()

    return jsonify(fetched_obj.to_json()), 200
