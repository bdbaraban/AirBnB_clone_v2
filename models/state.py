#!/usr/bin/python3
"""This is the state class"""
from models.base_model import BaseModel
from sqlalchemy import String, Column


class State(BaseModel):
    """This is the class for State
    Attributes:
        name: input name
    """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City",  backref = "state", cascade = "delete")

    @property
    def cities(self):
        for 
