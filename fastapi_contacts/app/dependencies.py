# app/dependencies.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi_contacts.app.security import SECRET_KEY, ALGORITHM

class RateLimiter:
    """
    Class implementing a simple rate limiting mechanism.

    Parameters:
    - `requests` (int): Number of allowed requests.
    - `seconds` (int): Time window in seconds.

    Usage:
    ```
    rate_limiter = RateLimiter(requests=5, seconds=60)
    if rate_limiter.limit_exceeded(username):
        # Handle rate limit exceeded
    ```

    Attributes:
    - `requests` (int): Number of allowed requests.
    - `seconds` (int): Time window in seconds.
    - `token_info` (dict): Dictionary to store token information.
    """

    def __init__(self, requests: int, seconds: int):
        self.requests = requests
        self.seconds = seconds
        self.token_info = {}

    def limit_exceeded(self, username: str):
        """
        Check if the rate limit for a user is exceeded.

        Usage:
        ```
        if rate_limiter.limit_exceeded(username):
            # Handle rate limit exceeded
        ```

        Parameters:
        - `username` (str): User identifier.

        Returns:
        - `bool`: True if rate limit exceeded, False otherwise.
        """
        now = datetime.utcnow()
        user_info = self.token_info.get(username, [])
        user_info = [t for t in user_info if now - t <= timedelta(seconds=self.seconds)]
        if len(user_info) >= self.requests:
            return True
        self.token_info[username] = user_info + [now]
        return False

# Create an instance of RateLimiter
rate_limiter = RateLimiter(requests=5, seconds=60)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Get the current user from the OAuth2 token.

    Usage:
    ```
    current_user = get_current_user(token="your_oauth2_token")
    ```

    Parameters:
    - `token` (str): OAuth2 token.

    Returns:
    - `str`: User identifier.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    if rate_limiter.limit_exceeded(username):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded",
            headers={"Retry-After": str(rate_limiter.seconds)},
        )

    return username
get_current_user.decode = jwt.decode
def get_current_user_rate_limited(token: str = Depends(oauth2_scheme)):
    """
    Get the current user with rate limiting.

    Usage:
    ```
    current_user = get_current_user_rate_limited(token="your_oauth2_token")
    ```

    Parameters:
    - `token` (str): OAuth2 token.

    Returns:
    - `str`: User identifier.
    """
    return get_current_user(token=token)
