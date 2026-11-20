
# Student Management API

A REST API built using Python and FastAPI to manage
student information.

## Technology Stack

- Python
- FastAPI
- Uvicorn
- SQLite
- SQLAlchemy
- Pydantic

## Features

- REST API development
- CRUD operations
- Database connectivity
- File upload and download
- Custom middleware
- Request validation

## Project Structure

```text
app/
  main.py
  routes/
  middleware/
  uploads/
```

## Installation

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
```

Navigate into the project:

```bash
cd fastapi-student-management-api
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
uvicorn app.main:app --reload
```

## API Documentation

http://127.0.0.1:8000/docs