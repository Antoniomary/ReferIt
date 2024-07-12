#!/usr/bin/python3
"""books"""
from api.v1.views import app_views
from flask import abort, jsonify
from models import storage


@app_views.route("/contributors", strict_slashes=False,
                 methods=["GET"])
def get_contributors():
    """retrieves all contributors"""
    contributors = [c.to_dict() for c in storage.all("Contributor").values()]
    return jsonify(contributors)


@app_views.route("/contributors/<contributor_id>", strict_slashes=False,
                 methods=["GET"])
def get_contributor(contributor_id):
    """retrieves one contributor"""
    contributor = storage.get("Contributor", contributor_id)
    if contributor:
        return jsonify(contributor.to_dict())
    abort(404)


@app_views.route("/contributors/<contributor_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_contributor(contributor_id):
    """deletes a contributor from storage"""
    contributor = storage.get("Contributor", contributor_id)
    if contributor:
        contributor.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route("/contributors/<contributor_id>", strict_slashes=False,
                 methods=["PUT"])
def update_contributor(contributor_id):
    """deletes a contributor from storage"""
    contributor = storage.get("Contributor", contributor_id)
    if not contributor:
        abort(404)

        contributor.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route("/contributors", strict_slashes=False,
                 methods=["POST"])
def create_contributor():
    """creates a contributor in storage"""
    pass
