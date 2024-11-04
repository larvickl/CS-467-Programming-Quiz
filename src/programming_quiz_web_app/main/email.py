from programming_quiz_web_app.main import mail
from flask_mail import Message

def send_reset_email(to, link):
    # once email/DNS is obtained, replace placeholder here
    msg = Message("Password Reset Request", sender="email@placeholder.com", recipients=[to])
    msg.body = f"To reset your password, click the following link: {link}"
    mail.send(msg)
    