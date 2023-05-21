"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True
                   )
    first_name = db.Column(db.String(40),
                     nullable=False,
                     unique=True)
    last_name = db.Column(db.String(40),
                     nullable=False,
                     unique=True)
    img_url = db.Column(db.String,
                          nullable=True,
                          unique=False,
                          default='https://cdn-icons-png.flaticon.com/512/727/727399.png?w=1060&t=st=1684565167~exp=1684565767~hmac=7044db93169614d3b84113687f6c3dc9ca966ba7cf924aa49d77d01a4ea2e877')
    

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)
    return app
    