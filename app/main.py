from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app import models

from app.routes import students
from app.middleware.logging import logging_middleware

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI(
    title="Student Management API",
    description="CRUD, Database, File Handling and Middleware",
    version="1.0.0"
)

# Custom middleware
app.middleware("http")(logging_middleware)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Register routes
app.include_router(students.router)

@app.get("/")
def home():
    return {
        "message": "Student Management API is running"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }