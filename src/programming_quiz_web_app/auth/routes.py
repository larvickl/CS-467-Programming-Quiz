from flask import render_template, flash, redirect, url_for, request, current_app
from programming_quiz_web_app.auth import bp
from werkzeug.security import generate_password_hash, check_password_hash
from programming_quiz_web_app.auth.forms import RegistrationValidator, LoginForm
from programming_quiz_web_app import db
from programming_quiz_web_app.models import Users
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
            return redirect(url_for('main.index'))
        else:
            form.password.errors.append('Invalid email or password')

    return render_template('auth/login.html', title="Login", form=form)

@bp.route('/request_password_reset', methods=['POST'])
def request_password_reset():
    """Request a password reset link."""
    data = request.get_json()
    email = data.get('email')
    
    # Check db for pre-existing email/account
    user = Users.query.filter_by(email=email).first()
    if not user:
        flash('Reset request failed. Please try again.', 'danger')
        return(redirect(url_for('auth.login')))

    # Generate a reset token
    token = jwt.encode({'email': email, 'exp':dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=24)}, 
                       current_app.config['SECRET_KEY'], algorithm='HS256')
    reset_link = url_for('auth.reset_password', token=token, _external=True)
    
    send_reset_email(email, reset_link)
    flash('Reset link sent! Please check your email.', 'success')
    return(redirect(url_for('auth.login')))

@bp.route('/reset_password', methods=['POST'])
def reset_password():
    """Reset the user's password using the JWT token."""
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('new_password')
    
    try:
        # Decode the JWT and check validity
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        email = payload['email']
    except jwt.ExpiredSignatureError:
        flash('Reset request expired. Please try again.', 'danger')
        return(redirect(url_for('auth.login')))
    except jwt.InvalidTokenError:
        flash('Reset request invalid. Please try again.', 'danger')
        return(redirect(url_for('auth.login')))

    user = Users.query.filter_by(email=email).first()
    if not user:
        flash('User not found. Please try again.', 'danger')
        return(redirect(url_for('auth.login')))

    # Create new password hash and store
    hashed_password = generate_password_hash(new_password)
    user.password_hash = hashed_password
    db.session.commit()

    flash('Password Changed!  Please login again.', 'success')
    return(redirect(url_for('auth.login')))
