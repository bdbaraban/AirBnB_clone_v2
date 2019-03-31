#!/usr/bin/python3
"""Defines unnittests for models/city.py."""
import os
import pep8
import unittest
import models
from datetime import datetime
from models.base_model import BaseModel
from models.city import City
from models.engine.file_storage import FileStorage


class TestCity(unittest.TestCase):
    """Unittests for testing the City class."""

    @classmethod
    def setUpClass(cls):
        """City testing setup.

        Temporarily renames any existing file.json.
        Resets FileStorage objects dictionary.
        Creates a City instance for testing.
        """
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}
        cls.city = City()
        cls.city.state_id = "415"
        cls.city.name = "San Francisco"

    @classmethod
    def tearDownClass(cls):
        """City testing teardown.

        Restore original file.json.
        Delete the test City instance.
        """
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        del cls.city

    def test_pep8(self):
        """Test pep8 styling."""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(["models/city.py"])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_docstrings(self):
        """Check for docstrings."""
        self.assertIsNotNone(City.__doc__)

    def test_attributes(self):
        """Check for attributes."""
        ct = City()
        self.assertEqual(str, type(ct.id))
        self.assertEqual(datetime, type(ct.created_at))
        self.assertEqual(datetime, type(ct.updated_at))
        self.assertEqual(str, type(ct.state_id))
        self.assertEqual(str, type(ct.name))

    def test_is_subclass(self):
        """Check that City is a subclass of BaseModel."""
        self.assertTrue(issubclass(City, BaseModel))

    def test_init(self):
        """Test initialization."""
        self.assertTrue(isinstance(self.city, City))
        self.assertIn(self.city, models.storage.all().values())

    def test_two_models_are_unique(self):
        """Test that different City instances are unique."""
        ct = City()
        self.assertNotEqual(self.city.id, ct.id)
        self.assertLess(self.city.created_at, ct.created_at)
        self.assertLess(self.city.updated_at, ct.updated_at)

    def test_init_args_kwargs(self):
        """Test initialization with args and kwargs."""
        dt = datetime.today()
        ct = City("1", id="5", created_at=dt.isoformat())
        self.assertEqual(ct.id, "5")
        self.assertEqual(ct.created_at, dt)

    def test_str(self):
        """Test __str__ representation."""
        s = self.city.__str__()
        self.assertIn("[City] ({})".format(self.city.id), s)
        self.assertIn("'id': '{}'".format(self.city.id), s)
        self.assertIn("'created_at': {}".format(repr(self.city.created_at)), s)
        self.assertIn("'updated_at': {}".format(repr(self.city.updated_at)), s)
        self.assertIn("'state_id': '{}'".format(self.city.state_id), s)
        self.assertIn("'name': '{}'".format(self.city.name), s)

    def test_save(self):
        """Test save method."""
        old = self.city.updated_at
        self.city.save()
        self.assertLess(old, self.city.updated_at)
        with open("file.json", "r") as f:
            self.assertIn("City." + self.city.id, f.read())

    def test_to_dict(self):
        """Test to_dict method."""
        city_dict = self.city.to_dict()
        self.assertEqual(dict, type(city_dict))
        self.assertEqual(self.city.id, city_dict["id"])
        self.assertEqual("City", city_dict["__class__"])
        self.assertEqual(self.city.created_at.isoformat(),
                         city_dict["created_at"])
        self.assertEqual(self.city.updated_at.isoformat(),
                         city_dict["updated_at"])
        self.assertEqual(self.city.state_id, city_dict["state_id"])
        self.assertEqual(self.city.name, city_dict["name"])


if __name__ == "__main__":
    unittest.main()
