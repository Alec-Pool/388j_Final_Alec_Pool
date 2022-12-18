from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, PasswordField, SelectField
from wtforms.fields.html5 import IntegerRangeField

from wtforms.validators import (
    InputRequired,
    DataRequired,
    NumberRange,
    Length,
    Email,
    EqualTo,
    ValidationError,
)


from .models import User


class NameSearchForm(FlaskForm):
    search_query = StringField(
        "Restaurant name and other info", validators=[InputRequired(), Length(min=1, max=100)]
    )

    location =  StringField(
        "Location", validators=[InputRequired(), Length(min=1, max=100)]
    )

    submit = SubmitField("Search")


class AttributeSearchForm(FlaskForm):
    romance = SelectField(u'How Romantic?', choices= ["Causal", "Semi-Romantic", "Romantic", "Very Romantic"])

    occasion = SelectField(u'What was the Occasion?', choices= ["Causal Night Out", "Nice Night Out", "Romantic Celebration", "Other"])

    price = IntegerRangeField('How Expensive?', [NumberRange(min=1, max=4)])

    submit = SubmitField("Search")





class RestaurantReviewForm(FlaskForm):
    text = TextAreaField(
        "General Comments", validators=[InputRequired(), Length(min=5, max=500)]
    )

    romance = SelectField(u'How Romantic?', choices= ["Causal", "Semi-Romantic", "Romantic", "Very Romantic"])

    occasion = SelectField(u'What was the Occasion?', choices= ["Causal Night Out", "Nice Night Out", "Romantic Celebration", "Other"])
    

    price = IntegerRangeField('How Expensive?', [NumberRange(min=1, max=4)])


    recommend = IntegerRangeField('How Likely to Recommend?', [NumberRange(min=0, max=100)])


    submit = SubmitField("Enter Review")


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=40)])
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is taken")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")


class UpdateUsernameForm(FlaskForm):
    username = StringField(
        "New Username:", validators=[InputRequired(), Length(min=1, max=40)]
    )
    submit = SubmitField("Update Username")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.objects(username=username.data).first()
            if user is not None:
                raise ValidationError("That username is already taken")


class UpdateEmailForm(FlaskForm):
    email = StringField(
        "New Email:", validators=[InputRequired(), Email()]
    )
    submit = SubmitField("Update Email")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.objects(email=email.data).first()
            if user is not None:
                raise ValidationError("Email is taken")