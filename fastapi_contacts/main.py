# app/main.py

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from fastapi_contacts.app.routes import router as contacts_router
from fastapi_contacts.app.database import create_tables
from fastapi_contacts.app.dependencies import rate_limiter, get_current_user_rate_limited

app = FastAPI()

# Apply CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router for contacts
app.include_router(contacts_router, prefix="/contacts", tags=["contacts"])

# Call create_tables to initialize the database tables
create_tables()

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

@app.get("/protected-route")
async def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": "This route is protected."}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
