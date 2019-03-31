#!/usr/bin/python3
"""Defines unnittests for models/user.py."""
import os
import pep8
import unittest
import models
from datetime import datetime
from models.base_model import BaseModel
from models.user import User
from models.engine.file_storage import FileStorage


class TestUser(unittest.TestCase):
    """Unittests for testing the User class."""

    @classmethod
    def setUpClass(cls):
        """User testing setup.

        Temporarily renames any existing file.json.
        Resets FileStorage objects dictionary.
        Creates a User instance for testing.
        """
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}
        cls.user = User()
        cls.user.email = "g@gmail.com"
        cls.user.password = "drowssap"
        cls.user.first_name = "Gob"
        cls.user.last_name = "Bog"

    @classmethod
    def tearDownClass(cls):
        """User testing teardown.

        Restore original file.json.
        Delete the test User instance.
        """
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        del cls.user

    def test_pep8(self):
        """Test pep8 styling."""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(["models/user.py"])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_docstrings(self):
        """Check for docstrings."""
        self.assertIsNotNone(User.__doc__)

    def test_attributes(self):
        """Check for attributes."""
        us = User()
        self.assertEqual(str, type(us.id))
        self.assertEqual(datetime, type(us.created_at))
        self.assertEqual(datetime, type(us.updated_at))
        self.assertEqual(str, type(us.email))
        self.assertEqual(str, type(us.password))
        self.assertEqual(str, type(us.first_name))
        self.assertEqual(str, type(us.last_name))

    def test_is_subclass(self):
        """Check that User is a subclass of BaseModel."""
        self.assertTrue(issubclass(User, BaseModel))

    def test_init(self):
        """Test initialization."""
        self.assertTrue(isinstance(self.user, User))
        self.assertIn(self.user, models.storage.all().values())

    def test_two_models_are_unique(self):
        """Test that different User instances are unique."""
        us = User()
        self.assertNotEqual(self.user.id, us.id)
        self.assertLess(self.user.created_at, us.created_at)
        self.assertLess(self.user.updated_at, us.updated_at)

    def test_init_args_kwargs(self):
        """Test initialization with args and kwargs."""
        dt = datetime.today()
        us = User("1", id="5", created_at=dt.isoformat())
        self.assertEqual(us.id, "5")
        self.assertEqual(us.created_at, dt)

    def test_str(self):
        """Test __str__ representation."""
        s = self.user.__str__()
        self.assertIn("[User] ({})".format(self.user.id), s)
        self.assertIn("'id': '{}'".format(self.user.id), s)
        self.assertIn("'created_at': {}".format(repr(self.user.created_at)), s)
        self.assertIn("'updated_at': {}".format(repr(self.user.updated_at)), s)
        self.assertIn("'email': '{}'".format(self.user.email), s)
        self.assertIn("'password': '{}'".format(self.user.password), s)
        self.assertIn("'first_name': '{}'".format(self.user.first_name), s)
        self.assertIn("'last_name': '{}'".format(self.user.last_name), s)

    def test_save(self):
        """Test save method."""
        old = self.user.updated_at
        self.user.save()
        self.assertLess(old, self.user.updated_at)
        with open("file.json", "r") as f:
            self.assertIn("User." + self.user.id, f.read())

    def test_to_dict(self):
        """Test to_dict method."""
        user_dict = self.user.to_dict()
        self.assertEqual(dict, type(user_dict))
        self.assertEqual(self.user.id, user_dict["id"])
        self.assertEqual("User", user_dict["__class__"])
        self.assertEqual(self.user.created_at.isoformat(),
                         user_dict["created_at"])
        self.assertEqual(self.user.updated_at.isoformat(),
                         user_dict["updated_at"])
        self.assertEqual(self.user.email, user_dict["email"])
        self.assertEqual(self.user.password, user_dict["password"])
        self.assertEqual(self.user.first_name, user_dict["first_name"])
        self.assertEqual(self.user.last_name, user_dict["last_name"])


if __name__ == "__main__":
    unittest.main()
