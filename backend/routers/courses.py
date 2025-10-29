from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from backend.models import CourseCreate, CourseResponse
from backend.auth import get_current_user_id
from backend.database import get_database
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/api/courses", tags=["Courses"])

@router.post("/", response_model=CourseResponse)
async def create_course(
    course: CourseCreate,
    user_id: str = Depends(get_current_user_id)
):
    """Create a new course"""
    db = await get_database()
    
    course_dict = course.dict()
    course_dict["user_id"] = user_id
    course_dict["created_at"] = datetime.utcnow()
    
    result = await db.courses.insert_one(course_dict)
    created_course = await db.courses.find_one({"_id": result.inserted_id})
    
    return CourseResponse(
        id=str(created_course["_id"]),
        course_name=created_course["course_name"],
        course_code=created_course.get("course_code"),
        instructor=created_course.get("instructor"),
        description=created_course.get("description"),
        created_at=created_course["created_at"]
    )

@router.get("/", response_model=List[CourseResponse])
async def get_courses(user_id: str = Depends(get_current_user_id)):
    """Get all courses for the current user"""
    db = await get_database()
    
    courses = await db.courses.find({"user_id": user_id}).to_list(length=None)
    
    return [
        CourseResponse(
            id=str(course["_id"]),
            course_name=course["course_name"],
            course_code=course.get("course_code"),
            instructor=course.get("instructor"),
            description=course.get("description"),
            created_at=course.get("created_at", datetime.utcnow())
        )
        for course in courses
    ]

@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(
    course_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """Get a specific course"""
    db = await get_database()
    
    if not ObjectId.is_valid(course_id):
        raise HTTPException(status_code=400, detail="Invalid course ID")
    
    course = await db.courses.find_one({
        "_id": ObjectId(course_id),
        "user_id": user_id
    })
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    return CourseResponse(
        id=str(course["_id"]),
        course_name=course["course_name"],
        course_code=course.get("course_code"),
        instructor=course.get("instructor"),
        description=course.get("description"),
        created_at=course.get("created_at", datetime.utcnow())
    )

@router.put("/{course_id}", response_model=CourseResponse)
async def update_course(
    course_id: str,
    course: CourseCreate,
    user_id: str = Depends(get_current_user_id)
):
    """Update a course"""
    db = await get_database()
    
    if not ObjectId.is_valid(course_id):
        raise HTTPException(status_code=400, detail="Invalid course ID")
    
    result = await db.courses.update_one(
        {"_id": ObjectId(course_id), "user_id": user_id},
        {"$set": course.dict()}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Course not found")
    
    updated_course = await db.courses.find_one({"_id": ObjectId(course_id)})
    
    return CourseResponse(
        id=str(updated_course["_id"]),
        course_name=updated_course["course_name"],
        course_code=updated_course.get("course_code"),
        instructor=updated_course.get("instructor"),
        description=updated_course.get("description"),
        created_at=updated_course.get("created_at", datetime.utcnow())
    )

@router.delete("/{course_id}")
async def delete_course(
    course_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """Delete a course"""
    db = await get_database()
    
    if not ObjectId.is_valid(course_id):
        raise HTTPException(status_code=400, detail="Invalid course ID")
    
    result = await db.courses.delete_one({
        "_id": ObjectId(course_id),
        "user_id": user_id
    })
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Course not found")
    
    return {"message": "Course deleted successfully"}
