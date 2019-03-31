#!/usr/bin/python3
"""Defines unnittests for models/engine/file_storage.py."""
import os
import json
import pep8
import models
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    """Unittests for testing the FileStorage class."""

    @classmethod
    def setUpClass(cls):
        """FileStorage testing setup.

        Temporarily renames any existing file.json.
        Resets FileStorage objects dictionary.
        Creates instances of all class types for testing.
        """
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}
        cls.base = BaseModel()
        cls.user = User()
        cls.state = State()
        cls.place = Place()
        cls.city = City()
        cls.amenity = Amenity()
        cls.review = Review()

    @classmethod
    def tearDownClass(cls):
        """FileStorage testing teardown.

        Restore original file.json.
        Delete all test class instances.
        """
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        del cls.base
        del cls.user
        del cls.state
        del cls.place
        del cls.city
        del cls.amenity
        del cls.review

    def new(self):
        """Call storage.new on all created class instances."""
        models.storage.new(self.base)
        models.storage.new(self.user)
        models.storage.new(self.state)
        models.storage.new(self.place)
        models.storage.new(self.city)
        models.storage.new(self.amenity)
        models.storage.new(self.review)

    def test_pep8_FileStorage(self):
        """Test pep8 styling."""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/engine/file_storage.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_docstrings(self):
        """Check for docstrings."""
        self.assertIsNotNone(FileStorage.__doc__)
        self.assertIsNotNone(FileStorage.all.__doc__)
        self.assertIsNotNone(FileStorage.new.__doc__)
        self.assertIsNotNone(FileStorage.reload.__doc__)

    def test_attributes(self):
        """Check for attributes."""
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def test_methods(self):
        """Check for methods."""
        self.assertTrue(hasattr(FileStorage, "all"))
        self.assertTrue(hasattr(FileStorage, "new"))
        self.assertTrue(hasattr(FileStorage, "reload"))

    def test_init(self):
        """Test initialization."""
        self.assertTrue(isinstance(models.storage, FileStorage))

    def test_all(self):
        """Test all method."""
        obj = models.storage.all()
        self.assertEqual(type(obj), dict)
        self.assertIs(obj, FileStorage._FileStorage__objects)

    def test_new(self):
        """Test new method."""
        self.new()
        store = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + self.base.id, store.keys())
        self.assertIn(self.base, store.values())
        self.assertIn("User." + self.user.id, store.keys())
        self.assertIn(self.user, store.values())
        self.assertIn("State." + self.state.id, store.keys())
        self.assertIn(self.state, store.values())
        self.assertIn("Place." + self.place.id, store.keys())
        self.assertIn(self.place, store.values())
        self.assertIn("City." + self.city.id, store.keys())
        self.assertIn(self.city, store.values())
        self.assertIn("Amenity." + self.amenity.id, store.keys())
        self.assertIn(self.amenity, store.values())
        self.assertIn("Review." + self.review.id, store.keys())
        self.assertIn(self.review, store.values())

    def test_save(self):
        """Test save method."""
        self.new()
        with open("file.json", "r") as f:
            save_text = f.read()
            self.assertIn("BaseModel." + self.base.id, save_text)
            self.assertIn("User." + self.user.id, save_text)
            self.assertIn("State." + self.state.id, save_text)
            self.assertIn("Place." + self.place.id, save_text)
            self.assertIn("City." + self.city.id, save_text)
            self.assertIn("Amenity." + self.amenity.id, save_text)
            self.assertIn("Review." + self.review.id, save_text)

    def test_reload(self):
        """Test reload method."""
        self.new()
        models.storage.save()
        models.storage.reload()
        store = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + self.base.id, store)
        self.assertIn("User." + self.user.id, store)
        self.assertIn("State." + self.state.id, store)
        self.assertIn("Place." + self.place.id, store)
        self.assertIn("City." + self.city.id, store)
        self.assertIn("Amenity." + self.amenity.id, store)
        self.assertIn("Review." + self.review.id, store)

    def test_reload_no_file(self):
        """Test reload method with no existing file.json."""
        try:
            models.storage.reload()
        except Exception:
            self.fail


if __name__ == "__main__":
    unittest.main()
