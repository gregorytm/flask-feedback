from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, NumberRange, Email, Optional
from wtforms import StringField, PasswordField

class AddUserForm(FlaskForm):
    username = StringField("username")
    password = PasswordField('password')
    email = StringField("email address")
    first_name = StringField(" first name")
    last_name = StringField("last name")

class LoginForm(FlaskForm):
    username = StringField("username", validators=[InputRequired(), Length(min=1, max=20)],)

    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=20)],)


class FeedbackForm(FlaskForm):

    title = StringField(
        "Title",
        validators=[InputRequired(), Length(max=100)],
    )
    content = StringField(
        "Content",
        validators=[InputRequired()]
    )