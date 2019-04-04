#!/usr/bin/python3
"""Defines unnittests for models/review.py."""
import os
import pep8
import MySQLdb
import unittest
from datetime import datetime
from models.base_model import Base, BaseModel
from models.review import Review
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker


class TestReview(unittest.TestCase):
    """Unittests for testing the Review class."""

    @classmethod
    def setUpClass(cls):
        """Review testing setup.
        Temporarily renames any existing file.json.
        Resets FileStorage objects dictionary.
        Creates FileStorage, DBStorage and Review instances for testing.
        """
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}
        cls.filestorage = FileStorage()
        cls.review = Review(email="poppy@holberton.com", password="betty98")

        if os.getenv("HBNB_ENV") is None:
            return
        cls.dbstorage = DBStorage()
        Base.metadata.create_all(cls.dbstorage._DBStorage__engine)
        session_factory = sessionmaker(bind=cls.dbstorage._DBStorage__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        cls.dbstorage._DBStorage__session = Session()

    @classmethod
    def tearDownClass(cls):
        """Review testing teardown.
        Restore original file.json.
        Delete the FileStorage, DBStorage and Review test instances.
        """
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        if os.getenv("HBNB_ENV") is not None:
            cls.dbstorage._DBStorage__session.close()
            del cls.dbstorage
        del cls.review
        del cls.filestorage

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
        us = Review(email="a", password="a")
        self.assertEqual(str, type(us.id))
        self.assertEqual(datetime, type(us.created_at))
        self.assertEqual(datetime, type(us.updated_at))
        self.assertTrue(hasattr(us, "__tablename__"))
        self.assertTrue(hasattr(us, "text"))
        self.assertTrue(hasattr(us, "place_id"))
        self.assertTrue(hasattr(us, "user_id"))

    @unittest.skipIf(os.getenv("HBNB_ENV") is None, "MySQL env vars required")
    def test_email_not_nullable(self):
        """Test that email attribute is non-nullable."""
        with self.assertRaises(OperationalError):
            self.dbstorage._DBStorage__session.add(Review(password="a"))
            self.dbstorage._DBStorage__session.commit()
        self.dbstorage._DBStorage__session.rollback()
        with self.assertRaises(OperationalError):
            self.dbstorage._DBStorage__session.add(Review(email="a"))
            self.dbstorage._DBStorage__session.commit()

    def test_is_subclass(self):
        """Check that Review is a subclass of BaseModel."""
        self.assertTrue(issubclass(Review, BaseModel))

    def test_init(self):
        """Test initialization."""
        self.assertIsInstance(self.review, Review)

    def test_two_models_are_unique(self):
        """Test that different Review instances are unique."""
        us = Review(email="a", password="a")
        self.assertNotEqual(self.review.id, us.id)
        self.assertLess(self.review.created_at, us.created_at)
        self.assertLess(self.review.updated_at, us.updated_at)

    def test_init_args_kwargs(self):
        """Test initialization with args and kwargs."""
        dt = datetime.utcnow()
        st = Review("1", id="5", created_at=dt.isoformat())
        self.assertEqual(st.id, "5")
        self.assertEqual(st.created_at, dt)

    def test_str(self):
        """Test __str__ representation."""
        s = self.review.__str__()
        self.assertIn("[Review] ({})".format(self.review.id), s)
        self.assertIn("'id': '{}'".format(self.review.id), s)
        self.assertIn("'created_at': {}".format(
            repr(self.review.created_at)), s)
        self.assertIn("'updated_at': {}".format(
            repr(self.review.updated_at)), s)
        self.assertIn("'email': '{}'".format(self.review.email), s)
        self.assertIn("'password': '{}'".format(self.review.password), s)

    @unittest.skipIf(os.getenv("HBNB_ENV") is not None, "Testing DBStorage")
    def test_save_filestorage(self):
        """Test save method with FileStorage."""
        old = self.review.updated_at
        self.review.save()
        self.assertLess(old, self.review.updated_at)
        with open("file.json", "r") as f:
            self.assertIn("Review." + self.review.id, f.read())

    @unittest.skipIf(os.getenv("HBNB_ENV") is None, "MySQL env vars required")
    def test_save_dbstorage(self):
        """Test save method with DBStorage."""
        old = self.review.updated_at
        self.review.save()
        self.assertLess(old, self.review.updated_at)
        db = MySQLdb.connect(review="hbnb_test",
                             passwd="hbnb_test_pwd",
                             db="hbnb_test_db")
        cursor = db.cursor()
        cursor.execute("SELECT * \
                          FROM `reviews` \
                         WHERE BINARY email = '{}'".
                       format(self.review.email))
        query = cursor.fetchall()
        self.assertEqual(1, len(query))
        self.assertEqual(self.review.id, query[0][0])
        cursor.close()

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
        self.assertEqual(self.review.email, review_dict["email"])
        self.assertEqual(self.review.password, review_dict["password"])


if __name__ == "__main__":
    unittest.main()
