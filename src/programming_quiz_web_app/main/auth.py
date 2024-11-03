from programming_quiz_web_app.main import bp
from programming_quiz_web_app.models import Users
from models import Users
from programming_quiz_web_app.main.email import send_reset_email
from flask import request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from extensions import db
import datetime as dt
import pytz
import jwt 

@bp.route('/auth/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    surname = data.get('surname')
    given_name = data.get('given_name')

    # Check if user already exists
    if Users.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 400

    # Hash the password and create a new user
    hashed_password = generate_password_hash(password)
    new_user = Users(
        email=email,
        password_hash=hashed_password,
        surname=surname,
        given_name=given_name,
        account_state="active",
        account_created=dt.datetime.now(pytz.timezone('America/Indiana/Indianapolis')),
        last_login=None
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@bp.route('/auth/login', methods=['POST'])
@jwt_required
def login():
    """Authenticate user using JWT token"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Find if user is valid
    user = Users.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid email or password"}), 401

    # Use session and date-time to create timed access token
    user.last_login = dt.datetime.now(pytz.timezone('America/Indiana/Indianapolis'))
    db.session.commit()

    access_token = create_access_token(identity=user.get_id())

    user.token = access_token
    db.session.commit()

    return jsonify(access_token=access_token), 200


@bp.route('/auth/request_password_reset', methods=['POST'])
def request_password_reset():
    """Request a password reset link."""
    data = request.get_json()
    email = data.get('email')
    
    user = Users.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Generate a reset token
    token = jwt.encode({'email': email, 'exp':dt.datetime.now(pytz.timezone('America/Indiana/Indianapolis')) + dt.timedelta(hours=24)}, 
                       current_app.config['SECRET_KEY'], algorithm='HS256')
    url = "34.45.239.202" 
    reset_link = f"http://{url}/reset_password?token={token}"
    
    send_reset_email(email, reset_link)
    
    return jsonify({"message": "Password reset email sent."}), 200

@bp.route('/auth/reset_password', methods=['POST'])
def reset_password():
    """Reset the user's password using the provided token."""
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('new_password')
    
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        email = payload['email']
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 400
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 400

    user = Users.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    hashed_password = generate_password_hash(new_password)
    user.password_hash = hashed_password
    db.session.commit()

    return jsonify({"message": "Password has been reset successfully."}), 200
