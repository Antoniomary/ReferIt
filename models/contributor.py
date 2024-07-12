#!/usr/bin/python3
"""a module for the Book class"""
from datetime import datetime
from models import storage
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class Contributor(BaseModel, Base):
    """defines a Contributor class"""
    if getenv("REFERIT_STORAGE") == "db":
        __tablename__ = "contributors"

        first_name = Column(String(40), nullable=False)
        last_name = Column(String(40), nullable=False)
        email = Column(String(128), nullable=False, unique=True)
        user_name = Column(String(64), nullable=False, unique=True)
        password = Column(String(64), nullable=False)
        last_login = Column(DateTime, nullable=False, default=datetime.utcnow)
        number_added = Column(Integer, nullable=False, default=0)
        added_books = relationship("Book", backref="added_by")
    else:
        first_name = ""
        last_name = ""
        email = ""
        user_name = ""
        password = ""
        last_login = ""
        added_book_ids = []
        number_added = 0

        @property
        def added_books(self) -> list:
            """returns the list of books added by a contributor"""
            added_books = []
            if self.added_book_ids:
                for book in storage.all('Book').values():
                    if book.id in added_book_ids:
                        added_books.append(book)
            return added_books

        @added_books.setter
        def added_books(self, obj: object) -> None:
            """adds book to list of books added by a contributor"""
            if obj and obj.__class__.__name__ == 'Book':
                if obj.id not in added_book_ids:
                    self.added_book_ids.append(obj.id)
