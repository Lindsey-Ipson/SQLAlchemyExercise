"""Models for Dog Blog"""

from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class User(db.Model):
    """Site user"""

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True
                   )
    first_name = db.Column(db.String(40),
                        nullable=False)
    last_name = db.Column(db.String(40),
                    nullable=False)
    img_url = db.Column(db.String,
                          nullable=True,
                          unique=False,
                          default='https://cdn-icons-png.flaticon.com/512/727/727399.png?w=1060&t=st=1684565167~exp=1684565767~hmac=7044db93169614d3b84113687f6c3dc9ca966ba7cf924aa49d77d01a4ea2e877')

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")
    
    @property
    def full_name(self):
        """Return user's full name"""

        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        return f"User {self.id} {self.first_name} {self.last_name} {self.img_url}"
    

class Post(db.Model):
    """Blog post"""

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, 
                   autoincrement=True)
    
    title = db.Column(db.String,
                     nullable=False)
    content = db.Column(db.String,
                     nullable=False)
    created_at = db.Column(db.DateTime, 
                           default=datetime.datetime.now,
                           nullable=False)
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.id'))
    
    @property
    def friendly_date(self):
        """Return nicely-formatted date."""
        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")

    def __repr__(self):
        return f"Post {self.id} {self.title} {self.content} {self.created_at} {self.user_id}"
    

class Tag(db.Model):
    """Blog tag"""

    __tablename__ = 'tags'

    id = db.Column(db.Integer,
                   primary_key=True, 
                   autoincrement=True)
    name = db.Column(db.String,
                     nullable=False,
                     unique=True)
    
    posts = db.relationship('Post', secondary='posts_tags', backref='tags')
    
    def __repr__(self):
        return f"Tag {self.id} {self.name}"
    

class PostTag(db.Model):
    """Post-Tag relationship"""

    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'),
                        primary_key=True)
    
    tag_id = db.Column(db.Integer,
                       db.ForeignKey('tags.id'),
                       primary_key=True)
    
    def __repr__(self):
        return f"PostTag {self.post_id} {self.tag_id}"

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)
    return app


