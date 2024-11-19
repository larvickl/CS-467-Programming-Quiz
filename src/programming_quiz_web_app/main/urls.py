import uuid
import secrets
import string
from programming_quiz_web_app.models import Assignments

def generate_quiz_url_and_pin() -> tuple[str, str]:
    """Generate the unique part of a quiz URL and the URL PIN.

    The unique part of the URL is generated using UUID version 4 (see 
    RFC 4122).  The uniqueness of this string is confirmed by checking 
    the database.  It is EXTREMELY unlikely that that there will ever actually
    be a duplicate.

    Returns
    -------
    str
        The unique part of the quiz URL.
    str
        The URL PIN.
    """
    url_unique_part = uuid.uuid4().hex
    while Assignments.query.filter_by(url=url_unique_part).first() is not None:
        url_unique_part = uuid.uuid4().hex
    url_pin = ''.join(secrets.choice(string.digits) for i in range(8))
    return url_unique_part, url_pin
