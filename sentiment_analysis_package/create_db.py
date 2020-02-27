'''
from run_app import db
from run_app import User, Post
db.create_all()
user1 = User(username='Stan', email='d@yahoo.com', password='pass')
db.session.add(user1)
user2 = User(username='Ion', email='Ion@yahoo.com', password='pass')
db.session.add(user2)
db.session.commit()

db.drop_all()

query_list = User.query.all()
print(query_list)
user = User.query.filter_by(username='Ion').first()

post_1 = Post(title='post1',content='First post content', user_id=user.id)
db.session.add(post_1)
post_2 = Post(title='post2',content='Second post content', user_id=user.id)
db.session.add(post_2)
db.session.commit()

for post in user.posts:
    print(post.author)
print(user.posts)

my_list = User.query.all()
print(my_list)
'''