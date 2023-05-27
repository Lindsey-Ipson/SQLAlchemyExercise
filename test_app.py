from unittest import TestCase
from sqlalchemy import inspect

from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors real errors, rather than HTML pages with error info
app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

User.query.delete()
Post.query.delete()

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
        """Clean up any fouled transaction"""
        db.session.rollback()
 

    def test_list_users(self):
        """Test list of users"""
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Mal Tese', html)


    def test_show_user(self):
        """Test user details page"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Mal Tese</h1>', html)


    def test_add_user(self):
        """Test adding user"""
        with app.test_client() as client:
            u = {'first-name': 'Cor', 'last-name': 'Gie', 'img-url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/Welchcorgipembroke.JPG/440px-Welchcorgipembroke.JPG'}
            resp = client.post("/users/new", data=u, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Cor Gie", html)


    def test_edit_user(self):
        """Test editing user"""
        with app.test_client() as client:
            u = {'first-name': 'MalTwo', 'last-name': 'TeseTwo', 'img-url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/Maltese_600.jpg/440px-Maltese_600.jpg'}
            resp = client.post(f"/users/{self.user_id}/edit", data=u, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("MalTwo TeseTwo", html)
    

    def test_delete_user(self):
        """Test deleting user"""
        with app.test_client() as client:
            resp = client.post(f"/users/{self.user_id}/delete")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)
            self.assertNotIn(html, "Mal Tese")


class PostViewsTestCase(TestCase):
    """Tests for views for Posts"""

    def setUp(self):
        """Add sample user"""

        User.query.delete()

        user = User(first_name="Mal", last_name="Tese", img_url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/Maltese_600.jpg/440px-Maltese_600.jpg")
        db.session.add(user)
        db.session.commit()

        Post.query.delete()

        post = Post(title="Set Up Test Post", content="Set Up Test Post Content", user=user)
        db.session.add(post)
        db.session.commit()

        self.user_id = user.id
        self.post_id = post.id


    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()
        db.session.query(Post).delete()
        db.session.query(User).delete()
        db.session.commit()


    def test_add_post(self):
        """Test adding post"""
        with app.test_client() as client:
            form_data = {
                'title': 'Test Title',
                'content': 'Test Content',
            }
            resp = client.post(f"/users/{self.user_id}/posts/new", data=form_data, follow_redirects=True)
            
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test Title', html)


    def test_edit_post(self):
        """Test editing post"""
        with app.test_request_context():
            # Simulate an authenticated user
            with app.test_client() as client:
                with client.session_transaction() as session:
                    user = User.query.get_or_404(self.user_id)
                    session['user_id'] = user.id

                form_data = {
                    'title': 'Set Up Test Post Edited',
                    'content': 'Set Up Test Content Edited',
                }
                resp = client.post(f'/posts/{self.post_id}/edit', data=form_data, follow_redirects=True)
                html = resp.get_data(as_text=True)

                self.assertEqual(resp.status_code, 200)
                self.assertIn('Set Up Test Post Edited', html)


    def test_delete_post(self):
        """Test deleting post"""
        with app.test_client() as client:
            resp = client.post(f'/posts/{self.post_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)
            print('HTML==============================>', html)
            self.assertEqual(resp.status_code, 200)
            # &#39; represents single quotation mark
            self.assertIn("Post &#39;Set Up Test Post&#39; by Mal Tese deleted.", html)

 



