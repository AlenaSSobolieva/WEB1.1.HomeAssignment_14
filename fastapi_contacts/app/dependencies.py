# app/dependencies.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from security import SECRET_KEY, ALGORITHM

# Define a simple rate limiting mechanism
class RateLimiter:
    def __init__(self, requests: int, seconds: int):
        self.requests = requests
        self.seconds = seconds
        self.token_info = {}

    def limit_exceeded(self, username: str):
        now = datetime.utcnow()
        user_info = self.token_info.get(username, [])
        user_info = [t for t in user_info if now - t <= timedelta(seconds=self.seconds)]
        if len(user_info) >= self.requests:
            return True
        self.token_info[username] = user_info + [now]
        return False

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Define the rate limiter with 5 requests per 60 seconds
rate_limiter = RateLimiter(requests=5, seconds=60)

def get_current_user(token: str = Depends(oauth2_scheme)):
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

    # Check rate limiting
    if rate_limiter.limit_exceeded(username):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded",
            headers={"Retry-After": str(rate_limiter.seconds)},
        )

    return username

def get_current_user_rate_limited(token: str = Depends(oauth2_scheme)):
    return get_current_user(token=token)
