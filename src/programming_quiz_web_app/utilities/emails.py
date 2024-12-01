import datetime as dt
from flask import render_template, current_app, url_for
from smtplib import SMTP, SMTP_SSL
from email.message import EmailMessage
from email.headerregistry import Address
from programming_quiz_web_app.models import Assignments

def send_email(
        email_to: Address | tuple[Address], 
        email_cc: Address | tuple[Address] | None,
        email_bcc: Address | tuple[Address] | None,
        subject: str, 
        ascii_email: str, 
        html_email: str | None) -> None:
    """Send an email via SMTP.

    Parameters
    ----------
    email_to : Address | tuple[Address]
        The address(es) to send the email to.
    email_cc : Address | tuple[Address] | None
        The address(es) to CC the email to.  If None, 
        the email is not CC'd to anyone.
    email_bcc : Address | tuple[Address] | None
        The address(es) to BCC the email to.  If None, 
        the email is not BCC'd to anyone.
    subject : str
        The subject of the email.
    ascii_email : str
        The ASCII text version of the email.
    html_email : str | None
        The HTML version of the email.  If None, a strictly ASCII
        email will be sent.
    """
    # Prepare email header.
    message = EmailMessage()
    message["Subject"] = subject
    message['From'] = current_app.config["SMTP_FROM"]
    message['To'] = email_to
    if email_cc is not None:
        message['Cc'] = email_cc
    if email_bcc is not None:
        message["Bcc"] = email_bcc
    # Add ASCII version of email.
    message.set_content(ascii_email)
    # Add HTML version of email if provided.
    if html_email is not None:
        message.add_alternative(html_email, subtype='html')
    # Send email with authentication.
    if current_app.config["SMTP_SSL"] is True:
        with SMTP_SSL(current_app.config["SMTP_SERVER"], current_app.config["SMTP_PORT"]) as server:
            server.login(current_app.config["SMTP_USERNAME"], current_app.config["SMTP_PASSWORD"])
            server.send_message(message)
    else:  # Send mail without authentication.
        with SMTP(current_app.config["SMTP_SERVER"], current_app.config["SMTP_PORT"]) as server:
            server.send_message(message)

def send_password_reset_email(email_to: Address | tuple[Address], password_reset_url: str) -> None:
    """Send a password reset email.

    Parameters
    ----------
    email_to : Address | tuple[Address]
        The address(es) to send the email to.
    password_reset_url : str
        The password reset URL.
    """
    # Email Subject.
    subject = "Reset Password - Software Programming Quiz"
    # Generate ASCII email body.
    ascii_email = render_template(
        "emails/password_reset.txt", 
        password_reset_url = password_reset_url, 
        contact_email = current_app.config["CONTACT_EMAIL_ADDRESS"])
    # Generate HTML email body.
    html_email = render_template(
        "emails/password_reset.html", 
        password_reset_url = password_reset_url, 
        contact_email = current_app.config["CONTACT_EMAIL_ADDRESS"])
    send_email(email_to, None, None, subject, ascii_email, html_email)
    
