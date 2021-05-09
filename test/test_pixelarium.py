import unittest
import os
# from pixelarium import server
# from pixelarium import model
# # import server as server
from pixelarium.server import app
from pixelarium.seed import populate_database
from pixelarium.model import db, connect_to_db, sample_data

class PixelariumTests(unittest.TestCase):
    """Tests for Pixelarium image repository"""

    def setUp(self):
        self.client = app.test_client()
        app.config["TESTING"] = True


    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn(b"Welcome to Pixelarium", result.data)
    
    def test_search(self):
        result = self.client.post("/results")
        self.assertIn(b"Your search", result.data)
        self.assertNotIn(b"Welcome")

    def test_no_results(self):
        result = self.client.post("/results", data={"search": ""})
        self.assertIn(b"No results")

    def tearDown(self):
        """Do at end of every test."""

        # (uncomment when testing database)
        db.session.close()
        db.drop_all()

class PixelariumDatabaseTests(unittest.TestCase):
    """Tests for Pixelarium database"""

    def setUp(self):
        self.client = app.test_client()
        app.config["TESTING"] = True

        os.system("dropdb testdb")
        os.system("createdb testdb")

        # Connect to test database (uncomment when testing database)
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data (uncomment when testing database)
        db.create_all()
        example_data()


if __name__ == "__main__":
    unittest.main()