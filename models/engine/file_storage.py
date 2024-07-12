#!/usr/bin/python3
"""hold FileStorage class defintion"""
from datetime import datetime
from os.path import isfile
import json


class FileStorage:
    """serializes instances to a JSON file and
       deserializes JSON file to instances.
    """
    __file_name: str = "file.json"
    __objects: dict = {}

    def __init__(self) -> None:
        """constructor function"""
        pass

    def all(self, cls=None) -> dict:
        """returns a dictionary of objects.
           Each object is stored in the format:
           "<class name>.<id>" : object
        """
        if cls is None:
            return self.__objects
        if self.get_cls(cls):
            return dict([(key, val) for key, val in self.__objects.items()
                        if cls == val.__class__.__name__])

    def add(self, obj: object) -> None:
        """adds a new object to __objects in the format:
           "<class name>.<id>" : object
        """
        self.__objects[obj.__class__.__name__ + '.' + obj.id] = obj

    def save(self) -> None:
        """serializes __objects to the JSON file name after __file_name"""
        with open(self.__file_name, 'w') as file:
            objects = {}
            for key, value in self.__objects.items():
                objects[key] = value.to_dict()
            json.dump(objects, file)

    def reload(self) -> None:
        """deserializes the JSON file in __file_path to __objects"""
        if isfile(self.__file_name):
            try:
                with open(self.__file_name) as file:
                    obj_dict = json.load(file)
                    for key, value in obj_dict.items():
                        obj_class = value['__class__']
                        self.__objects[key] = self.get_cls(obj_class)(**value)
            except Exception as e:
                pass

    @staticmethod
    def get_cls(cls: str) -> object:
        """returns a class based on the class name"""
        from models.author import Author
        from models.base_model import BaseModel
        from models.book import Book
        from models.contributor import Contributor
        classes = {
            "BaseModel": BaseModel,
            "Author": Author,
            "Book": Book,
            "Contributor": Contributor,
        }
        if cls and cls in classes.keys():
            return classes[cls]

    @staticmethod
    def get_cls_attr(cls: str) -> dict:
        """returns a dictionary of the attribute and its type of the class"""
        cls_and_its_attrs = {
            'BaseModel': {
                'id': str,
                'created_at': datetime,
                'updated_at': datetime,
            },
            'Book': {
                'title': str,
                'subtitle': str,
                'isbn': str,
                'doi': str,
                'publication_year': int,
                'publication_place': str,
                'publisher': str,
                'description': str,
                'edition': str,
                'volume': str,
            },
            'Author': {
                'first_name': str,
                'middle_name': str,
                'last_name': str,
            },
            'Contributor': {
                'first_name': str,
                'last_name': str,
                'email': str,
                'user_name': str,
                'password': str,
                'last_login': str,
            },
        }

        return cls_and_its_attrs[cls]

    def get(self, cls, obj_id) -> object:
        """returns a particular obj in storage based on id"""
        if self.get_cls(cls) and obj_id:
            for obj in self.all(cls).values():
                if obj.id == obj_id:
                    return obj

    def delete(self, obj=None) -> None:
        """deletes an object from storage if it exists"""
        if obj:
            if obj in self.all().values():
                del self.__objects[obj.__class__.__name__ + '.' + obj.id]
                self.save()

    def count(self, cls: str = None):
        """return the number of instances of a class in storage if it exists
           else None if class is invalid
        """
        if cls and self.get_cls(cls):
            return len(self.all(cls))

    def close(self) -> None:
        """does nothing.
           It was created to avoid problem with API
        """
        pass
