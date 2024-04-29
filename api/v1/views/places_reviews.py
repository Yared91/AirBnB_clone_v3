#!/usr/bin/python3
'''
    Create a Review objects that handles all default RESTFul API actions
'''
from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def place_review(place_id):
    '''
        Retrieves the list of all place review
    '''
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify([rev.to_dict() for rev in place.reviews]), 200


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def review_id(review_id):
    '''
        Retrieves a Review object using GET methods
    '''
    review_obj = storage.get("Review", review_id)
    if review_obj is None:
        abort(404)
    response = jsonify(review_obj.to_dict())
    return response, 200


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def review_delete(review_id):
    '''
        Delete review obj using DELETE method
    '''
    review_obj = storage.get("Review", review_id)
    if review_obj is None:
        abort(404)
    storage.delete(review_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def review_post(place_id):
    '''
        Create new review obj using POST method
    '''
    if storage.get("Place", place_id) is None:
        abort(404)
    req = request.get_json()
    elif not req:
        err = {"error": "Not a JSON"}
        return jsonify(err), 400
    elif "user_id" not in req:
        err1 = {"error": "Missing user_id"}
        return jsonify(err1), 400
    posts = request.get_json()["user_id"]
    elif storage.get("User", posts) is None:
        abort(404)
    elif "text" not in req:
        err2 = {"error": "Missing text"}
        return jsonify(err2), 400
    else:
        review_obj = request.get_json()
        post = Review(**review_obj)
        post.place_id = place_id
        post.save()
        response = jsonify(post.to_dict())
        return response, 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def review_put(review_id):
    '''
        Update review city object using PUT Method
    '''
    rev = storage.get("Review", review_id)
    if rev is None:
        abort(404)
    req = request.get_json()
    elif not req:
        err3 = {"error": "Not a JSON"}
        return jsonify(err3), 400
    else:
        review_obj = request.get_json()
        i = ("id", "user_id", "place_id", "created_at", "updated_at")
        puts = review_obj.keys()
        for key in puts:
            if key in i:
                pass
            else:
                setattr(rev, key, review_obj[key])
        rev.save()
        return jsonify(rev.to_dict()), 200
