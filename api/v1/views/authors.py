#!/usr/bin/python3
"""authors"""
from api.v1.views import app_views
from flask import abort, jsonify
from models import storage


@app_views.route("/authors", strict_slashes=False,
                 methods=["GET"])
def get_authors():
    """retrieves all authors"""
    authors = [author.to_dict() for author in storage.all("Author").values()]
    return jsonify(authors)


@app_views.route("/authors/<author_id>", strict_slashes=False,
                 methods=["GET"])
def get_author(author_id):
    """retrieves one author"""
    author = storage.get("Author", author_id)
    if author:
        return jsonify(author.to_dict())
    abort(404)


@app_views.route("/authors/<author_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_author(author_id):
    """deletes an author from storage"""
    author = storage.get("Author", author_id)
    if author:
        author.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route("/authors/<author_id>", strict_slashes=False,
                 methods=["PUT"])
def update_author(author_id):
    """deletes an author from storage"""
    author = storage.get("Author", author_id)
    if not author:
        abort(404)

        author.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route("/authors", strict_slashes=False,
                 methods=["POST"])
def create_author():
    """creates an author in storage"""
    pass
