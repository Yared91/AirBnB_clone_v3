#!/usr/bin/python3
'''
    RESTful API for class State
'''
from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def state_all():
    '''
        return state in json form
    '''
    store = storage.all('State').values()
    state = [st.to_dict() for st in store]
    return jsonify(state)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_id(state_id):
    '''
        return state and its id using http verb GET
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
        delete state obj given state_id
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
        create new state obj
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
def update_state(states_id):
    '''
        update existing state object
    '''
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    obj = storage.get("State", states_id)
    if obj is None:
        abort(404)
    obj_data = request.get_json()
    obj.name = obj_data['name']
    obj.save()
    return jsonify(obj.to_dict()), 200