def send_quiz_assigned_email(
        email_to: Address | tuple[Address], 
        assignment: Assignments,
        email_cc: Address | tuple[Address] | None = None,
        email_bcc: Address | tuple[Address] | None = None) -> None:
    """Send a quiz assignment email.

    Parameters
    ----------
    email_to : Address | tuple[Address]
        The address(es) to send the email to.
    assignment : Assignments
        The assignment that was assigned.
    email_cc : Address | tuple[Address] | None, optional
        The address(es) to CC the email to.  If None, 
        the email is not CC'd to anyone, by default None
    email_bcc : Address | tuple[Address] | None, optional
        The address(es) to BCC the email to.  If None, 
        the email is not BCC'd to anyone, by default None
    """
    # Email subject
    subject = "Quiz Assigned - Software Programming Quiz"
    # Quiz Assigned by.
    assigned_by = assignment.assigned_by
    # Format due date.
    due_datetime_string = assignment.expiry.astimezone(dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC+00:00")
    # Format time limit.
    days, remainder = divmod(assignment.time_limit_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    if days != 0:
        time_limit_string = f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
    elif hours != 0:
        time_limit_string = f"{hours} hours, {minutes} minutes, {seconds} seconds"
    elif minutes != 0:
        time_limit_string = f"{minutes} minutes, {seconds} seconds"
    else:
        time_limit_string = f"{seconds} seconds"
    # Make URL:
    quiz_url = f'{url_for("main.start_quiz", url_id=assignment.url , _external=True)}'
    # Generate ASCII email body.
    ascii_email = render_template(
        "emails/quiz_assigned.txt",
        quiz_name = assignment.quiz.name,
        due_datetime_string = due_datetime_string,
        allowed_time = time_limit_string,
        quiz_pin = assignment.url_pin,
        assigned_by_name = f"{assigned_by.given_name} {assigned_by.surname}",
        assigned_by_email = assigned_by.email,
        quiz_url = quiz_url,
        contact_email = current_app.config["CONTACT_EMAIL_ADDRESS"])
    # Generate HTML email body.
    html_email = render_template(
        "emails/quiz_assigned.html",
        quiz_name = assignment.quiz.name,
        due_datetime_string = due_datetime_string,
        allowed_time = time_limit_string,
        quiz_pin = assignment.url_pin,
        assigned_by_name = f"{assigned_by.given_name} {assigned_by.surname}",
        assigned_by_email = assigned_by.email,
        quiz_url = quiz_url,
        contact_email = current_app.config["CONTACT_EMAIL_ADDRESS"])
    # Send Email.
    send_email(email_to, email_cc, email_bcc, subject, ascii_email, html_email)

def send_quiz_submitted_email(
        email_to: Address | tuple[Address], 
        assignment: Assignments,
        email_cc: Address | tuple[Address] | None = None,
        email_bcc: Address | tuple[Address] | None = None) -> None:
    """Send an email upon quiz submission.

    Parameters
    ----------
    email_to : Address | tuple[Address]
        The address(es) to send the email to.
    assignment : Assignments
        The assignment that was submitted.
    email_cc : Address | tuple[Address] | None, optional
        The address(es) to CC the email to.  If None, 
        the email is not CC'd to anyone, by default None
    email_bcc : Address | tuple[Address] | None, optional
        The address(es) to BCC the email to.  If None, 
        the email is not BCC'd to anyone, by default None
    """
    # Email subject.
    subject = "Quiz Submitted - Software Programming Quiz"
    # Quiz Assigned by.
    assigned_by = assignment.assigned_by
    # Format due date.
    due_datetime_string = assignment.expiry.astimezone(dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC+00:00")
    # Format Submitted datetime.
    submitted_time_string = assignment.submit_time.astimezone(dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC+00:00")
    ascii_email = render_template(
        "emails/quiz_submitted.txt",
        quiz_name = assignment.quiz.name,
        due_datetime_string = due_datetime_string,
        submitted_time = submitted_time_string,
        assigned_by_name = f"{assigned_by.given_name} {assigned_by.surname}",
        assigned_by_email = assigned_by.email,
        contact_email = current_app.config["CONTACT_EMAIL_ADDRESS"])
    html_email = render_template(
        "emails/quiz_submitted.html",
        quiz_name = assignment.quiz.name,
        due_datetime_string = due_datetime_string,
        submitted_time = submitted_time_string,
        assigned_by_name = f"{assigned_by.given_name} {assigned_by.surname}",
        assigned_by_email = assigned_by.email,
        contact_email = current_app.config["CONTACT_EMAIL_ADDRESS"])
    # Send Email.
    send_email(email_to, email_cc, email_bcc, subject, ascii_email, html_email)
