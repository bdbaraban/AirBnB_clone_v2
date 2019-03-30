#!/usr/bin/python3
"""This is the city class"""
from models.base_model import BaseModel


class City(BaseModel):
    """This is the class for City
    Attributes:
        state_id: The state id
        name: input name
    """
    state_id = ""
    name = ""
