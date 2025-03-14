from bleach import clean
from flask_mail import Mail, Message
import os
from flask import request

# mail = None
# previous_contacts = []
#
#
# def setup_email_config(app):
#     """Sets up Flask-Mail"""
#     global mail
#
#     app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
#     app.config['MAIL_PORT'] = 587
#     app.config['MAIL_USE_TLS'] = True
#     app.config['MAIL_USE_SSL'] = False
#     app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
#     app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
#     app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_USERNAME")
#
#     mail = Mail(app)
#
#
#
#
# def clean_email_components(name_input, email_input, message_input):
#     """Uses bleach to sanitise message components"""
#     return clean(name_input), clean(email_input), clean(message_input)
#
#
# def check_valid_contact(email):
#     """checks if a valid message - if email not been sent too many times before then valid - else False"""
#     if email in previous_contacts:
#         occurrences = previous_contacts.count(email)
#         if occurrences > 5:
#             return False
#     return True
#
#
# def send_email(name, email, message):
#     """
#     Sends message from website to my email.
#     Cleans message contents and stops frequent + repeated messages from same sender.
#     """
#
#     if mail:
#         # clean the message components
#         name, email, message = clean_email_components(name, email, message)
#
#         # check valid contact (not too many previous emails from sender)
#         email_valid = check_valid_contact(email)
#
#         if email_valid:
#
#             try:  # send email
#                 msg = Message(
#                     f'Portfolio Contact - {name}, {email}',
#                     recipients=[os.getenv("MAIL_USERNAME")],
#                     body=f"Message from: {name},\nEmail Address: {email}\n\nContents:\n{message}"
#                 )
#                 mail.send(msg)
#
#                 # add email to previous email sent list
#                 previous_contacts.append(email)
#                 # remove last added email if more than 10 added
#                 if len(previous_contacts) >= 10:
#                     previous_contacts.pop()
#
#                 return "Thankyou for message! I will respond shortly"
#
#             except:  # error sending email
#                 return "Could not send email. Please try again shortly."
#
#     return False
#


mail = None
previous_contacts = {}  # Dictionary to track email + IP attempts


def setup_email_config(app):
    """Sets up Flask-Mail configuration."""
    global mail

    app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
    app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_USERNAME")

    mail = Mail(app)


def get_client_ip():
    """Retrieves client IP address (supports proxies)."""
    return request.headers.get('X-Forwarded-For', request.remote_addr)


def normalize_email(email):
    """Normalizes email: converts to lowercase, removes dots for Gmail addresses."""
    email = email.strip().lower()
    if '@gmail.com' in email:
        email = email.replace('.', '')
    return email


def clean_email_components(name_input, email_input, message_input):
    """Uses bleach to sanitize message components."""
    return clean(name_input), clean(email_input), clean(message_input)


def check_valid_contact(email):
    """Limits messages to 5 per (email, IP) to prevent spam."""

    # Normalize email & get IP
    email = normalize_email(email)
    ip = get_client_ip()

    # Create a (email, IP) key to track attempts
    contact_key = (email, ip)
    previous_contacts[contact_key] = previous_contacts.get(contact_key, 0) + 1

    # Allow max 5 messages per (email, IP)
    if previous_contacts[contact_key] > 5:
        return False

    return True


def send_email(name, email, message):
    """
    Sends message from website to my email.
    Cleans message contents and stops frequent + repeated messages from same sender.
    """

    if mail:
        # Clean the message components
        name, email, message = clean_email_components(name, email, message)

        # Check if the sender is valid (not spamming)
        email_valid = check_valid_contact(email)

        if email_valid:
            try:  # Send email
                msg = Message(
                    f'Portfolio Contact - {name}, {email}',
                    recipients=[os.getenv("MAIL_USERNAME")],
                    body=f"Message from: {name},\nEmail Address: {email}\n\nContents:\n{message}"
                )
                mail.send(msg)

                return "Thank you for your message! I will respond shortly."

            except:  # Error sending email
                return "Could not send email. Please try again shortly."

    return "Message limit exceeded or email error. Please try later."
