from flask import render_template, url_for, flash, redirect
from sentiment_analysis_package import app
from sentiment_analysis_package.forms import RegistrationForm, LoginForm
import Classification.movie_classifier.vectorizer as vctrz
from sentiment_analysis_package.models import User, Post


example = ['this movie is so bad, i wont watch it ever again']
X = vctrz.vect.transform(example)
classifier = vctrz.clf

string_example = ''.join(example)

tuple = {0: 'negativ', 1: 'positiv'}
posts = [
    {
        'author': 'exemplul este urmatorul: ' + string_example,
        'title': 'pozitiv sau negativ: ' + str(tuple[classifier.predict(X)[0]]),
        'content':'probabilitatea ca el sa fie pozitiv sau negativ este de: ' +
                  str(round(vctrz.np.max(classifier.predict_proba(X))*100, 2)),
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