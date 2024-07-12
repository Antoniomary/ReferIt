#!/usr/bin/python3
"""a module for the Book class"""
from models import storage
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String


class Author(BaseModel, Base):
    """defines an Author class"""
    if getenv("REFERIT_STORAGE") == "db":
        __tablename__ = "authors"

        first_name = Column(String(64), nullable=False)
        middle_name = Column(String(64), nullable=True, default='')
        last_name = Column(String(64), nullable=True, default='')
        # books = relationship('Book', secondary='book_author,
        #                      viewonly=False, backref='books')
    else:
        first_name = ""
        middle_name = ""
        last_name = ""
        book_ids = []

        @property
        def books(self):
            """returns list of books written by author"""
            my_books = []
            for book in storage.all("Books").values():
                if book.id in book_ids:
                    my_books.append(book)
            return my_books

        @books.setter
        def books(self, obj):
            """adds a book to an author as its author"""
            if obj and obj.__class__.name == 'Book':
                if obj.id not in book_ids:
                    book_ids.append(obj.id)
