from flask import render_template, flash, redirect, url_for, request, current_app
from programming_quiz_web_app.auth import bp
from werkzeug.security import generate_password_hash, check_password_hash
from programming_quiz_web_app.auth.forms import RegistrationValidator, LoginForm, PasswordResetRequestForm, PasswordResetForm
from programming_quiz_web_app import db
from programming_quiz_web_app.models import Users
from programming_quiz_web_app.utilities import send_password_reset_email
from flask_jwt_extended import create_access_token
import jwt
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
            # Generate a new JWT token.
            token = create_access_token(identity={"id": user.id, "email": user.email})
            try:
                # Store the token in the database.
                user.token = token
                user.last_login = dt.datetime.now(dt.timezone.utc)
                db.session.commit()
            except:
                db.session.rollback()
                flash('Failed to store token. Please try again.', 'danger')
                return redirect(url_for('auth.login'))
            return redirect(url_for('employer.dashboard'))
        else:
            form.password.errors.append('Invalid email or password')

    return render_template('auth/login.html', title="Login", form=form)

@bp.route('/request_password_reset', methods=['GET', 'POST'])
def request_password_reset():
    """This is the endpoint to request a password reset link."""
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        email = form.email.data
        # Check db for pre-existing account
        user = Users.query.filter_by(email=email).first()
        if not user:
            flash('No account found.', 'danger')
            return redirect(url_for('auth.request_password_reset'))
        # Generate a reset token
        token = jwt.encode({'email': email, 'exp': dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=24)}, 
                           current_app.config['SECRET_KEY'], algorithm='HS256')
        reset_link = url_for('auth.reset_password', token=token, _external=True)
        try:
            send_password_reset_email(email, reset_link)
            flash('Reset link sent! Please check your email.', 'success')
        except Exception as e:
            current_app.logger.error(f"Error sending password reset email: {e}")
            flash('Failed to send reset email. Please try again.', 'danger')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/request_password_reset.html', title="Request Password Reset", form=form)

@bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    """This is the endpoint to reset user's password."""
    token = request.args.get('token')
    if not token:
        flash('Invalid reset token.', 'danger')
        return redirect(url_for('auth.request_password_reset'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        new_password = form.password.data
        try:
            # Decode JWT and check validity
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            email = payload['email']
        except jwt.ExpiredSignatureError:
            flash('Reset token has expired.', 'danger')
            return redirect(url_for('auth.request_password_reset'))
        except jwt.InvalidTokenError:
            flash('Invalid reset token.', 'danger')
            return redirect(url_for('auth.request_password_reset'))
        user = Users.query.filter_by(email=email).first()
        if not user:
            flash('User not found.', 'danger')
            return redirect(url_for('auth.request_password_reset'))
        # Create new password hash and commit to db
        hashed_password = generate_password_hash(new_password)
        user.password_hash = hashed_password
        db.session.commit()
        flash('Password successfully changed! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', title="Reset Password", form=form)

