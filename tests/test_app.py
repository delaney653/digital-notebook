import unittest
from app import app

class FlaskTests(unittest.TestCase):
    def setUp(self):
        #test client for each test
        self.app = app.test_client()

    def test_home_page_status_code(self):
        res = self.app.get('/')
        self.assertEqual(res.status_code, 200)

    def test_home_page_content(self):
        res = self.app.get('/')
        self.assertIn(b"Choose your color!", res.data)  # Change to a string inside index.html

    def test_get_default_color(self):
        response = self.client.get("/color")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["value"], "#FFFFFF")

    def test_set_valid_color(self):
        response = self.client.post("/color", json={"color": "#FF00FF"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["value"], "#FF00FF")

    def test_set_invalid_color(self):
        response = self.client.post("/color", json={"color": "not-a-color"})
        self.assertEqual(response.status_code, 400)

    def test_delete_resets_color(self):
        self.client.post("/color", json={"color": "#000000"})
        response = self.client.delete("/color")
        self.assertEqual(response.get_json()["value"], "#FFFFFF")

    def test_multiple_color_changes(self):
        colors = ["#123456", "#ABCDEF", "#000"]
        for color in colors:
            self.client.post("/color", json={"color": color})
            response = self.client.get("/color")
            self.assertEqual(response.get_json()["value"], color)

if __name__ == "__main__":
    unittest.main()

if __name__ == '__main__':
    unittest.main()