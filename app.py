"""Blogly application."""

from flask import Flask, request, render_template,  redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "TopSecret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# debug = DebugToolbarExtension(app)
toolbar = DebugToolbarExtension(app)

connect_db(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET'])
def redirect_to_users():
    """Homepage redirects to list of users."""
    return redirect("/users")

@app.route('/users', methods=['GET'])
def show_all_users():
        # with app.app_context():
            users = User.query.all()
            return render_template('user-listing.html', users=users)

@app.route('/users/new', methods=['GET'])
def show_user_form():
    
    return render_template('new-user-form.html')

@app.route('/users/new', methods=['POST'])
def create_user():
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    img_url = request.form['img-url']
    img_url = img_url if img_url else None

    new_user = User(first_name=first_name, last_name=last_name, img_url=img_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>', methods=['GET'])
def show_user_info(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user-detail-page.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['GET'])
def show_edit_page(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user-edit-page.html', user=user)



@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_users(user_id):

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first-name']
    user.last_name = request.form['last-name']
    user.image_url = request.form['img-url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    
    return redirect('/users')






