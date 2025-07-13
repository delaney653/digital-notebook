import unittest
import os
import sys
import time
from sqlalchemy.exc import OperationalError

os.environ["ENV"] = "testing"
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.app import app, db, Note


class FlaskTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = (
            "mysql+pymysql://root:password@mysql-test/test_notes"
        )
        self.app = app.test_client()
        with app.app_context():
            for _ in range(10):
                try:
                    db.create_all()
                    break
                except OperationalError:
                    print("Test database not ready, retrying in 1s...")
                    time.sleep(2)
            else:
                raise Exception("Could not connect to test database after 5 tries")

    def tearDown(self):
        # Cleans DB
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home_page_data(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Choose your color!", response.data)
        self.assertIn(b'style="background-color: AntiqueWhite;"', response.data)

    def test_add_color(self):
        """Test adding a color"""
        response = self.app.post("/add", data={"note": "Crimson"})
        self.assertEqual(response.status_code, 302)  # redirects

        response = self.app.get("/")
        self.assertIn(b"Crimson:", response.data)
        self.assertIn(b"chosen the best color", response.data)
        self.assertIn(b". I vote we stick with this color!", response.data)

    def test_delete_color(self):
        """Test deleting a color"""
        self.app.post("/add", data={"note": "Plum"})
        response = self.app.get("/")
        self.assertIn(b"Plum:", response.data)

        response = self.app.post("/delete/1")
        self.assertEqual(response.status_code, 302)  # redirects

        response = self.app.get("/")
        self.assertNotIn(b"Crimson:", response.data)
        self.assertIn(b'style="background-color: AntiqueWhite;"', response.data)

    def test_reset_color_history(self):
        """Testing clearing the color history"""
        self.app.post("/add", data={"note": "Plum"})
        self.app.post("/add", data={"note": "LightBlue"})

        response = self.app.get("/")
        self.assertIn(b"Plum:", response.data)
        self.assertIn(b"LightBlue:", response.data)

        response = self.app.post("/reset")
        self.assertEqual(response.status_code, 302)  # redirects
        response = self.app.get("/")

        self.assertNotIn(b"Plum:", response.data)
        self.assertNotIn(b"LightBlue:", response.data)
        self.assertIn(b'style="background-color: AntiqueWhite;"', response.data)

    def test_multiple_color_changes(self):
        """Test adding multiple colors"""
        chosen_colors = ["Plum", "Ivory", "Crimson"]

        for color in chosen_colors:
            self.app.post("/add", data={"note": color})

        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)

        for color in chosen_colors:
            self.assertIn(color.encode(), response.data)
        self.assertIn(b'style="background-color: Crimson;"', response.data)
        self.assertIn(b". I vote we stick with this color!", response.data)

    def test_color_not_red_logic(self):
        """Test logic for multiple non-red colors"""
        self.app.post("/add", data={"note": "LightBlue"})
        response = self.app.get("/")
        self.assertIn(b"ugly color", response.data)

        self.app.post("/add", data={"note": "LightSeaGreen"})
        response = self.app.get("/")
        self.assertIn(b"Better than the last one", response.data)

        self.app.post("/add", data={"note": "Plum"})
        response = self.app.get("/")
        self.assertIn(b"Please just stick to crimson.", response.data)


if __name__ == "__main__":
    unittest.main()
