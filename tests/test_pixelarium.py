import unittest
import server
from server import app
from model import db, connect_to_db, example_data

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
        self.assertIn(b"")



if __name__ == "__main__":
    unittest.main()