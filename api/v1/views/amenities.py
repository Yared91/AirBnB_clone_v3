#!/usr/bin/python3
'''
    Create a new view for Amenity objects
'''
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities_all():
    '''
        Retrieves the list of all Amenity objects
    '''
    return jsonify([am.to_dict() for am in storage.all('Amenity').values()])


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def amenitys_id(amenity_id):
    '''
        Retrieves a Amenity object and Id
    '''
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def amenity_delete(amenity_id):
    '''
        Deletes a Amenity object by given Id
    '''
    amenity_obj = storage.get("Amenity", amenity_id)
    if amenity_obj is None:
        abort(404)
    storage.delete(amenity_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def amenities_post():
    '''
        Create new Amenity using POST method
    '''
    req = request.get_json()
    if not req:
        err = {"error": "Not a JSON"}
        return jsonify(err), 400
    elif "name" not in req:
        err1 = {"error": "Missing name"}
        return jsonify(err1), 400
    else:
        amenity_obj = request.get_json()
        post = Amenity(**amenity_obj)
        post.save()
        return jsonify(post.to_dict()), 201


@app_views.route('/amenities/<amenities_id>',
                 methods=['PUT'], strict_slashes=False)
def amenity_put(amenities_id):
    '''
        update Amenity object using PUT Method
    '''
    req = request.get_json()
    if not req:
        err2 = {"error": "Not a JSON"}
        return jsonify(err2), 400
    am = storage.get("Amenity", amenities_id)
    if am is None:
        abort(404)
    puts = request.get_json()
    am.name = puts['name']
    am.save()
    return jsonify(am.to_dict()), 200
