# utilities.py

# fastapi_contacts/app/utilities.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

def send_email_verification(email: str, user_id: int):
    sender_email = os.getenv("EMAIL_SENDER")  # Replace with your email
    sender_password = os.getenv("EMAIL_PASSWORD")  # Replace with your email password
    smtp_server = os.getenv("SMTP_SERVER")  # Replace with your SMTP server
    smtp_port = os.getenv("SMTP_PORT")  # Replace with your SMTP port

    subject = "Email Verification"
    body = f"Click the link to verify your email: http://your-app-url/verify-email/{user_id}"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, message.as_string())
        print("Email verification link sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

# Add your email server details to the .env file
# EMAIL_SENDER=your-email@example.com
# EMAIL_PASSWORD=your-email-password
# SMTP_SERVER=your-smtp-server
# SMTP_PORT=your-smtp-port
