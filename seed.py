"""Seed file to make sample data for db."""

from models import User, Post, Tag, PostTag, db
from app import app

db.drop_all()
db.create_all()

User.query.delete()
Post.query.delete()

u1 = User(first_name='Dash', last_name='Hund', img_url='https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/Short-haired-Dachshund.jpg/440px-Short-haired-Dachshund.jpg')
u2 = User(first_name='Max', last_name='Schnauzer', img_url='https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Zwergschnauzer_im_Lauf.jpg/440px-Zwergschnauzer_im_Lauf.jpg')
u3 = User(first_name='Murphy', last_name='Terrier', img_url='https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Ernest_Gustave_Girardot04.jpg/440px-Ernest_Gustave_Girardot04.jpg')
u4 = User(first_name='Princess', last_name='Poodle', img_url='https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Full_attention_%288067543690%29.jpg/1920px-Full_attention_%288067543690%29.jpg')

db.session.add_all([u1, u2, u3, u4])
db.session.commit()


p1 = Post(title='Play Fetch', content="I love to play fetch because sometimes when I bring the ball back I get a treat!", user=User.query.get(1))
p2 = Post(title='Wet Vs Dry Food', content="I'm a strong believer that wet dog food is much better than dry dog food. Does anyone else here agree?", user=User.query.get(2))
p3 = Post(title='Baths', content="One thing I really hate is when my owners give me a bath. I got all this nice mud on me on purpose! So rude!", user=User.query.get(3))
p4 = Post(title='Walks', content="I love going on walks! My favorite places to walk are parks, beaches, and hiking trails! But of course, the classic neighborhood 'around-the-block' walks work in a pinch as well!", user=User.query.get(4))
p5 = Post(title='Squirrel Patrol', content="Great news, everybody! I recently just got promoted from Squirrel Officer to Squirrel Detective! My passion is keeping the neighborhood free from squirrel crimes! If you or anyone you know has any knowledge of fugitive squirrel whereabout, please let me know! It's my honor to serve!", user=User.query.get(1))
p6 = Post(title="Woof! The Struggle of Trying to Catch My Tail - A Dog's Tale", content="Hey there, fellow canines! Today, I want to talk about a daily struggle that we all face: catching our own tails. It's like a never-ending chase game! Just when you think you've got it, it slips away. Is it a conspiracy? Are our tails secretly taunting us? Let's discuss the hilarious and sometimes frustrating pursuit of our elusive tails. Stay tuned, and remember, wag more, bark less!", user=User.query.get(2))
p7 = Post(title="The Great Sock Heist: A Tale of Canine Mischief", content="Today, I embarked on a daring mission to conquer the forbidden treasures of the laundry room - socks! Armed with stealth and a wagging tail, I snuck past my humans and raided the sock drawer. The thrill of chewing on those soft, stretchy goodies was unmatched. Alas, my victory was short-lived when I got caught red-pawed. The chase that followed was worth every stolen sock!", user=User.query.get(3))
p8 = Post(title="Park Politics: The Art of Making Fur-riends", content="Ah, the dog park, a social battlefield where furry alliances are forged and territory is marked. I've perfected the art of tail-wagging diplomacy to win over fellow canines and secure my spot in the pack. From playful sprints to tail-sniffing diplomacy, I navigate the intricate politics of park life with finesse. It's a dog-eat-dog world out there, but with a wag and a smile, we can all find our place.", user=User.query.get(4))
p9 = Post(title="The Bath Chronicles: Tales from the Soapy Abyss", content="Today, I faced the dreaded enemy - the bath. As my humans lured me into the watery abyss, I clung to the edge of the tub for dear life. The soapy onslaught began, but I put up a valiant fight, leaving a trail of wet paw prints across the bathroom. They may have won the battle, but mark my words, the war against baths will continue!", user=User.query.get(1))
p10 = Post(title="The Case of the Vanishing Treats: A Paw-some Mystery Unleashed", content="It was a dark and delicious night when treats started disappearing mysteriously from the kitchen counter. Armed with my sniffing superpower, I embarked on a mission to uncover the truth. Following the crumb trail, I discovered a secret stash under the couch, hidden by none other than my sneaky feline housemate. Case closed, treats reclaimed, and a furry detective was born!", user=User.query.get(2))
p11 = Post(title="The Art of Canine Yoga: Zen and the Wagging Tail", content="In pursuit of inner peace and the perfect stretch, I've embraced the ancient art of doggy yoga. From the Downward-Facing Dog to the Paws-up Pose, I contort my body into shapes that make my humans' jaws drop. They may think I'm a master yogi, but little do they know that my ultimate goal is to snatch their snacks while they're busy chanting 'om'.", user=User.query.get(3))
p12 = Post(title="The Great Squirrel Chase: A Quest for Nutty Triumph", content="Oh, those bushy-tailed daredevils! Today, I embarked on a grand adventure to chase squirrels. With boundless energy and a tail full of determination, I sprinted through the yard, leaping over obstacles and barking with wild abandon. Alas, those agile acorn hoarders always manage to escape my clutches. Until next time, my furry foes!", user=User.query.get(4))
p13 = Post(title="The Toy Graveyard: Where Squeakers Go to Rest", content="Behind the couch lies a secret world, a graveyard for once-beloved toys. There, abandoned squeakers and tattered plushies gather, waiting for their furry friends to give them another chance at play. As I dig through the toy graveyard, memories of epic battles and playful romps flood my mind. Though their squeaks may have faded, their spirit lives on in my wagging tail.", user=User.query.get(1))
p14 = Post(title="Paw-ty Crashers: Tales of Epic Tail-Wagging Shenanigans", content="When my humans host a party, it's my time to shine as the ultimate paw-ty crasher. I weave through guests' legs, searching for dropped snacks and stolen pats. With a wag of my tail and a wet nose, I bring joy and chaos to the gathering. After all, who needs party games when you have a four-legged entertainer stealing the show?", user=User.query.get(2))

