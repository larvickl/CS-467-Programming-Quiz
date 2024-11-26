from flask import render_template, flash, redirect, url_for, request
from programming_quiz_web_app.auth import bp
from werkzeug.security import generate_password_hash, check_password_hash
from programming_quiz_web_app.auth.forms import RegistrationValidator, LoginForm
from programming_quiz_web_app import db
from programming_quiz_web_app.models import Users
import datetime as dt

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """This is the endpoint for the registration page."""
    form = RegistrationValidator()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = Users(
                email=form.email.data,
                password_hash=generate_password_hash(form.password.data),
                given_name=form.given_name.data,
                surname=form.surname.data,
                account_state='active',
                account_created=dt.datetime.now(dt.timezone.utc)
            )
            
            try:
                db.session.add(user)
                db.session.commit()
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('auth.login'))
            except Exception as e:
                db.session.rollback()
                flash('Registration failed. Please try again.', 'danger')
                print(f"Registration error: {str(e)}")
    return render_template('auth/registration.html', title="Register", form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """This is the endpoint for the login page."""
    
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            return redirect(url_for('employer.dashboard'))
        else:
            form.password.errors.append('Invalid email or password')

    return render_template('auth/login.html', title="Login", form=form)