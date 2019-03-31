#!/usr/bin/python3
"""Defines unnittests for models/review.py."""
import os
import pep8
import unittest
import models
from datetime import datetime
from models.base_model import BaseModel
from models.review import Review
from models.engine.file_storage import FileStorage


class TestReview(unittest.TestCase):
    """Unittests for testing the Review class."""

    @classmethod
    def setUpClass(cls):
        """Review testing setup.

        Temporarily renrves any existing file.json.
        Resets FileStorage objects dictionary.
        Creates a Review instance for testing.
        """
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}
        cls.review = Review()
        cls.review.place_id = "415"
        cls.review.user_id = "7"
        cls.review.text = "San Frantastic"

    @classmethod
    def tearDownClass(cls):
        """Review testing teardown.

        Restore original file.json.
        Delete the test Review instance.
        """
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        del cls.review

    def test_pep8(self):
        """Test pep8 styling."""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(["models/review.py"])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_docstrings(self):
        """Check for docstrings."""
        self.assertIsNotNone(Review.__doc__)

    def test_attributes(self):
        """Check for attributes."""
        rv = Review()
        self.assertEqual(str, type(rv.id))
        self.assertEqual(datetime, type(rv.created_at))
        self.assertEqual(datetime, type(rv.updated_at))
        self.assertEqual(str, type(rv.place_id))
        self.assertEqual(str, type(rv.user_id))
        self.assertEqual(str, type(rv.text))

    def test_is_subclass(self):
        """Check that Review is a subclass of BaseModel."""
        self.assertTrue(issubclass(Review, BaseModel))

    def test_init(self):
        """Test initialization."""
        self.assertTrue(isinstance(self.review, Review))
        self.assertIn(self.review, models.storage.all().values())

    def test_two_models_are_unique(self):
        """Test that different Review instances are unique."""
        rv = Review()
        self.assertNotEqual(self.review.id, rv.id)
        self.assertLess(self.review.created_at, rv.created_at)
        self.assertLess(self.review.updated_at, rv.updated_at)

    def test_init_args_kwargs(self):
        """Test initialization with args and kwargs."""
        dt = datetime.today()
        rv = Review("1", id="5", created_at=dt.isoformat())
        self.assertEqual(rv.id, "5")
        self.assertEqual(rv.created_at, dt)

    def test_str(self):
        """Test __str__ representation."""
        s = self.review.__str__()
        self.assertIn("[Review] ({})".format(self.review.id), s)
        self.assertIn("'id': '{}'".format(self.review.id), s)
        self.assertIn("'created_at': {}".format(
            repr(self.review.created_at)), s)
        self.assertIn("'updated_at': {}".format(
            repr(self.review.updated_at)), s)
        self.assertIn("'place_id': '{}'".format(self.review.place_id), s)
        self.assertIn("'user_id': '{}'".format(self.review.user_id), s)
        self.assertIn("'text': '{}'".format(self.review.text), s)

    def test_save(self):
        """Test save method."""
        old = self.review.updated_at
        self.review.save()
        self.assertLess(old, self.review.updated_at)
        with open("file.json", "r") as f:
            self.assertIn("Review." + self.review.id, f.read())

    def test_to_dict(self):
        """Test to_dict method."""
        review_dict = self.review.to_dict()
        self.assertEqual(dict, type(review_dict))
        self.assertEqual(self.review.id, review_dict["id"])
        self.assertEqual("Review", review_dict["__class__"])
        self.assertEqual(self.review.created_at.isoformat(),
                         review_dict["created_at"])
        self.assertEqual(self.review.updated_at.isoformat(),
                         review_dict["updated_at"])
        self.assertEqual(self.review.place_id, review_dict["place_id"])
        self.assertEqual(self.review.user_id, review_dict["user_id"])
        self.assertEqual(self.review.text, review_dict["text"])


if __name__ == "__main__":
    unittest.main()
