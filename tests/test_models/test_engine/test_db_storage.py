#!/usr/bin/python3
"""Defines unnittests for models/engine/db_storage.py."""
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
from models.engine.db_storage import DBStorage
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.session import Session


class TestDBStorage(unittest.TestCase):
    """Unittests for testing the DBStorage class."""

    @classmethod
    def setUpClass(cls):
        """Create instances of all class types for testing."""
        cls.state = State(name="California")
        models.storage.new(cls.state)
        cls.city = City(name="San_Jose", state_id=cls.state.id)
        models.storage.new(cls.city)
        models.storage.save()

    @classmethod
    def tearDownClass(cls):
        """Delete all test class instances."""
        del cls.state
        del cls.city

    def new(self):
        """Call storage.new on all created class instances."""
        models.storage.new(self.state)
        models.storage.new(self.city)

    def test_pep8(self):
        """Test pep8 styling."""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/engine/db_storage.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_docstrings(self):
        """Check for docstrings."""
        self.assertIsNotNone(DBStorage.__doc__)
        self.assertIsNotNone(DBStorage.__init__.__doc__)
        self.assertIsNotNone(DBStorage.all.__doc__)
        self.assertIsNotNone(DBStorage.new.__doc__)
        self.assertIsNotNone(DBStorage.save.__doc__)
        self.assertIsNotNone(DBStorage.delete.__doc__)
        self.assertIsNotNone(DBStorage.reload.__doc__)

    @unittest.skipIf(os.getenv("HBNB_ENV") != "test",
                     "Requires MySQL environmental variables")
    def test_attributes(self):
        """Check for attributes."""
        self.assertEqual(Engine, type(models.storage._DBStorage__engine))
        self.assertEqual(Session, type(models.storage._DBStorage__session))

    def test_methods(self):
        """Check for methods."""
        self.assertTrue(hasattr(DBStorage, "__init__"))
        self.assertTrue(hasattr(DBStorage, "all"))
        self.assertTrue(hasattr(DBStorage, "new"))
        self.assertTrue(hasattr(DBStorage, "save"))
        self.assertTrue(hasattr(DBStorage, "delete"))
        self.assertTrue(hasattr(DBStorage, "reload"))

    @unittest.skipIf(os.getenv("HBNB_ENV") != "test",
                     "Requires MySQL environmental variables")
    def test_init(self):
        """Test initialization."""
        self.assertTrue(isinstance(models.storage, DBStorage))

    @unittest.skipIf(os.getenv("HBNB_ENV") != "test",
                     "Requires MySQL environmental variables")
    def test_all(self):
        """Test default all method."""
        obj = models.storage.all()
        self.assertEqual(type(obj), dict)
        self.assertEqual(len(obj), 7)

    @unittest.skipIf(os.getenv("HBNB_ENV") != "test",
                     "Requires MySQL environmental variables")
    def test_all_cls(self):
        """Test all method with specified cls."""
        obj = models.storage.all(BaseModel)
        self.assertEqual(type(obj), dict)
        self.assertEqual(len(obj), 1)
        self.assertEqual(self.base, list(obj.values())[0])

    @unittest.skipIf(os.getenv("HBNB_ENV") != "test",
                     "Requires MySQL environmental variables")
    def test_new(self):
        """Test new method."""
        self.new()
        store = list(DBStorage._DBStorage__session.new)
        self.assertIn(self.state, store)
        self.assertIn(self.city, store)

    @unittest.skipIf(os.getenv("HBNB_ENV") != "test",
                     "Requires MySQL environmental variables")
    def test_save(self):
        """Test save method."""
        self.new()
        models.storage.save()
        store = models.storage.all()
        self.assertIn(self.state, store)
        self.assertIn(self.city, store)

    @unittest.skipIf(os.getenv("HBNB_ENV") != "test",
                     "Requires MySQL environmental variables")
    def test_delete(self):
        """Test delete method."""
        st = State()
        models.storage.new(st)
        models.storage.save(st)
        models.storage.delete(st)
        models.storage.save(st)
        self.assertNotIn(st, models.storage.all(State))

    @unittest.skipIf(os.getenv("HBNB_ENV") != "test",
                     "Requires MySQL environmental variables")
    def test_delete_none(self):
        """Test delete method with None."""
        try:
            models.storage.delete(None)
        except Exception:
            self.fail

    @unittest.skipIf(os.getenv("HBNB_ENV") != "test",
                     "Requires MySQL environmental variables")
    def test_reload(self):
        """Test reload method."""
        og_session = models.storage._DBStorage__session
        models.storage.reload()
        self.assertEqual(Session, type(models.storage._DBStorage__session))
        self.assertNotEqual(og_session, models.storage._DBStorage__session)


if __name__ == "__main__":
    unittest.main()
