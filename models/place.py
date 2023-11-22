#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Integer, Float, String, Column, ForeignKey, Table
from sqlalchemy.orm import relationship
from os import getenv
from models.amenity import Amenity
from models.review import Review


place_amenity = Table('place_amenity',
                      Base.metadata,
                      Column('place_id', String(60),
                             ForeignKey('places.id'),
                             nullable=False, primary_key=True),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'),
                             nullable=False, primary_key=True))
"""The many to many relationship table
between Place and Amenity records.
"""


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False
                     ) if getenv('HBNB_TYPE_STORAGE') == 'db' else ''
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False
                     ) if getenv('HBNB_TYPE_STORAGE') == 'db' else ''
    name = Column(String(128), nullable=False
                  )if getenv('HBNB_TYPE_STORAGE') == 'db' else ''
    description = Column(String(1024)
                         )if getenv('HBNB_TYPE_STORAGE') == 'db' else ''
    number_rooms = Column(Integer, nullable=False, default=0
                          ) if getenv('HBNB_TYPE_STORAGE') == 'db' else 0
    number_bathrooms = Column(Integer, nullable=False, default=0
                              ) if getenv('HBNB_TYPE_STORAGE') == 'db' else 0
    max_guest = Column(Integer, nullable=False, default=0
                       ) if getenv('HBNB_TYPE_STORAGE') == 'db' else 0
    price_by_night = Column(Integer, nullable=False, default=0
                            ) if getenv('HBNB_TYPE_STORAGE') == 'db' else 0
    latitude = Column(Float) if getenv('HBNB_TYPE_STORAGE') == 'db' else 0.0
    longitude = Column(Float) if getenv('HBNB_TYPE_STORAGE') == 'db' else 0.0

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        reviews = relationship('Review', backref='place',
                               cascade='all, delete, delete-orphan')
    else:
        @property
        def reviews(self):
            """Gets list of reviews"""
            from models import storage

            res = []
            for _, review in storage.all(Review).items:
                if review.place_id == self.id:
                    res.append(review)
            return res
    amenity_ids = []

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        amenities = relationship('Amenity',
                                 secondary=place_amenity,
                                 backref='place_amenities', viewonly=False)
    else:
        @property
        def amenities(self):
            """Gets all the amenities for a place"""
            from models import storage

            res = []
            for val in storage.all(Amenity).values():
                if val.id not in self.amenity_ids:
                    res.append(val)
            return res

        @amenities.setter
        def amenities(self, value):
            """Adds an amenity to this Place"""
            if type(value) is Amenity and value.id not in self.amenity_ids:
                self.amenity_ids.append(value.id)
