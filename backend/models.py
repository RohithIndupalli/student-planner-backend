from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")

# User Models
class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    
    class Config:
        populate_by_name = True

# Course Models
class CourseBase(BaseModel):
    course_name: str
    course_code: Optional[str] = None
    instructor: Optional[str] = None
    description: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class CourseResponse(BaseModel):
    id: str
    course_name: str
    course_code: Optional[str] = None
    instructor: Optional[str] = None
    description: Optional[str] = None
    created_at: datetime
    
    class Config:
        populate_by_name = True

# Assignment Models
class AssignmentBase(BaseModel):
    title: str
    description: Optional[str] = None
    course_id: str
    due_date: datetime
    priority: Optional[str] = "medium"  # low, medium, high

class AssignmentCreate(AssignmentBase):
    pass

class Assignment(AssignmentBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: str
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    reminder_sent: bool = False
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class AssignmentResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    course_id: str
    course_name: Optional[str] = None
    due_date: datetime
    priority: str
    completed: bool
    created_at: datetime
    
    class Config:
        populate_by_name = True

# Schedule Models
class ScheduleBase(BaseModel):
    title: str
    description: Optional[str] = None
    course_id: Optional[str] = None
    start_time: datetime
    end_time: datetime
    day_of_week: Optional[str] = None  # Monday, Tuesday, etc.
    location: Optional[str] = None

class ScheduleCreate(ScheduleBase):
    pass

class Schedule(ScheduleBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class ScheduleResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    course_id: Optional[str] = None
    course_name: Optional[str] = None
    start_time: datetime
    end_time: datetime
    day_of_week: Optional[str] = None
    location: Optional[str] = None
    created_at: datetime
    
    class Config:
        populate_by_name = True

# Token Models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Chat Models
class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
