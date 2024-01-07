# fastapi_contacts/app/utilities.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

class CustomSMTP_SSL(smtplib.SMTP_SSL):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

def send_email_verification(smtp: CustomSMTP_SSL, email: str, user_id: int):
    """
    Send an email verification link to the specified email address.

    Parameters:
    - `smtp` (CustomSMTP_SSL): An instantiated CustomSMTP_SSL object.
    - `email` (str): Email address to send the verification link to.
    - `user_id` (int): User ID to include in the verification link.

    Returns:
    - None
    """
    sender_email = os.getenv("EMAIL_SENDER")  # Replace with your email
    subject = "Email Verification"
    body = f"Click the link to verify your email: http://your-app-url/verify-email/{user_id}"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        smtp.connect(os.getenv("SMTP_SERVER"), os.getenv("SMTP_PORT"))  # Use your SMTP server and port
        smtp.login(sender_email, os.getenv("EMAIL_PASSWORD"))
        smtp.sendmail(sender_email, email, message.as_string())
        print("Email verification link sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")
