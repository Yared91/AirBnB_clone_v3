#!/usr/bin/python3
'''
    Create a new view for Place objects
'''
from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def place_city(city_id):
    '''
        Retrieves the list of all Place objects of a City
    '''
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    response = jsonify([place.to_dict() for place in city.places])
    return response, 200


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def place_id(place_id):
    '''
        Retrieves a Place object
    '''
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)
    response = jsonify(place_obj.to_dict())
    return response, 200


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def place_delete(place_id):
    '''
        Deletes a Place object using DELETE method
    '''
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)
    storage.delete(place_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def place_post(city_id):
    '''
        Create Place Object using POST method
    '''
    req = request.get_json()
    if not req:
        err = {"error": "Not a JSON"}
        return jsonify(err), 400
    elif "name" not in req:
        err1 = {"error": "Missing name"}
        return jsonify(err1), 400
    elif "user_id" not in req:
        err2 = {"error": "Missing user_id"}
        return jsonify(err2), 400
    else:
        place_obj = request.get_json()
        c = storage.get("City", city_id)
        u = storage.get("User", obj_data['user_id'])
        if c is None or u is None:
            abort(404)
        place_obj['city_id'] = c.id
        place_obj['user_id'] = u.id
        post = Place(**place_obj)
        post.save()
        response = jsonify(post.to_dict())
        return response, 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    '''
        Update place object using PUT
    '''
    req = request.get_json()
    if not req:
        err3 = {"error": "Not a JSON"}
        return jsonify(err3), 400

    pl = storage.get("Place", place_id)
    if pl is None:
        abort(404)
    place_obj = request.get_json()
    i = ("id", "user_id", "created_at", "updated_at")
    puts = obj_data.items()
    for key, value in puts:
        if key not in i:
            setattr(pl, key, value)
    pl.save()
    response = jsonify(pl.to_dict())
    return response, 200
