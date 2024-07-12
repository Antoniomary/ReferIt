#!/usr/bin/python3
"""books"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", strict_slashes=False)
def status():
    """gets status of api service"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def get_stats():
    """endpoint to retrieve the number of each resource in storage"""
    return jsonify(
            {
                "authors": storage.count("Author"),
                "books": storage.count("Book"),
                "contributors": storage.count("Contributor")
            })
