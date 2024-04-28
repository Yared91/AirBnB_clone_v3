#!/usr/bin/python3
'''
Create a State objects that handles all default RESTFul API actions
'''
from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', methods=['GET'])
def state_all():
    '''
        Retrieves the list of all State objects
    '''
    lists = [state.to_dict() for state in storage.all('State').values()]
    return jsonify(lists)


@app_views.route('/states/<state_id>', methods=['GET'])
def state_id(state_id):
    '''
        Check if state_id is connected to State object
    '''
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def state_delete(state_id):
    '''
        Deletes State objects that has state_id
    '''
    state_obj = storage.get("State", state_id)
    if state_obj is None:
        abort(404)
    state_obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def state_post():
    '''
        Creates or adds a new state
    '''
    new_post = request.get_json()
    if new_post is None:
        err = {"error": "Not a JSON"}
        return jsonify(err), 400
    elif "name" not in new_post:
        err1 = {"error": "Missing name"}
        return jsonify(err1), 400
    else:
        post = request.get_json()
        st = State(**post)
        st.save()
        return jsonify(st.to_dict()), 201


@app_views.route('/states/<states_id>', methods=['PUT'])
def update_state(states_id):
    '''
    Updates a State object by ID
    Args:
    state_id (str): The ID of the State object to update
    Returns:
    JSON: The updated State object (200) or error message
    '''
    new_post = request.get_json()
    if new_post is None:
        err2 = {"error": "Not a JSON"}
        return jsonify(err2), 400

    state_obj = storage.get("State", states_id)
    if state_obj is None:
        abort(404)
    post = request.get_json()
    state_obj.name = post['name']
    state_obj.save()
    return jsonify(state_obj.to_dict()), 200
