#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import DATETIME, String, Column, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv
from models.city import City


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False
                  ) if getenv('HBNB_TYPE_STORAGE') == 'db' else ''

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship("City", backref="state",
                              cascade="all, delete, delete-orphan")
    else:
        @property
        def cities(self):
            """Returns all cities in this state"""
            from models import storage
            state_cities = []
            for value in storage.all(City).values():
                if value.state_id == self.id:
                    state_cities.append(value)
            return state_cities
