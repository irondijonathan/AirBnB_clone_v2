#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import DATETIME, String, Column, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    __tablename__ = 'cities'
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False
                      ) if getenv('HBNB_TYPE_STORAGE') == 'db' else ''
    name = Column(String(128), nullable=False
                  ) if getenv('HBNB_TYPE_STORAGE') == 'db' else ''
    places = relationship('Place', backref='cities',
                          cascade='all, delete, delete-orphan'
                          ) if getenv('HBNB_TYPE_STORAGE') == 'db' else None
