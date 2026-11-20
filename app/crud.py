from sqlalchemy.orm import Session
from sqlalchemy import select
from app import models, schemas

def get_students(db: Session):
    return db.scalars(
        select(models.Student)
    ).all()

def get_student(db: Session, student_id: int):
    return db.get(models.Student, student_id)

def create_student(db: Session, student: schemas.StudentCreate):

    existing = db.scalar(
        select(models.Student).where(
            models.Student.email == student.email
        )
    )

    if existing:
        raise ValueError("Email already registered")

    new_student = models.Student(**student.model_dump())

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student

def update_student(
    db: Session,
    student_id: int,
    student: dict
):
    existing = get_student(db, student_id)

    if not existing:
        return None

    if "email" in student:
        duplicate = db.scalar(
            select(models.Student).where(
                models.Student.email == student["email"],
                models.Student.id != student_id
            )
        )

        if duplicate:
            raise ValueError("Email already registered")

    for key, value in student.items():
        setattr(existing, key, value)

    db.commit()
    db.refresh(existing)

    return existing

def delete_student(db: Session, student_id: int):

    student = get_student(db, student_id)

    if not student:
        return False

    db.delete(student)
    db.commit()

    return True