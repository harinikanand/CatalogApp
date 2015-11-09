import sys

from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()

# create a User Class
class User(Base):
   __tablename__ = 'user'
   id = Column(Integer, primary_key=True)
   name = Column(String(250), nullable=False)
   email = Column(String(250), nullable=False)
   picture = Column(String(250))

# create a Book_genres Class
class Book_genres(Base):

   __tablename__ = 'book_genres'

   name = Column(String(80), nullable = False)
   id = Column(Integer, primary_key = True)
   user_id = Column(Integer, ForeignKey('user.id'))
   user = relationship(User)

   # We added this serialize function to be able to send JSON objects in a
   # serializable format
   @property
   def serialize(self):
    """Return object data in easily serializeable format"""
    return {
        'name': self.name,
        'id': self.id
    }

# create a Books Class
class Books(Base):

   __tablename__ = 'book'

   name = Column(String(80), nullable = False)
   id = Column(Integer, primary_key = True)
   author = Column(String(100))
   description = Column(String(1000))
   price = Column(String(8))

   book_genre_id = Column(Integer, ForeignKey('book_genres.id'))
   book_genre = relationship(Book_genres)

   user_id = Column(Integer, ForeignKey('user.id'))
   user = relationship(User)

   # We added this serialize function to be able to send JSON objects in a
   # serializable format
   @property
   def serialize(self):
    """Return object data in easily serializeable format"""
    return {
        'name': self.name,
        'description': self.description,
        'id': self.id,
        'price': self.price,
        'author': self.author,
        'book_genre_id': self.book_genre_id
    }

# create a bookstore sql database file
engine = create_engine('sqlite:///bookstore.db')
Base.metadata.create_all(engine)
