"""Blogly application."""

from flask import Flask, request, render_template,  redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "TopSecret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

connect_db(app)

with app.app_context():
    db.create_all()

# ______________________ General Routes ______________________

@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""
    return render_template('404.html'), 404


@app.route('/recent-posts')
def root():
    """Show recent list of posts, most-recent first."""
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('homepage.html', posts=posts)

# ______________________ User Routes ______________________

@app.route('/', methods=['GET'])
def redirect_to_users():
    """Redirects to list of users."""
    return redirect("/users")


@app.route('/users', methods=['GET'])
def show_all_users():
    """Display list of users"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('user-listing.html', users=users)


@app.route('/users/new', methods=['GET'])
def show_user_form():
    """Display new user form"""
    return render_template('user-new.html')


@app.route('/users/new', methods=['POST'])
def create_user():
    """Send new user to database, redirect to user list"""
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    img_url = request.form['img-url']
    img_url = img_url if img_url else None

    new_user = User(first_name=first_name, last_name=last_name, img_url=img_url)

    db.session.add(new_user)
    db.session.commit()

    flash(f"User {new_user.full_name} added.")

    return redirect('/users')


@app.route('/users/<int:user_id>', methods=['GET'])
def show_user_info(user_id):
    """Display user details"""
    user = User.query.get_or_404(user_id)
    posts = user.posts
    return render_template('user-detail.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['GET'])
def show_edit_page(user_id):
    """Display form to edit user info"""
    user = User.query.get_or_404(user_id)
    return render_template('user-edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_users(user_id):
    """Send new user info and add to database. Redirect to user list"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first-name']
    user.last_name = request.form['last-name']
    user.image_url = request.form['img-url']

    db.session.add(user)
    db.session.commit()

    flash(f"User {user.full_name} edited.")

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete user from database and redirect to user list"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    flash(f"User {user.full_name} deleted.")
    
    return redirect('/users')


@app.route('/users/<int:user_id>/posts/new', methods=['GET'])
def show_new_post_form(user_id):
    """Display new post form"""
    user = User.query.get_or_404(user_id)
    return render_template('post-new.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def send_new_post(user_id):
    """Send new post to database, redirect to user list"""
    title = request.form['title']
    content = request.form['content']
    user = User.query.get_or_404(user_id)

    new_post = Post(title=title, content=content, user=user)

    db.session.add(new_post)
    db.session.commit()

    flash(f"Post '{new_post.title}' added.")

    return redirect(f'/users/{user.id}')

# ______________________ Post Routes ______________________

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Display single post with title and content. Show buttons to edit and delete post"""
    post = Post.query.get_or_404(post_id)
    user=post.user
    return render_template('post-detail.html', post=post, user=user)


@app.route('/posts/<int:post_id>/edit', methods=['GET'])
def show_edit_post_form(post_id):
    """Show form to edit post"""
    post = Post.query.get_or_404(post_id)
    user = post.user
    return render_template('post-edit.html', post=post, user=user)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def send_edited_post(post_id):
    """Send edited form and redirect to the user of the edited post"""
    post = Post.query.get_or_404(post_id)
    user = post.user
    user_id = user.id
    title = request.form['title']
    content = request.form['content']

    post.title = title
    post.content = content

    db.session.add(post)
    db.session.commit()

    flash(f"Post '{post.title}' edited.")

    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Handle form submission for deleting a post and redirect to the user of the deleted post"""
    post = Post.query.get_or_404(post_id)
    user = post.user
    print("pipi")
    print(user)
    user_id = user.id

    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title}' by {user.full_name} deleted.")

    return redirect(f'/users/{user_id}')
