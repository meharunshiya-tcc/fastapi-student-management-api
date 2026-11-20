from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File
)

from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from pathlib import Path
from uuid import uuid4

from app.database import get_db
from app import schemas, crud

router = APIRouter(prefix="/students", tags=["Students"])

UPLOAD_DIR = Path("app/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".pdf"}
MAX_FILE_SIZE = 5 * 1024 * 1024

# CREATE STUDENT
@router.post("/", response_model=schemas.StudentResponse, status_code=201)
def create_student(
    student: schemas.StudentCreate,
    db: Session = Depends(get_db)
):
    try:
        return crud.create_student(db, student)
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error))

# GET ALL STUDENTS
@router.get("/", response_model=list[schemas.StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return crud.get_students(db)

# GET STUDENT BY ID
@router.get("/{student_id}", response_model=schemas.StudentResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = crud.get_student(db, student_id)

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return student

# UPDATE STUDENT - PUT
@router.put("/{student_id}", response_model=schemas.StudentResponse)
def update_student(
    student_id: int,
    student: schemas.StudentUpdate,
    db: Session = Depends(get_db)
):
    try:
        result = crud.update_student(
            db, student_id, student.model_dump()
        )

        if not result:
            raise HTTPException(status_code=404, detail="Student not found")

        return result

    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error))

# PARTIAL UPDATE - PATCH
@router.patch("/{student_id}", response_model=schemas.StudentResponse)
def patch_student(
    student_id: int,
    student: schemas.StudentPatch,
    db: Session = Depends(get_db)
):
    try:
        result = crud.update_student(
            db,
            student_id,
            student.model_dump(exclude_unset=True)
        )

        if not result:
            raise HTTPException(status_code=404, detail="Student not found")

        return result

    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error))

# DELETE STUDENT
@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    result = crud.delete_student(db, student_id)

    if not result:
        raise HTTPException(status_code=404, detail="Student not found")

    return {"message": "Student deleted successfully"}

# UPLOAD FILE
@router.post("/{student_id}/upload")
async def upload_file(
    student_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    student = crud.get_student(db, student_id)

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    extension = Path(file.filename or "").suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="File type not allowed")

    content = await file.read(MAX_FILE_SIZE + 1)

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File exceeds 5 MB limit")

    if not content:
        raise HTTPException(status_code=400, detail="Empty file")

    filename = f"{uuid4().hex}{extension}"
    file_path = UPLOAD_DIR / filename

    file_path.write_bytes(content)

    old_filename = student.profile_picture
    student.profile_picture = filename

    try:
        db.commit()
        db.refresh(student)
    except Exception:
        db.rollback()
        file_path.unlink(missing_ok=True)
        raise

    if old_filename:
        old_path = UPLOAD_DIR / old_filename
        old_path.unlink(missing_ok=True)

    await file.close()

    return {
        "message": "File uploaded successfully",
        "filename": filename
    }

# DOWNLOAD FILE
@router.get("/{student_id}/download")
def download_file(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = crud.get_student(db, student_id)

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    if not student.profile_picture:
        raise HTTPException(status_code=404, detail="No file uploaded")

    file_path = UPLOAD_DIR / student.profile_picture

    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=file_path,
        filename=file_path.name
    )