from flask import Blueprint

bp = Blueprint(
    'vite',
    __name__,
    static_folder="vite-flask-integration/assets_compiled/bundled",
    static_url_path="/assets/bundled")

from programming_quiz_web_app.vite import assets