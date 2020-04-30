import Classification.movie_classifier.vectorizer as vctrz


# function to find out the rating of a review thru classification
def get_movie_rating(form):
    x = vctrz.vect.transform([form.content.data])
    my_classifier = vctrz.clf
    rating = str(round(vctrz.np.max(my_classifier.predict_proba(x)) * 10, 1))
    label = {0: 'negative', 1: 'positive'}
    if label[my_classifier.predict(x)[0]] == 'positive':
        rating = round(vctrz.np.max(my_classifier.predict_proba(x)) * 10, 1)
    else:
        rating = round(10 - vctrz.np.max(my_classifier.predict_proba(x)) * 10, 1)
    return rating


# swap elements positions of a list
def swap_positions(list, pos1, pos2):
    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list


def get_top_movies(reviews):
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
                sum = sum + float(movie_names[j + 1])

        final.append(val)
        final.append(sum / contor)

    n = len(final)

    for i in range(1, n, 2):
        for j in range(i + 2, n, 2):
            if final[i] < final[j]:
                swap_positions(final, i, j)
                swap_positions(final, i - 1, j - 1)

    final_movie_names = []
    final_ratings = []
    final_ratings_rounded = []
    for i in range(0, n, 2):
        final_movie_names.append(final[i])
        final_ratings.append(final[i + 1])
        final_ratings_rounded.append(int(round(final[i + 1])))
    return final_movie_names, final_ratings, final_ratings_rounded


def get_average_rating(reviews):
    ratings = []
    x = 0
    for each_review in reviews:
        ratings.append(each_review.rating)
        x = x + 1
    average = sum(ratings) / len(ratings)
    return average, x
