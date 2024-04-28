#!/usr/bin/python3
'''
    Create a State objects that handles all default RESTFul API actions
'''
from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def state_all():
    '''
        Retrieves the list of all State objects
    '''
    store = storage.all('State').values()
    state = [st.to_dict() for st in store]
    return jsonify(state)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_id(state_id):
    '''
        Check if state_id is connected to State object
    '''
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route(
    '/states/<state_id>',
    methods=['DELETE'],
    strict_slashes=False)
def state_delete(state_id):
    '''
         Deletes State objects that has state_id
    '''
    state_obj = storage.get("State", state_id)
    if state_obj is None:
        abort(404)
    storage.delete(state_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def state_post():
    '''
        Creates or adds a new state
    '''
    req = request.get_json()
    if not req:
        return jsonify({"error": "Not a JSON"}), 400
    elif "name" not in req:
        return jsonify({"error": "Missing name"}), 400
    else:
        state_data = request.get_json()
        post = State(**state_data)
        post.save()
        return jsonify(post.to_dict()), 201


@app_views.route('/states/<states_id>', methods=['PUT'], strict_slashes=False)
def state_put(states_id):
    '''
        Updates a State object by Id
    '''
    req = request.get_json()
    if not req:
        return jsonify({"error": "Not a JSON"}), 400

    st = storage.get("State", states_id)
    if st is None:
        abort(404)
    state_obj = request.get_json()
    st.name = state_obj['name']
    st.save()
    return jsonify(st.to_dict()), 200
