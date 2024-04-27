#!/usr/bin/python3
"""
Create a State objects that handles all default RESTFul API actions
"""

from flask import Flask, jsonify
from flask import request, abort
from api.v1.views import app_views, storage
from models.state import State
from models import storage


@app_views.route("/states", methods=["GET"])
def state_all():
    """
    Retrieves the list of all State objects
    """
    states = [state.to_json() for state in storage.all("State").values()]
    return jsonify(states)


@app_views.route("/states/<state_id>", methods=["GET"])
def state_id():
    """
    Check if state_id is connected to State object
    """
    state_obj = storage.get("State", state_id)

    if state_obj:
        return jsonify(state_obj.to_json())
    else:
        abort(404)


@app_views.route("/states/<state_id>", methods=["DELETE"])
def state_delete():
    """
    Deletes State objects that has state_id
    """
    state_obj = storage.get("State", state_id)

    if state_obj:
        storage.delete(state_obj)
        storage.save()

        return jsonify({})
    else:
        abort(404)


@app_views.route("/states", methods=["POST"])
def state_post():
    """
    Creats or adds a new state
    """
    post = request.get_json()

    if post is None:
        abort(400, 'Not a JSON')
    elif post.get("name") is None:
        abort(400, 'Missing name')
    else:
        new_post = State(**post)
        new_post.save()

    return jsonify(new_post.to_json()), 201


@app_views.route("/states/<state_id>",  methods=["PUT"])
def state_put():
    """
    Updates a State object by ID
    Args:
    state_id (str): The ID of the State object to update
    Returns:
    JSON: The updated State object (200) or error message
    """
    state_data = request.get_json()

    if not state_data:
        abort(400, 'Not a JSON')

    state_obj = storage.get("State", state_id)

    if not state_obj:
        abort(400)

    st = state_data.items()
    keys = ["id", "created_at", "updated_at"]
    fields = {key: val for key, val in st if key not in keys}

    """Update object attributes efficiently and save"""
    fetched_obj.__dict__.update(**fields)
    fetched_obj.save()

    return jsonify(fetched_obj.to_json())
