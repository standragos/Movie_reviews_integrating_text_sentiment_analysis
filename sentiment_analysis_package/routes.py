from flask import render_template, url_for, flash, redirect, request, abort
from sentiment_analysis_package import app, db, bcrypt
from sentiment_analysis_package.forms import RegistrationForm, LoginForm, AddReview, UpdateInformation
import Classification.movie_classifier.vectorizer as vctrz
from sentiment_analysis_package.models import User, Review
from flask_login import login_user, current_user, logout_user, login_required
import numpy as np
# TO DO:
# - create a new route (/addReview) in which the user, or anybody can add a review, and after a button is pressed you
# will be shown the probability of it being positive or negative


# function to find out the rating of a review thru classification
def get_movie_rating(form):
    x = vctrz.vect.transform([form.content.data])
    my_classifier = vctrz.clf
    probability = str(round(vctrz.np.max(my_classifier.predict_proba(x)) * 10, 1))
    label = {0: 'negative', 1: 'positive'}
    if label[my_classifier.predict(x)[0]] == 'positive':
        probability = round(vctrz.np.max(my_classifier.predict_proba(x)) * 10, 1)
    else:
        probability = round(10 - vctrz.np.max(my_classifier.predict_proba(x)) * 10, 1)
    return probability


@app.route('/')
def index():
    reviews = Review.query.all()
    return render_template('home.html', reviews=reviews)


@app.route('/home')
def home():
    reviews = Review.query.all()
    return render_template('home.html', reviews=reviews)


@app.route("/about")
def about():
    return render_template('about.html', title='about')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        password = form.password.data
        user = User(username=form.username.data, email=form.email.data, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Account succesfully created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=form.rememberMe.data)
            next_page = request.args.get('next')

            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
        else:
            flash('Incorrect credentials.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/addReview", methods=['GET', 'POST'])
@login_required
def add_review():
    form = AddReview()
    if form.validate_on_submit():
        probability = get_movie_rating(form)
        review = Review(movie_name=form.movie_name.data, content=form.content.data, author=current_user,
                        rating=probability)
        db.session.add(review)
        db.session.commit()
        # flash('Based on other reviews, this review has a rating of:' + ' - ' + str(probability), 'success')
        return redirect(url_for('home'))
    return render_template('add_review.html', title='Add a review', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    image_file = url_for('static', filename='pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file)


@app.route("/update", methods=['GET', 'POST'])
@login_required
def update():
    form = UpdateInformation()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account was successfully updated!', 'success')
        return redirect(url_for('account'))
    image_file = url_for('static', filename='pics/' + current_user.image_file)
    return render_template('update.html', title='Update account', image_file=image_file, form=form)


@app.route("/review/<int:review_id>")
def review(review_id):
    review = Review.query.get_or_404(review_id)
    return render_template('review.html', title='review.movie_name', review=review)


@app.route("/review/<int:review_id>/update", methods=['GET', 'POST'])
def update_review(review_id):
    form = AddReview()
    review = Review.query.get_or_404(review_id)
    if review.author != current_user:
        abort(403)
    if form.validate_on_submit():
        review.movie_name = form.movie_name.data
        review.content = form.content.data
        review.rating = get_movie_rating(form)
        db.session.commit()
        flash('Your review has been updated!', 'success')
        return redirect(url_for('review', review_id=review.id))
    return render_template('update_review.html', title='Update review', review=review, form=form)


@app.route("/top_movies")
def top_movies():
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
                sum = sum + float(movie_names[j + 1])

        final_movie_list.append(val)
        final_rating_list.append(round(sum / contor, 1))

    return render_template('top_movies.html', title='Top movies', movie_names=final_movie_list,
                           ratings=final_rating_list)
