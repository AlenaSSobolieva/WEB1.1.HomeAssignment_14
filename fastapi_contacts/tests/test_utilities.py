import unittest
from unittest.mock import patch, MagicMock
from fastapi_contacts.app.utilities import send_email_verification, CustomSMTP_SSL
import os


class TestUtilities(unittest.TestCase):

    @patch("fastapi_contacts.app.utilities.smtplib.SMTP_SSL", autospec=True)
    def test_send_email_verification(self, mock_smtp_ssl):
        # Replace these values with your actual environment variables
        email_sender = "your_email@example.com"
        email_password = "your_email_password"

        # Replace these values with the actual user email and ID
        user_email = "user@example.com"
        user_id = 123

        with patch.dict("os.environ", {"EMAIL_SENDER": email_sender, "EMAIL_PASSWORD": email_password}):
            smtp_instance = CustomSMTP_SSL()
            send_email_verification(smtp_instance, user_email, user_id)

        # Check if the CustomSMTP class was instantiated with the correct arguments
        mock_smtp_ssl.assert_called_once_with(
            os.getenv("SMTP_SERVER"), os.getenv("SMTP_PORT"), *(), **{})

        mock_smtp_instance = mock_smtp_ssl.return_value
        mock_smtp_instance.starttls.assert_called_once()
        mock_smtp_instance.login.assert_called_once_with(email_sender, email_password)

        # Verify that the sendmail method is called with the correct arguments
        mock_smtp_instance.sendmail.assert_called_once_with(
            email_sender,
            user_email,
            'Content-Type: multipart/mixed; boundary="===============8820278361265581765=="\nMIME-Version: 1.0\nFrom: your_email@example.com\nTo: user@example.com\nSubject: Email Verification\n\n--===============8820278361265581765==\nContent-Type: text/plain\n\nClick the link to verify your email: http://your-app-url/verify-email/123\n\n--===============8820278361265581765==--\n',
        )


if __name__ == '__main__':
    unittest.main()
