# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router as contacts_router
from app.database import create_tables
from app.dependencies import throttle_middleware_contact_routes


app = FastAPI()

# Apply CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Apply rate limiting middleware
app.add_middleware(throttle_middleware_contact_routes)

# Include the router for contacts
app.include_router(contacts_router, prefix="/contacts", tags=["contacts"])

# Call create_tables to initialize the database tables
create_tables()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
