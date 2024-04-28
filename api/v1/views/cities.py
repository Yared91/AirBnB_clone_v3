#!/usr/bin/python3
'''
    Create a new view for City objects
'''
from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities_all(state_id):
    '''
        Retrieves the list of all City objects
    '''
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities]), 200


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_id(city_id):
    '''
        Retrieves a City object using GET
    '''
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict()), 200


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    '''
        Deletes a City object
    '''
    city_obj = storage.get("City", city_id)
    if city_obj is None:
        abort(404)
    storage.delete(city_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def city_post(state_id):
    '''
        create new city obj through state obj using post
    '''
    req = request.get_json()
    if not req:
        return jsonify({"error": "Not a JSON"}), 400
    elif "name" not in req:
        return jsonify({"error": "Missing name"}), 400
    else:
        city_obj = request.get_json()
        st = storage.get("State", state_id)
        if st is None:
            abort(404)
        city_obj['state_id'] = state.id
        post = City(**obj_data)
        post.save()
        return jsonify(post.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    '''
        create new city obj through state obj using put
    '''
    req = request.get_json()
    if not req:
        return jsonify({"error": "Not a JSON"}), 400

    st = storage.get("City", city_id)
    if st is None:
        abort(404)
    puts = request.get_json()
    st.name = puts['name']
    st.save()
    return jsonify(st.to_dict()), 200
