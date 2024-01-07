# tests/test_main.py

import pytest
from httpx import AsyncClient
from fastapi import status
from fastapi.testclient import TestClient
import fastapi_contacts.app.main

# Your test user credentials
TEST_USERNAME = "test_user"
TEST_PASSWORD = "test_password"

@pytest.fixture
def test_app():
    """
    Fixture to provide a test client for the FastAPI app.
    """
    return TestClient(fastapi_contacts.app.main.app)

@pytest.mark.asyncio
async def test_protected_route(test_app: TestClient):
    # Assuming you have a route that requires authentication, like "/protected-route"
    response = await test_app.get("/protected-route")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Now, let's simulate a login and obtain a valid token
    login_data = {
        "username": TEST_USERNAME,
        "password": TEST_PASSWORD,
    }
    login_response = await test_app.post("/token", data=login_data)
    assert login_response.status_code == status.HTTP_200_OK

    token = login_response.json()["access_token"]

    # Use the obtained token in the Authorization header for the protected route
    protected_response = await test_app.get("/protected-route", headers={"Authorization": f"Bearer {token}"})
    assert protected_response.status_code == status.HTTP_200_OK
    assert protected_response.json() == {"message": "This route is protected."}
