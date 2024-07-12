#!/usr/bin/python3
"""hold DBStorage class defintion"""
from datetime import datetime
from os.path import isfile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import json


class DBStorage:
    """definea a database bases storage system """
    __engine = None
    __session = None

    def __init__(self) -> None:
        """constructor function"""
        from models.base_model import Base
        user = getenv('REFERIT_USER')
        pwd = getenv('REFERIT_PWD')
        host = getenv('REFERIT_HOST')
        db = getenv('REFERIT_DB')
        try:
            DB_URI = "mysql+mysqldb://{}:{}@{}/{}".format(user, pwd, host, db)
            self.__engine = create_engine(DB_URI, pool_pre_ping=True)
            if getenv('REFERIT_ENV') == 'test':
                Base.metadata.drop_all(self.__engine)
        except Exception as e:
            print(f'ERROR: {e}')

    def all(self, cls=None) -> dict:
        """returns a dictionary of objects.
           Each object is stored in the format:
           "<class name>.<id>" : object
        """
        all_objects = {}
        if cls is None:
            for cls in self.get_cls.classes.values():
                for each in self.__session.query(cls).all():
                    key = each.__class__.__name__ + '.' + each.id
                    all_objects[key] = each
        else:
            cls = self.get_cls(cls)
            if cls:
                result = self.__session.query(cls).all()
                for each in result:
                    key = each.__class__.__name__ + '.' + each.id
                    all_objects[key] = each
        return all_objects

    def add(self, obj: object) -> None:
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self) -> None:
        """commit all changes of the current database session"""
        self.__session.commit()

    def reload(self) -> None:
        """deserializes the JSON file in __file_path to __objects"""
        from models.author import Author
        from models.base_model import BaseModel, Base
        from models.book import Book
        from models.contributor import Contributor
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    @staticmethod
    def get_cls(cls: str) -> object:
        """returns a class based on the class name"""
        from models.author import Author
        from models.book import Book
        from models.contributor import Contributor
        classes = {
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
            return self.__session.query(cls).filter_by(id=obj_id).first()

    def delete(self, obj=None) -> None:
        """delete an object from the current database session"""
        if obj:
            self.__session.delete(obj)

    def count(self, cls: str = None):
        """return the number of instances of a class in storage if it exists
           else None if class is invalid
        """
        if cls and self.get_cls(cls):
            return self.__session.query(cls).count()

    def close(self) -> None:
        """removes session from context"""
        self.__session.remove()
