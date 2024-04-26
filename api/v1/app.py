#!/usr/bin/python3
"""
Create our first API that returns an endpoint
"""

from api.v1.views import app_views
from flask import Flask
from flask import jsonify
from os import getenv
from models import storage
from flask_cors import CORS


app = Flask(__name__)

"""
cross origin resource sharing
"""
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

""" run your Flask server (variable app) with """
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', '5000')

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

    jsonify(error).status_code = 404
    return (jsonify(error))


if __name__ == '__main__':
    app.run(host=host, port=port, threaded=True)
