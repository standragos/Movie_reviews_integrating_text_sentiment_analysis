from flask import render_template, url_for, flash, redirect, request
from sentiment_analysis_package import app, db, bcrypt
from sentiment_analysis_package.forms import RegistrationForm, LoginForm, AddReview
import Classification.movie_classifier.vectorizer as vctrz
from sentiment_analysis_package.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
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


@app.route('/')
def index():
    return render_template('home.html', posts=posts)


@app.route('/home')
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='about')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pass)
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
        if user and bcrypt.check_password_hash(user.password, form.password.data):
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
        my_review = form.review.data
        my_review = [my_review]
        x = vctrz.vect.transform(my_review)
        my_classifier = vctrz.clf
        probability = str(round(vctrz.np.max(my_classifier.predict_proba(x))*10, 1))
        label = {0: 'negative', 1: 'positive'}
        if label[my_classifier.predict(x)[0]] == 'positive':
            probability = round(vctrz.np.max(my_classifier.predict_proba(x)) * 10, 1)
        else:
            probability = round(10 - vctrz.np.max(my_classifier.predict_proba(x)) * 10, 1)

        flash('Based on other reviews, this review has a rating of:' +
              ' - ' + str(probability), 'succes')
        return redirect(url_for('home'))

    return render_template('addReview.html', title='Add a review', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')
