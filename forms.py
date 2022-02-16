from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,IntegerField
from wtforms.validators import InputRequired, Email, ValidationError
from models import User


class RegistrationForm(FlaskForm):
    full_names = StringField("Enter your names", validators=[InputRequired()])
    email = StringField('Your Email Address', validators=[InputRequired(), Email()])
    mobile_number = IntegerField('Mobile number', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Sign Up')

    def validate_full_names(self, full_names):
        existing_username = User.query.filter_by(full_names=full_names.data).first()
        if existing_username:
            raise ValidationError("The username already exists")

    def validate_email(self, email):
        existing_email = User.query.filter_by(email=email.data).first()
        if existing_email:
            raise ValidationError("The email already exists")


class LoginForm(FlaskForm):
    email = StringField("Enter email address", validators=[InputRequired(),Email()])
    password = PasswordField("Enter password:", validators=[InputRequired()])
    submit = SubmitField("Sign In")
