#!/usr/bin/python3
"""books"""
from api.v1.views import app_views
from flask import abort, jsonify
from models import storage


@app_views.route("/books", strict_slashes=False,
                 methods=["GET"])
def get_books():
    """retrieves all books"""
    books = [book.to_dict() for author in storage.all("Book").values()]
    return jsonify(books)


@app_views.route("/books/<book_id>", strict_slashes=False,
                 methods=["GET"])
def get_book(book_id):
    """retrieves one book"""
    book = storage.get("Book", book_id)
    if book:
        return jsonify(book.to_dict())
    abort(404)


@app_views.route("/books/<book_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_book(book_id):
    """deletes a book from storage"""
    book = storage.get("Book", book_id)
    if book:
        book.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route("/books/<book_id>", strict_slashes=False,
                 methods=["PUT"])
def update_book(book_id):
    """deletes a book from storage"""
    book = storage.get("Book", book_id)
    if not book:
        abort(404)

        book.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route("/books", strict_slashes=False,
                 methods=["POST"])
def create_book():
    """creates a book in storage"""
    pass
