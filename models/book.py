#!/usr/bin/python3
"""a module for the Book class"""
from models import storage
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String, Table, ForeignKey
from sqlalchemy.orm import relationship


if getenv("REFERIT_STORAGE") == "db":
    book_author = Table(
            'book_author', Base.metadata,
            Column('author_id',
                   String(60), ForeignKey('authors.id'),
                   nullable=False, primary_key=True),
            Column('book_id',
                   String(60), ForeignKey('books.id'),
                   nullable=False, primary_key=True),
    )


class Book(BaseModel):
    """defines Book class"""
    if getenv("REFERIT_STORAGE") == "db":
        __tablename__ = "books"

        title = Column(String(502), nullable=False)
        subtitle = Column(String(502), nullable=True, default='')
        isbn = Column(String(64), nullable=False, unique=True)
        doi = Column(String(256), nullable=True, default='')
        publication_year = Column(Integer, nullable=False)
        publication_place = Column(String(64), nullable=False)
        publisher = Column(String(64), nullable=False)
        description = Column(String, nullable=True, default='')
        edition = Column(String(256), nullable=True)
        volume = Column(String(256), nullable=True)
        added_by_id = Column(String(60), ForeignKey('contributors.id'),
                             nullable=False)
        added_by = relationship("Contributor", backref="added_books")
        authors = relationship("Author", secondary=book_author,
                               viewonly=False, backref="books")
    else:
        title = ""
        subtitle = ""
        isbn = ""
        doi = ""
        publication_year = ""
        publication_place = ""
        publisher = ""
        description = ""
        edition = ""
        volume = ""
        added_by_id = ""
        author_ids = []

        @property
        def authors(self) -> list:
            """returns a list of authors of a book"""
            my_authors = []
            if self.author_ids:
                for author in storage.all('Author').values():
                    if author.id in author_ids:
                        my_authors.append(author)
            return my_authors

        @authors.setter
        def authors(self, obj) -> None:
            """adds an author's id as one of the author of a book"""
            if obj and obj.__class__.__name__ == 'Author':
                if obj.id not in author_ids:
                    self.author_ids.append(obj.id)
