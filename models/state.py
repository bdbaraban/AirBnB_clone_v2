#!/usr/bin/python3
"""This is the state class"""
from models.base_model import BaseModel
from models.city import City
from sqlalchemy import String, Column


class State(BaseModel):
    """This is the class for State
    Attributes:
        name: input name
    """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City",  backref="state", cascade="delete")

    @property
    def cities(self):
        city_list = []
        for city in list(models.storage.all(City).vallues()):
            if city.state_id == self.id:
                city_list.append(city)
        return city_list
