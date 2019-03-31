#!/usr/bin/python3
"""Defines unnittests for models/amenity.py."""
import os
import pep8
import unittest
import models
from datetime import datetime
from models.base_model import BaseModel
from models.amenity import Amenity
from models.engine.file_storage import FileStorage


class TestAmenity(unittest.TestCase):
    """Unittests for testing the Amenity class."""

    @classmethod
    def setUpClass(cls):
        """Amenity testing setup.

        Temporarily renames any existing file.json.
        Resets FileStorage objects dictionary.
        Creates a Amenity instance for testing.
        """
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}
        cls.amenity = Amenity()
        cls.amenity.name = "Breakfast"

    @classmethod
    def tearDownClass(cls):
        """Amenity testing teardown.

        Restore original file.json.
        Delete the test Amenity instance.
        """
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        del cls.amenity

    def test_pep8(self):
        """Test pep8 styling."""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(["models/amenity.py"])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_docstrings(self):
        """Check for docstrings."""
        self.assertIsNotNone(Amenity.__doc__)

    def test_attributes(self):
        """Check for attributes."""
        am = Amenity()
        self.assertEqual(str, type(am.id))
        self.assertEqual(datetime, type(am.created_at))
        self.assertEqual(datetime, type(am.updated_at))
        self.assertEqual(str, type(am.name))

    def test_is_subclass(self):
        """Check that Amenity is a subclass of BaseModel."""
        self.assertTrue(issubclass(Amenity, BaseModel))

    def test_init(self):
        """Test initialization."""
        self.assertTrue(isinstance(self.amenity, Amenity))
        self.assertIn(self.amenity, models.storage.all().values())

    def test_two_models_are_unique(self):
        """Test that different Amenity instances are unique."""
        am = Amenity()
        self.assertNotEqual(self.amenity.id, am.id)
        self.assertLess(self.amenity.created_at, am.created_at)
        self.assertLess(self.amenity.updated_at, am.updated_at)

    def test_init_args_kwargs(self):
        """Test initialization with args and kwargs."""
        dt = datetime.today()
        am = Amenity("1", id="5", created_at=dt.isoformat(), name="Lunch")
        self.assertEqual(am.id, "5")
        self.assertEqual(am.created_at, dt)
        self.assertEqual(am.name, "Lunch")

    def test_str(self):
        """Test __str__ representation."""
        s = self.amenity.__str__()
        self.assertIn("[Amenity] ({})".format(self.amenity.id), s)
        self.assertIn("'id': '{}'".format(self.amenity.id), s)
        self.assertIn("'created_at': {}".format(repr(self.amenity.created_at)),
                      s)
        self.assertIn("'updated_at': {}".format(repr(self.amenity.updated_at)),
                      s)
        self.assertIn("'name': '{}'".format(self.amenity.name), s)

    def test_save(self):
        """Test save method."""
        old = self.amenity.updated_at
        self.amenity.save()
        self.assertLess(old, self.amenity.updated_at)
        with open("file.json", "r") as f:
            self.assertIn("Amenity." + self.amenity.id, f.read())

    def test_to_dict(self):
        """Test to_dict method."""
        amenity_dict = self.amenity.to_dict()
        self.assertEqual(dict, type(amenity_dict))
        self.assertEqual(self.amenity.id, amenity_dict["id"])
        self.assertEqual("Amenity", amenity_dict["__class__"])
        self.assertEqual(self.amenity.created_at.isoformat(),
                         amenity_dict["created_at"])
        self.assertEqual(self.amenity.updated_at.isoformat(),
                         amenity_dict["updated_at"])
        self.assertEqual(self.amenity.name, amenity_dict["name"])


if __name__ == "__main__":
    unittest.main()
