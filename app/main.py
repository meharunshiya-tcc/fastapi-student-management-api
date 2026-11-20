
from fastapi import FastAPI

# Create FastAPI application
app = FastAPI(
    title="Student Management API",
    description="A REST API built using FastAPI",
    version="1.0.0"
)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to Student Management API",
        "status": "Running"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }