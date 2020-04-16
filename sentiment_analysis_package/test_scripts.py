
from sentiment_analysis_package.models import Review
# from run_app import db
from sentiment_analysis_package.models import User, Review
'''
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

import Classification.movie_classifier.vectorizer as vctrz
import numpy as np

def get_movie_rating():
    x = vctrz.vect.transform(["Very long, boring, I give 1 star to make balance because everyon"
                              "e rates it 10 for nothing."])
    my_classifier = vctrz.clf
    prob = vctrz.np.max(my_classifier.predict_proba(x))
    label = {0: 'negative', 1: 'positive'}
    print('Prediction: %s\nProbability: %.2f%%' % (label[my_classifier.predict(x)[0]], np.max(my_classifier.predict_proba(x))*100))


get_movie_rating()


for post in user.posts:
    print(post.author)
print(user.posts)

my_list = User.query.all()
print(my_list)



# Swap function

def swap_positions(list, pos1, pos2):
    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list

reviews = Review.query.all()
movie_names = []
movie_name_set = set()
final = []
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

    final.append(val)
    final.append(sum / contor)

n = len(final)

for i in range(1, n, 2):
    for j in range(i+2, n, 2):
        if final[i] < final[j]:
            swap_positions(final, i, j)
            swap_positions(final, i-1, j-1)

final_movie_names = []
final_ratings = []
for i in range(0, n, 2):
    final_movie_names.append(final[i])
    final_ratings.append(final[i+1])


print(final)
print(final_movie_names)
print(final_ratings)
'''

from sentiment_analysis_package.models import User, Review, Movie

movies = Movie.query.all()
print(movies)