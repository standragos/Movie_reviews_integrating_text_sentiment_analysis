from flask import render_template, url_for, flash, redirect
from sentiment_analysis_package import app
from sentiment_analysis_package.forms import RegistrationForm, LoginForm, AddReview
import Classification.movie_classifier.vectorizer as vctrz
from sentiment_analysis_package.models import User, Post
# TO DO:
# - create a new route (/addReview) in which the user, or anybody can add a review, and after a button is pressed you
# will be shown the probability of it being positive or negative




tuple = {0: 'negativ', 1: 'positiv'}
posts = [
    {
        'author': 'exemplul este urmatorul: ',
        'title': 'pozitiv sau negativ: ' ,
        'content':'probabilitatea ca el sa fie pozitiv sau negativ este de:' ,
        'date_posted': '12 februarie'
    },

    {
        'author':'Vasile',
        'title': 'a doua postare',
        'content':'content 2',
        'date_posted':'13februarie'
    }
]
title = "Movie Reviews"


@app.route('/home')
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='about')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data} !', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@da.com' and form.password.data == '1234':
            flash('Succesfully logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Incorrect credentials .', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/addReview", methods=['GET', 'POST'])
def add_review():
    form = AddReview()
    if form.validate_on_submit():
        my_review = form.review.data
        my_review = [my_review]
        x = vctrz.vect.transform(my_review)
        classifier = vctrz.clf
        probability = str(round(vctrz.np.max(classifier.predict_proba(x))*100, 2))
        label = {0: 'negative', 1: 'positive'}
        flash('The review for the movie: ' + ' has a probability of being: ' + label[classifier.predict(x)[0]] +
              probability, 'succes')
        return redirect(url_for('home'))

    return render_template('addReview.html', title='Add a review', form=form)
