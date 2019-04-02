#!/usr/bin/python3
""" Module for db storage engine """
from os import gentenv
from sqlalchemy.orm import relationship
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
                                             getenv("HBNB_MYSQL_DB"))
                                      pool_pre_ping=True)
        if getenv("HBNB_ENV" == "test"):
            Base.metadata.drop_all()
