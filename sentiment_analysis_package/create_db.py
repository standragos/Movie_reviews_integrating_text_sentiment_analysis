from sentiment_analysis_package.models import Review
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

reviews = Review.query.all()
movie_names = []
movie_name_set = set()
final_movie_list = []
final_rating_list = []
for each_review in reviews:
    movie_names.append(each_review.movie_name)
    movie_names.append(each_review.rating)
    movie_name_set.add(each_review.movie_name)

for i, val in enumerate(movie_name_set):
    sum = 0
    contor = 0
    for j, name in enumerate(movie_names):
        if val == name:
            contor = contor + 1
            sum = sum + float(movie_names[j+1])

    final_movie_list.append(val)
    final_rating_list.append(sum / contor)

print(final_movie_list)
print(final_rating_list)