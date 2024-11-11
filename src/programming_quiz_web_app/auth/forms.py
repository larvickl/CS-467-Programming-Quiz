from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from programming_quiz_web_app.models import Users
import datetime as dt

class RegistrationValidator(FlaskForm):
    """Validate the registration form submission.
    
    Attributes
    ----------
    email : StringField
        User's email with validation rules
    given_name : StringField
        User's given name with validation rules
    surname : StringField
        User's surname with validation rules
    password : PasswordField
        User's password with validation rules
    confirm_password : PasswordField
        Password confirmation field
    """
    email = StringField('Email', validators=[
        DataRequired(),
        Email(),
        Length(max=300, message='Email must be less than 300 characters')
    ])
    given_name = StringField('First Name', validators=[
        DataRequired(),
        Length(max=100, message='First Name must be less than 100 characters')
    ])
    surname = StringField('Last Name', validators=[
        DataRequired(),
        Length(max=100, message='Last Name must be less than 100 characters')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Register')

    def validate_email(self, email):
        """Check if the email is already registered in the database.
    
        Parameters
        ----------
        email : StringField
            The email field to validate
        
        Raises
        ------
        ValidationError
            If the email is already registered
        """
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email address already registered.')

class LoginForm(FlaskForm):
    """Validate the login form submission.
    
    Attributes
    ----------
    email : StringField
        User's email with validation rules
    password : PasswordField
        User's password with validation rules
    submit : SubmitField
        Form submission button
    """

    email = StringField('Email', validators=[
        DataRequired(message="Email is required"),
        Email(message="Please enter a valid email address")
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required")
    ])
    
    submit = SubmitField('Log In')
    