from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    department: str

class StudentUpdate(BaseModel):
    name: str
    email: EmailStr
    department: str

class StudentPatch(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    department: Optional[str] = None

class StudentResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    department: str
    profile_picture: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)