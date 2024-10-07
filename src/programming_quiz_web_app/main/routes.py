from flask import render_template, send_from_directory
from programming_quiz_web_app.main import bp

@bp.route('/index')
@bp.route('/')
def index():
    """This is the endpoint for the index."""
    return render_template('main/index.html', title="Home")

@bp.route('/robots.txt')
def robots():
    """Return a robots.txt file from the application root directory."""
    return send_from_directory("static", "robots.txt")