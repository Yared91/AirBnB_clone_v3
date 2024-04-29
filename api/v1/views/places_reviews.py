#!/usr/bin/python3
'''
    Create a new view for Review object
'''
from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def review_place(place_id):
    '''
        Retrieves the list of all Review objects of a Place
    '''
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify([r.to_dict() for r in place.reviews]), 200


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def review_id(review_id):
    '''
        Retrieves a Review object using GET method
    '''
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict()), 200


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def review_delete(review_id):
    '''
        Delete review obj using id
    '''
    review_obj = storage.get("Review", review_id)
    if review_obj is None:
        abort(404)
    storage.delete(review_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    '''
        create new review obj through place association using POST
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
    elif storage.get("User", request.get_json()["user_id"]) is None:
        abort(404)
    elif "text" not in req:
        err2 = {"error": "Missing text"}
        return jsonify(err2), 400
    else:
        obj = request.get_json()
        post = Review(**obj)
        post.place_id = place_id
        post.save()
        return jsonify(post.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    '''
        update review city object using PUT
    '''
    obj = storage.get("Review", review_id)
    if obj is None:
        abort(404)
    elif not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    else:
        obj_data = request.get_json()
        ignore = ("id", "user_id", "place_id", "created_at", "updated_at")
        for k in obj_data.keys():
            if k in ignore:
                pass
            else:
                setattr(obj, k, obj_data[k])
        obj.save()
        return jsonify(obj.to_dict()), 200
