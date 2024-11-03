from flask import request, jsonify
from programming_quiz_web_app.main import bp
from programming_quiz_web_app.models import *
from flask_jwt_extended import jwt_required, get_jwt_identity

@bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
