from flask import render_template, url_for, flash, redirect, request
from sentiment_analysis_package import app, db, bcrypt
from sentiment_analysis_package.forms import RegistrationForm, LoginForm, AddReview, UpdateInformation
import Classification.movie_classifier.vectorizer as vctrz
from sentiment_analysis_package.models import User, Review
from flask_login import login_user, current_user, logout_user, login_required
# TO DO:
# - create a new route (/addReview) in which the user, or anybody can add a review, and after a button is pressed you
# will be shown the probability of it being positive or negative


@app.route('/')
def index():
    reviews = Review.query.all()
    return render_template('home.html', posts=reviews)


@app.route('/home')
def home():
    reviews = Review.query.all()
    return render_template('home.html', posts=reviews)


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
        x = vctrz.vect.transform([form.content.data])
        my_classifier = vctrz.clf
        probability = str(round(vctrz.np.max(my_classifier.predict_proba(x))*10, 1))
        label = {0: 'negative', 1: 'positive'}
        if label[my_classifier.predict(x)[0]] == 'positive':
            probability = round(vctrz.np.max(my_classifier.predict_proba(x)) * 10, 1)
        else:
            probability = round(10 - vctrz.np.max(my_classifier.predict_proba(x)) * 10, 1)

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