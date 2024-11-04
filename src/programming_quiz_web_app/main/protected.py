from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from programming_quiz_web_app.main import bp

@bp.route('/api/protected', methods=['GET'])
@jwt_required()
def protected():
    """Access protected content with valid JWT."""
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200