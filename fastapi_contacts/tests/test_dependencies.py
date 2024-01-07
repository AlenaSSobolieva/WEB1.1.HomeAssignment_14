import unittest
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from unittest.mock import patch
from fastapi_contacts.app.dependencies import RateLimiter, get_current_user, get_current_user_rate_limited

class TestRateLimiter(unittest.TestCase):

    def test_limit_exceeded(self):
        rate_limiter = RateLimiter(requests=2, seconds=60)
        username = "test_user"

        # Test the rate limit not exceeded initially
        self.assertFalse(rate_limiter.limit_exceeded(username))

        # Test the rate limit exceeded after making requests
        for _ in range(rate_limiter.requests):
            rate_limiter.limit_exceeded(username)

        self.assertTrue(rate_limiter.limit_exceeded(username))

        # Test the rate limit reset after the time window
        rate_limiter.token_info[username] = [datetime.utcnow() - timedelta(seconds=rate_limiter.seconds)]
        self.assertFalse(rate_limiter.limit_exceeded(username))

class TestDependencies(unittest.TestCase):

    @staticmethod
    def mock_jwt_decode(token):
        return {"sub": "test_user"}

    @patch('fastapi_contacts.app.dependencies.get_current_user')
    def test_get_current_user_rate_limited(self, mock_get_current_user):
        # Mock OAuth2PasswordBearer token
        token = "mock_token"

        # Configure the mock to return the desired value
        mock_get_current_user.return_value = "test_user"
        rate_limiter = RateLimiter(requests=5, seconds=60)
        rate_limiter.limit_exceeded = lambda username: False  # Mock rate limit not exceeded

        try:
            # Test the get_current_user_rate_limited function
            result = get_current_user_rate_limited(token=token)
            self.assertEqual(result, "test_user")
        finally:
            # Ensure the mock is restored
            mock_get_current_user.assert_called_once_with(token=token)
            mock_get_current_user.reset_mock()

if __name__ == '__main__':
    unittest.main()
