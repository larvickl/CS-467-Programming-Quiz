from flask import render_template, request, jsonify
from programming_quiz_web_app.errors import bp
from flask_wtf.csrf import CSRFError

@bp.app_errorhandler(CSRFError)
def handle_csrf_error(error):
    return make_error(400, "Form Error", 'errors/csrf_error.html')

@bp.app_errorhandler(400)
def bad_request_error(error):
    return make_error(400, "Bad Request", "errors/400.html")

@bp.app_errorhandler(401)
def unauthorized_error(error):
    return make_error(401, "Unauthorized", "errors/401.html")

@bp.app_errorhandler(403)
def forbidden_error(error):
    return make_error(403, "Forbidden", "errors/403.html")

@bp.app_errorhandler(404)
def not_found_error(error):
    return make_error(404, "Not Found", "errors/404.html")

@bp.app_errorhandler(405)
def method_not_allowed_error(error):
    return make_error(405, "Method Not Allowed", None)

@bp.app_errorhandler(409)
def conflict_error(error):
    return make_error(409, "Conflict", None)

@bp.app_errorhandler(410)
def gone_error(error):
    return make_error(410, "Gone", None)

@bp.app_errorhandler(411)
def length_required_error(error):
    return make_error(411, "Length Required", None)

@bp.app_errorhandler(413)
def payload_too_large_error(error):
    return make_error(413, "Payload Too Large", None)

@bp.app_errorhandler(414)
def uri_too_long_error(error):
    return make_error(414, "URI Too Long", None)

@bp.app_errorhandler(415)
def unsupported_media_type_error(error):
    return make_error(415, "Unsupported Media Type", None)

@bp.app_errorhandler(429)
def too_many_requests_error(error):
    return make_error(429, "Too Many Requests", None)

@bp.app_errorhandler(431)
def request_header_fields_too_large_error(error):
    return make_error(431, "Request Header Fields Too Large", None)

@bp.app_errorhandler(500)
def internal_server_error(error):
    return make_error(400, "Internal Server Error", "errors/500.html")

def make_error(http_code, error_title, html_template=None):
    """Make an error response.

    Parameters
    ----------
    http_code : int
        The HTTP status code.
    error_title : str
        The HTTP status description.
    html_template : str, optional
        The template for the status code., by default None

    Returns
    -------
    tuple[str, int] | Response
        The response for flask to return.
    """
    # Return HTML if accepted.
    if request.accept_mimetypes.accept_html and html_template != None:
        return render_template(html_template), http_code
    # Return JSON if accepted.
    elif request.accept_mimetypes.accept_json:
        responce = jsonify({'error': error_title})
        responce.status_code = http_code
        return responce
    # Return palin text if nothing else is accepted.
    else:
        return f'{str(http_code)} -  Not Found', http_code
