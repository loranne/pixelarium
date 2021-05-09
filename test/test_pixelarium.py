import unittest
import os
# from pixelarium import server
# from pixelarium import model
# # import server as server
from pixelarium.server import app
from pixelarium.seed import populate_database
from pixelarium.model import db, connect_to_db, sample_data, Image, Tag, ImageTag

class PixelariumStaticTests(unittest.TestCase):
    """Tests for Pixelarium image repository"""

    def setUp(self):
        self.client = app.test_client()
        app.config["TESTING"] = True

    # checks homepage for 200 (responsive) status
    def test_homepage(self):
        response = self.client.get("/")
        self.assertIn(b"Welcome to Pixelarium", response.data)
        assert response.status_code == 200

    def tearDown(self):
        """Not really necessary for these tests."""


class PixelariumDatabaseTests(unittest.TestCase):
    """Tests for Pixelarium database"""

    def setUp(self):
        """Initialize the pixtestdb and populate with data"""

        self.client = app.test_client()
        app.config["TESTING"] = True

        os.system("dropdb pixtestdb")
        os.system("createdb pixtestdb")

        # Connect to test database (uncomment when testing database)
        connect_to_db(app, "postgresql:///pixtestdb")

        # Create tables and add sample data (uncomment when testing database)
        db.create_all()
        sample_data()

    # test search string passed correctly
    def test_search_results(self):
        response = self.client.post("/results", data={"search": "cats"})
        self.assertIn(b"cats", response.data)
        self.assertNotIn(b"Welcome", response.data)
        self.assertTrue(response.status_code == 200)

    # test no results page
    def test_no_results(self):
        response = self.client.post("/results", data={"search": ""})
        self.assertIn(b"No results", response.data)
        self.assertTrue(response.status_code == 200)
    
    # test browse all page
    def test_browse(self):
        response = self.client.get("/browse")
        self.assertIn(b"Browse all", response.data)
        self.assertTrue(response.status_code == 200)

    # test fuzzy string match
    def test_search_query_string_match(self):
        """Test of search_images function"""
        response = self.client.post("/results", data={"search": "pet"})
        self.assertIn(b"pets", response.data)
    
    # test for searching by keyword
    def test_search_query_tag(self):
        """Test of search_images function"""
        response = self.client.post("/results", data={"search": "tag: travel"})
        self.assertIn(b"italy", response.data)
        self.assertNotIn(b"pets", response.data)

    # test exact match search
    def test_search_exact(self):
        """Test of searching images for exact matches"""
        response = self.client.post("/results", data={"search": '"Sample Image - Travel"'})
        self.assertIn(b"italy", response.data)
        self.assertNotIn(b"landscape", response.data)

    def tearDown(self):
        """Drop all tables in pixtestdb, which gets torn down and recreated during setUp"""
        db.drop_all()


# class PixelariumQueryTests(unittest.TestCase):
#     """Tests for search queries and fuzzy string matching"""

#     def setUp(self):
#         """Initialize the pixtestdb and populate with data"""
        
#         self.client = app.test_client()
#         app.config["TESTING"] = True

#         os.system("dropdb pixpixtestdb")
#         os.system("createdb pixpixtestdb")

#         # Connect to test database (uncomment when testing database)
#         connect_to_db(app, "postgresql:///pixtestdb")

#         # Create tables and add sample data (uncomment when testing database)
#         db.create_all()
#         sample_data()

    


    # def tearDown(self):
    #     """Drop all tables in pixtestdb, which gets torn down and recreated during setUp"""
    #     db.drop_all()


if __name__ == "__main__":
    unittest.main()