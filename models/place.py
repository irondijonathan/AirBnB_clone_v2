#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Integer, Float, String, Column, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False
                     ) if getenv('HBNB_TYPE_STORAGE') == 'db' else ''
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False
                     )if getenv('HBNB_TYPE_STORAGE') == 'db' else ''
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
    amenity_ids = []
