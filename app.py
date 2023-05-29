"""Blogly application."""

from flask import Flask, request, render_template,  redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

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
    return render_template('general/404.html'), 404


@app.route('/recent-posts')
def root():
    """Show recent list of posts, most-recent first."""
    posts = Post.query.order_by(Post.created_at.desc()).limit(15).all()
    return render_template('general/homepage.html', posts=posts)

# ______________________ User Routes ______________________

@app.route('/', methods=['GET'])
def redirect_to_users():
    """Redirects to list of users."""
    return redirect("/users")


@app.route('/users', methods=['GET'])
def show_all_users():
    """Display list of users"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/user-list.html', users=users)


@app.route('/users/new', methods=['GET'])
def show_user_form():
    """Display new user form"""
    return render_template('users/user-new.html')


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
    return render_template('users/user-detail.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['GET'])
def show_edit_page(user_id):
    """Display form to edit user info"""
    user = User.query.get_or_404(user_id)
    return render_template('users/user-edit.html', user=user)


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

# ______________________ Post Routes ______________________

@app.route('/users/<int:user_id>/posts/new', methods=['GET'])
def show_new_post_form(user_id):
    """Display new post form"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('posts/post-new.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def send_new_post(user_id):
    """Send new post to database, redirect to user list"""
    title = request.form['title']
    content = request.form['content']
    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist('tags')]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title=title, content=content, user=user, tags=tags)

    db.session.add(new_post)
    db.session.commit()

    flash(f"Post '{new_post.title}' added.")

    return redirect(f'/users/{user.id}')


@app.route('/posts/<int:post_id>', methods=['GET'])
# ^ methods just added
def show_post(post_id):
    """Display single post with title and content. Show buttons to edit and delete post"""
    post = Post.query.get_or_404(post_id)
    user = post.user

    return render_template('posts/post-detail.html', post=post, user=user)


@app.route('/posts/<int:post_id>/edit', methods=['GET'])
def show_edit_post_form(post_id):
    """Show form to edit post"""
    post = Post.query.get_or_404(post_id)
    user = post.user
    tags = Tag.query.all()
    return render_template('posts/post-edit.html', post=post, user=user,tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def send_edited_post(post_id):
    """Send edited form and redirect to the user of the edited post"""
    post = Post.query.get_or_404(post_id)
    user = post.user
    user_id = user.id
    title = request.form['title']
    content = request.form['content']
    tag_ids = [int(num) for num in request.form.getlist('tags')]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    post.title = title
    post.content = content
    post.tags = tags

    db.session.add(post)
    db.session.commit()

    flash(f"Post '{post.title}' edited.")

    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Handle form submission for deleting a post and redirect to the user of the deleted post"""
    post = Post.query.get_or_404(post_id)
    user = post.user
    user_id = user.id

    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title}' by {user.full_name} deleted.")

    return redirect(f'/users/{user_id}')

# ______________________ Tag Routes ______________________

@app.route('/tags', methods=['GET'])   
def list_tags():
    """Lists all tags, with links to the tag detail page"""
    tags = Tag.query.order_by(Tag.name).all()
    return render_template('tags/tag-list.html', tags=tags)


@app.route('/tags/<int:tag_id>', methods=['GET'])   
def show_tag_details(tag_id):
    """Show details about a tag. Have links to edit form and to delete"""
    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts
    return render_template('tags/tag-detail.html', tag=tag, posts=posts)


@app.route('/tags/new', methods=['GET'])   
def show_add_tag_form():
    """Show a form to add a new tag, and posts to which that tag can be added"""
    posts = Post.query.all()
    return render_template('tags/tag-new.html', posts=posts)


@app.route('/tags/new', methods=['POST'])   
def add_tag():
    """Process add form, add tag, add that tag to any checked posts, and redirect to tag list"""

    post_ids = [int(num) for num in request.form.getlist('posts')]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    name = request.form['name']
    new_tag = Tag(name=name, posts=posts)

    db.session.add(new_tag)
    db.session.commit()

    flash(f"Tag '{new_tag.name}' added.")

    return redirect('/tags')


@app.route('/tags/<int:tag_id>/edit', methods=['GET'])   
def show_edit_tag_form(tag_id):
    """Show edit form for a tag"""
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('tags/tag-edit.html', tag=tag, posts=posts)


@app.route('/tags/<int:tag_id>/edit', methods=['POST'])   
def edit_tag(tag_id):
    """Process edit form, edit tag, and redirect to the tags list"""

    tag = Tag.query.get_or_404(tag_id)
    new_name = request.form['name']
    tag.name = new_name
    post_ids = [int(num) for num in request.form.getlist('posts')]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()

    flash(f"Tag '{tag.name}' edited.")

    return redirect('/tags')


@app.route('/tags/<int:tag_id>/delete', methods=['POST'])   
def delete_tag(tag_id):
    """Delete a tag.""" 

    tag = Tag.query.get(tag_id)
    db.session.delete(tag)
    db.session.commit()

    flash(f"Tag '{tag.name}' deleted.")

    return redirect('/tags')
