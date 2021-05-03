import unittest

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
        result = self.client.get("/")
        self.assertIn(b"your search", result.data)
        self.assertNotIn(b"Welcome")