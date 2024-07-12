#!/usr/bin/python3
"""holds BaseModel class definition"""
from datetime import datetime
from models import storage
from os import getenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from uuid import uuid4


if getenv("REFERIT_STORAGE") == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """a class that defines common attributes/methods for other classes.
       It has three attributes:
       1. id
       2. created_at
       3. updated_at
    """
    if getenv("REFERIT_STORAGE") == "db":
        id = Column(String(60), nullable=False, primary_key=True)
        created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
        updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs) -> None:
        """constructor method"""
        if kwargs:
            for key, value in kwargs.items():
                if key in ['created_at', 'updated_at']:
                    kwargs[key] = datetime.fromisoformat(value)
            kwargs.pop('__class__', None)
            if kwargs.get('id') is None:
                kwargs['id'] = str(uuid4())
            if not kwargs.get('created_at') and not kwargs.get('updated_at'):
                kwargs['created_at'] = datetime.utcnow()
                kwargs['updated_at'] = kwargs['created_at']
            self.__dict__.update(kwargs)
        else:
            self.id: str = str(uuid4())
            self.created_at: datetime = datetime.utcnow()
            self.updated_at: datetime = self.created_at

    def __str__(self) -> str:
        """returns string representation of an object"""
        return f'[{self.__class__.__name__}] ({self.id}) {self.__dict__}'

    def save(self) -> None:
        """updates updated_at with current datetime"""
        self.updated_at: datetime = datetime.utcnow()
        storage.add(self)
        storage.save()

    def to_dict(self) -> dict:
        """returns a dictionary of __dict__ of the instance"""
        new_dict: dict = {}
        for key, value in self.__dict__.items():
            if key in ['updated_at', 'created_at', 'last_login']:
                new_dict[key] = value.isoformat()
            elif key in ['_sa_instance_state', 'password']:
                continue
            else:
                new_dict[key] = value
        new_dict['__class__'] = self.__class__.__name__
        return new_dict

    def delete(self) -> None:
        """deletes an object from storage"""
        storage.delete(self)
