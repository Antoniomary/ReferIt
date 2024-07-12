#!/usr/bin/python3
"""initializes as a python package"""
from flask import Blueprint


# create Blueprint instance
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


# wildcard importation of app_view routes
from api.v1.views.index import *
from api.v1.views.authors import *
from api.v1.views.books import *
from api.v1.views.contributors import *
from api.v1.views.search import *
