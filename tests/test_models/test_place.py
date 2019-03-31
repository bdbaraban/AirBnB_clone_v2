#!/usr/bin/python3
"""Defines unnittests for models/place.py."""
import os
import pep8
import unittest
import models
from datetime import datetime
from models.base_model import BaseModel
from models.place import Place
from models.engine.file_storage import FileStorage


class TestPlace(unittest.TestCase):
    """Unittests for testing the Place class."""

    @classmethod
    def setUpClass(cls):
        """Place testing setup.

        Temporarily renames any existing file.json.
        Resets FileStorage objects dictionary.
        Creates a Place instance for testing.
        """
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}
        cls.place = Place()
        cls.place.city_id = "1234-abcd"
        cls.place.user_id = "4321-dcba"
        cls.place.name = "Death Star"
        cls.place.description = "UNLIMITED POWER!!!!!"
        cls.place.number_rooms = 1000000
        cls.place.number_bathrooms = 1
        cls.place.max_guest = 607360
        cls.place.price_by_night = 10
        cls.place.latitude = 160.0
        cls.place.longitude = 120.0
        cls.place.amenity_ids = ["1324-lksd"]

    @classmethod
    def tearDownClass(cls):
        """Place testing teardown.

        Restore original file.json.
        Delete the test Place instance.
        """
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        del cls.place

    def test_pep8(self):
        """Test pep8 styling."""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(["models/place.py"])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_docstrings(self):
        """Check for docstrings."""
        self.assertIsNotNone(Place.__doc__)

    def test_attributes(self):
        """Check for attributes."""
        pl = Place()
        self.assertEqual(str, type(pl.id))
        self.assertEqual(datetime, type(pl.created_at))
        self.assertEqual(datetime, type(pl.updated_at))
        self.assertEqual(str, type(pl.city_id))
        self.assertEqual(str, type(pl.user_id))
        self.assertEqual(str, type(pl.name))
        self.assertEqual(str, type(pl.description))
        self.assertEqual(int, type(pl.number_rooms))
        self.assertEqual(int, type(pl.number_bathrooms))
        self.assertEqual(int, type(pl.max_guest))
        self.assertEqual(int, type(pl.price_by_night))
        self.assertEqual(float, type(pl.latitude))
        self.assertEqual(float, type(pl.longitude))
        self.assertEqual(list, type(pl.amenity_ids))

    def test_is_subclass(self):
        """Check that Place is a subclass of BaseModel."""
        self.assertTrue(issubclass(Place, BaseModel))

    def test_init(self):
        """Test initialization."""
        self.assertTrue(isinstance(self.place, Place))
        self.assertIn(self.place, models.storage.all().values())

    def test_two_models_are_unique(self):
        """Test that different Place instances are unique."""
        am = Place()
        self.assertNotEqual(self.place.id, am.id)
        self.assertLess(self.place.created_at, am.created_at)
        self.assertLess(self.place.updated_at, am.updated_at)

    def test_init_args_kwargs(self):
        """Test initialization with args and kwargs."""
        dt = datetime.today()
        pl = Place("1", id="5", created_at=dt.isoformat())
        self.assertEqual(pl.id, "5")
        self.assertEqual(pl.created_at, dt)

    def test_str(self):
        """Test __str__ representation."""
        s = self.place.__str__()
        self.assertIn("[Place] ({})".format(self.place.id), s)
        self.assertIn("'id': '{}'".format(self.place.id), s)
        self.assertIn("'created_at': {}".format(
            repr(self.place.created_at)), s)
        self.assertIn("'updated_at': {}".format(
            repr(self.place.updated_at)), s)
        self.assertIn("'city_id': '{}'".format(self.place.city_id), s)
        self.assertIn("'user_id': '{}'".format(self.place.user_id), s)
        self.assertIn("'name': '{}'".format(self.place.name), s)
        self.assertIn("'description': '{}'".format(self.place.description), s)
        self.assertIn("'number_rooms': {}".format(self.place.number_rooms), s)
        self.assertIn("'number_bathrooms': {}".format(
            self.place.number_bathrooms), s)
        self.assertIn("'max_guest': {}".format(self.place.max_guest), s)
        self.assertIn("'price_by_night': {}".format(
            self.place.price_by_night), s)
        self.assertIn("'latitude': {}".format(self.place.latitude), s)
        self.assertIn("'longitude': {}".format(self.place.longitude), s)
        self.assertIn("'amenity_ids': {}".format(self.place.amenity_ids), s)

    def test_save(self):
        """Test save method."""
        old = self.place.updated_at
        self.place.save()
        self.assertLess(old, self.place.updated_at)
        with open("file.json", "r") as f:
            self.assertIn("Place." + self.place.id, f.read())

    def test_to_dict(self):
        """Test to_dict method."""
        place_dict = self.place.to_dict()
        self.assertEqual(dict, type(place_dict))
        self.assertEqual(self.place.id, place_dict["id"])
        self.assertEqual("Place", place_dict["__class__"])
        self.assertEqual(self.place.created_at.isoformat(),
                         place_dict["created_at"])
        self.assertEqual(self.place.updated_at.isoformat(),
                         place_dict["updated_at"])
        self.assertEqual(self.place.city_id, place_dict["city_id"])
        self.assertEqual(self.place.user_id, place_dict["user_id"])
        self.assertEqual(self.place.name, place_dict["name"])
        self.assertEqual(self.place.description, place_dict["description"])
        self.assertEqual(self.place.number_rooms, place_dict["number_rooms"])
        self.assertEqual(self.place.number_bathrooms,
                         place_dict["number_bathrooms"])
        self.assertEqual(self.place.max_guest, place_dict["max_guest"])
        self.assertEqual(self.place.price_by_night,
                         place_dict["price_by_night"])
        self.assertEqual(self.place.latitude, place_dict["latitude"])
        self.assertEqual(self.place.longitude, place_dict["longitude"])
        self.assertEqual(self.place.amenity_ids, place_dict["amenity_ids"])


if __name__ == "__main__":
    unittest.main()
