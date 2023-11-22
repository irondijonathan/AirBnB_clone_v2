#!/usr/bin/python3
"""Database storage engine"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class DBStorage:
    """Defines the DBStorage class"""

    __engine = None
    __session = None

    def __init__(self):
        """Initializes a DBStorage object"""
        user = getenv('HBNB_MYSQL_USER')
        pword = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        env = getenv('HBNB_ENV')
        conn_uri = "mysql+mysqldb://{}:{}@{}:3306/{}"\
            .format(user, pword, host, db)
        self.__engine = create_engine(conn_uri, pool_pre_ping=True)
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of the objects in the database"""
        dictionary = {}
        classes = (State, City, User)
        if cls is not None:
            classes = (cls)
        for cls_type in classes:
            objs = self.__session.query(cls_type).all()

            for obj in objs:
                # print(obj)
                key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                dictionary[key] = obj
        # print("===========Final Dict=========")
        # print(dictionary[key])
        # print("==========================")

        return dictionary

    def new(self, obj):
        """Adds an object to the database"""
        if obj is not None:
            try:
                self.__session.add(obj)
            except Exception as ex:
                self.__session.rollback()
                raise ex

    def save(self):
        """Commit all changes of the current db session"""
        self.__session.commit()

    def delete(self, obj):
        """Deletes an object from the database"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """
        Create all tables in the database
        and create the current database session
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()


