#!/usr/bin/python3
""" Module for db storage engine """
from os import getenv
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from sqlalchemy import (create_engine)
from models.base_model import Base, BaseModel
from models.city import City
from models.state import State
from models.user import User
from models.amenity import Amenity
from models.review import Review
from models.place import Place


class DBStorage:
    """ Represent a database storage engine """

    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                      format(getenv("HBNB_MYSQL_USER"),
                                             getenv("HBNB_MYSQL_PWD"),
                                             getenv("HBNB_MYSQL_HOST"),
                                             getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all()

    def all(self, cls=None):
        print(cls)
        print(type(cls))
        if cls is None:
            objs = self.__session.query(User, State, City,
                                        Amenity, Place, Review).all()
        else:
            objs = self.__session.query(cls)
        objs_dict = {}
        for o in objs:
            objs_dict["{}.{}".format(type(o).__name__, o.id)] = o
        return objs_dict

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
