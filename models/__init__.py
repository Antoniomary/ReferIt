#!/usr/bin/python3
"""initializes directory as a package"""
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
from os import getenv


if  getenv('REFERIT_STORAGE') == 'db':
    # create instance of FileStorage
    storage = DBStorage()
else:
    # create instance of FileStorage
    storage = FileStorage()

# call the reload method
storage.reload()