db.session.add_all([p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14])
db.session.commit()

t1 = Tag(name='walks')
t2 = Tag(name='squirrels')
t3 = Tag(name='mystery')
t4 = Tag(name='baths')
t5 = Tag(name='funny')
t6 = Tag(name='educational')
t7 = Tag(name='interesting')
t8 = Tag(name='entertaining')
t9 = Tag(name='fetch')
t10 = Tag(name='food/treats')

db.session.add_all([t1, t2, t3, t4, t5, t6, t7, t8, t9, t10])
db.session.commit()

pt1 = PostTag(post_id=1, tag_id=9)
pt2 = PostTag(post_id=1, tag_id=10)
pt3 = PostTag(post_id=2, tag_id=10)
pt4 = PostTag(post_id=3, tag_id=4)
pt5 = PostTag(post_id=4, tag_id=1)
pt6 = PostTag(post_id=5, tag_id=2)
pt7 = PostTag(post_id=6, tag_id=9)
pt8 = PostTag(post_id=6, tag_id=5)
pt9 = PostTag(post_id=6, tag_id=3)
pt10 = PostTag(post_id=7, tag_id=3)
pt11 = PostTag(post_id=7, tag_id=5)
pt12 = PostTag(post_id=7, tag_id=8)
pt13 = PostTag(post_id=8, tag_id=5)
pt14 = PostTag(post_id=8, tag_id=7)
pt15 = PostTag(post_id=8, tag_id=1)
pt16 = PostTag(post_id=9, tag_id=4)
pt17 = PostTag(post_id=10, tag_id=3)
pt18 = PostTag(post_id=10, tag_id=10)
pt19 = PostTag(post_id=10, tag_id=7)
pt20 = PostTag(post_id=11, tag_id=5)
pt21 = PostTag(post_id=11, tag_id=10)
pt22 = PostTag(post_id=12, tag_id=2)
pt23 = PostTag(post_id=12, tag_id=8)
pt24 = PostTag(post_id=13, tag_id=3)
pt25 = PostTag(post_id=13, tag_id=9)
pt26 = PostTag(post_id=14, tag_id=8)
pt27 = PostTag(post_id=14, tag_id=5)
pt28 = PostTag(post_id=14, tag_id=10)

db.session.add_all([pt1, pt2, pt3, pt4, pt5, pt6, pt7, pt8, pt9, pt10, pt11, pt12, pt13, pt14, pt15, pt16, pt17, pt18, pt19, pt20, pt21, pt22, pt23, pt24, pt25, pt26, pt27, pt28])
db.session.commit()

