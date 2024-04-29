#!/usr/bin/python3
'''
    Create a new view for User object
'''
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users_all():
    '''
        Retrieves the list of all User objects
    '''
    return jsonify([user.to_dict() for user in storage.all('User').values()])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def user_id(user_id):
    '''
        Retrieves a User object using GET method
    '''
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def user_delete(user_id):
    '''
        Deletes a User object using DELETE method
    '''
    user_obj = storage.get("User", user_id)
    if user_obj is None:
        abort(404)
    storage.delete(user_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def user_post():
    '''
        Creat New user using POST method
    '''
    req = request.get_json()
    if not req:
        err = {"error": "Not a JSON"}
        return jsonify(err), 400
    elif "email" not in req:
        err1 = {"error": "Missing email"}
        return jsonify(err1), 400
    elif "password" not in req:
        err2 = {"error": "Missing password"}
        return jsonify(err2), 400
    else:
        user_obj = request.get_json()
        post = User(**user_obj)
        post.save()
        return jsonify(post.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def user_put(user_id):
    '''
        Update user object using PUT method
    '''
    req = request.get_json()
    if not req:
        err3 = {"error": "Not a JSON"}
        return jsonify(err3), 400
    us = storage.get("User", user_id)
    if us is None:
        abort(404)
    user_obj = request.get_json()
    i = ("id", "email", "created_at", "updated_at")
    puts = user_obj.keys()
    for key in post:
        if key in i:
            pass
        else:
            setattr(us, key, user_obj[key])
    us.save()
    return jsonify(us.to_dict()), 200
