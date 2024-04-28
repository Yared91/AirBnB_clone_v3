#!/usr/bin/python3
"""
Create a Users objects that handles all default RESTFul API actions
"""

from flask import Flask, jsonify
from flask import request, abort
from api.v1.views import app_views, storage
from models.state import State
from models.user import User


@app_views.route("/users", methods=["GET"])
def user_all():
    """
    Retrieves the list of all User objects
    """
    users = [user.to_json() for user in storage.all("User").values()]
    return jsonify(users)


@app_views.route("/users/<user_id>", methods=["GET"])
def user_id():
    """
    Check if user_id is connected to User object
    """
    user_obj = storage.get("User", user_id)

    if user_obj:
        return jsonify(user_obj.to_json()), 200
    else:
        abort(404)


@app_views.route("/users/<user_id>", methods=["DELETE"])
def user_delete():
    """
    Deletes user objects that has user_id
    """
    user_obj = storage.get("User", user_id)

    if user_obj:
        storage.delete(user_obj)
        storage.save()

        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/users", methods=["POST"])
def user_post():
    """
    Creats or adds a new user
    """
    post = request.get_json()

    if post is None:
        abort(400, 'Not a JSON')
    elif post.get("email") is None:
        abort(400, 'Missing email')
    elif post.get("password") is None:
        abort(400, 'Missing password')
    else:
        new_post = User(**post)
        new_post.save()

    return jsonify(new_post.to_json()), 201


@app_views.route("/users/<user_id>",  methods=["PUT"])
def user_put():
    """
    Updates a user object by ID
    Args:
    user_id (str): The ID of the user object to update
    Returns:
    JSON: The updated user object (200) or error message
    """
    user_data = request.get_json()

    if not user_data:
        abort(400, 'Not a JSON')

    user_obj = storage.get("User", user_id)

    if not user_obj:
        abort(400)

    st = user_data.items()
    keys = ["id", "created_at", "updated_at"]
    fields = {key: val for key, val in st if key not in keys}

    """Update object attributes efficiently and save"""
    fetched_obj.__dict__.update(**fields)
    fetched_obj.save()

    return jsonify(fetched_obj.to_json()), 200
