#!/usr/bin/python3
"""entry point"""
from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.teardown_appcontext
def teardown(exception):
    """removes session from storage context"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """custom 404 errer response"""
    return jsonify({"error": "not found"}), 404


if __name__ == "__main__":
    """run app"""
    host = getenv("API_HOST", "0.0.0.0")
    port = int(getenv("API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
