"""Seed file to make sample data for db."""

from models import User, Post, db
from app import app

db.drop_all()
db.create_all()

User.query.delete()
Post.query.delete()

u1 = User(first_name='Dachs', last_name='Hund', img_url='https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/Short-haired-Dachshund.jpg/440px-Short-haired-Dachshund.jpg')
u2 = User(first_name='Schnau', last_name='Zer', img_url='https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Zwergschnauzer_im_Lauf.jpg/440px-Zwergschnauzer_im_Lauf.jpg')
u3 = User(first_name='Yorkshire', last_name='Terrier', img_url='https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Ernest_Gustave_Girardot04.jpg/440px-Ernest_Gustave_Girardot04.jpg')

db.session.add_all([u1, u2, u3])
db.session.commit()

p1 = Post(title='Hello', content="I'm a cute dog", user=User.query.get(1))
p2 = Post(title='Hey', content="I'm an even cuter dog", user=User.query.get(2))
p3 = Post(title='Not True', content="I'm the cutest dog of them all", user=User.query.get(3))
p4 = Post(title='Play Fetch', content="I love to play fetch because sometimes when I bring the ball back I get a treat", user=User.query.get(2))
p5 = Post(title='Wet Vs Dry Food', content="I'm a strong believer that wet dog food is much better than dry dog food. Does anyone else here agree?", user=User.query.get(2))
p6 = Post(title='Baths', content="One thing I really hate is when my owners give me a bath. I got all this nice mud on me on purpose! So rude!", user=User.query.get(3))

db.session.add_all([p1, p2, p3, p4, p5, p6])
db.session.commit()
