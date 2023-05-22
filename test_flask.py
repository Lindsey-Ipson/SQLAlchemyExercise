from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors real errors, rather than HTML pages with error info
app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for Users"""

    def setUp(self):
        """Add sample user"""

        User.query.delete()

        user = User(first_name="Mal", last_name="Tese", img_url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/Maltese_600.jpg/440px-Maltese_600.jpg")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()
        db.session.query(User).delete()
        db.session.commit()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Mal Tese', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Mal Tese</h1>', html)

    def test_add_user(self):
        with app.test_client() as client:
            u = {'first-name': 'Cor', 'last-name': 'Gie', 'img-url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/Welchcorgipembroke.JPG/440px-Welchcorgipembroke.JPG'}
            resp = client.post("/users/new", data=u, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Cor Gie", html)

    def test_edit_user(self):
        with app.test_client() as client:
            u = {'first-name': 'MalTwo', 'last-name': 'TeseTwo', 'img-url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/Maltese_600.jpg/440px-Maltese_600.jpg'}
            resp = client.post(f"/users/{self.user_id}/edit", data=u, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("MalTwo TeseTwo", html)
    
    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.post(f"/users/{self.user_id}/delete")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)
            self.assertNotIn(html, "Mal Tese")