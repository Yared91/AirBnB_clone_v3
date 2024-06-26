#!/usr/bin/python3
"""
Create our first API that returns an endpoint
"""
from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
import os


app = Flask(__name__)

"""
cross origin resource sharing
"""
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

"""register the blueprint app_views"""
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_storage(exception):
    """
    It calls the storage.close()
    """
    storage.close()


@app.errorhandler(404)
def error_404(exception):
    """
    It handles the 404 error
    and displays error: "Not Found"
    """

    error = {
        "error": "Not found"
        }

    response = jsonify(error)
    response.status_code = 404
    return (response)


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
