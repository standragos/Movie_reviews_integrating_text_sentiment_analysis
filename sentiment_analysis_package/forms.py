from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from sentiment_analysis_package.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    @staticmethod
    def validate_username(username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That user name is already taken')

    @staticmethod
    def validate_email(email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already taken')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    rememberMe = BooleanField('remember me')
    submit = SubmitField('Log in')


class AddReview(FlaskForm):
    movie_name = StringField('Movie name', validators=[DataRequired()])
    review = StringField('review', validators=[DataRequired(), Length(min=30)])
    submit = SubmitField('submit your review')