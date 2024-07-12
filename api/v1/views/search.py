#!/usr/bin/python3
"""authors"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
import requests


@app_views.route("/search", strict_slashes=False,
                 methods=["GET"])
def search():
    """retrieves information about a book"""
    query = request.args.get('q')
    if query:
        query = query.strip()
        books = storage.all("Book").values()
        if books:
            result = []
            if query.startswith('10.'):
                # start search from doi
                # DOI starts with 10
                for book in books:
                    if book.doi == query:
                        return jsonify(book.to_dict())
            elif len(query.replace('-', ' ')) in [10, 13]:
                # maybe it is an Isbn
                # they have 10 digits for isbn-10 or 13 for isbn-13
                for book in books:
                    if book.isbn == query:
                        return jsonify(book.to_dict())

            q = query.lower()
            # next, search author
            for book in books:
                for author in book.authors:
                    if author.name.lower() == q:
                        return jsonify(book.to_dict())
                    elif author.name.lower() in q or q in author.name.lower():
                        result.append(book.to_dict())
            # finally title
            for book in books:
                if book.title.lower() == q:
                    return jsonify(book.to_dict())
                elif book.title.lower() in q or q in book.title.lower():
                    result.append(book.to_dict())
            # return related search for similar book titles or author name
            if result:
                return jsonify(result)

        return jsonify(error="no result found")
    else:
        return jsonify(error="nothing to search")
