from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from backend.models import ScheduleCreate, ScheduleResponse
from backend.auth import get_current_user_id, get_current_user
from backend.database import get_database
from bson import ObjectId
from backend.email_service import send_schedule_notification
from datetime import datetime

router = APIRouter(prefix="/api/schedules", tags=["Schedules"])

@router.post("/", response_model=ScheduleResponse)
async def create_schedule(
    schedule: ScheduleCreate,
    user_id: str = Depends(get_current_user_id),
    current_user: dict = Depends(get_current_user)
):
    """Create a new schedule"""
    db = await get_database()
    
    # Verify course exists if course_id is provided
    course_name = None
    if schedule.course_id:
        if not ObjectId.is_valid(schedule.course_id):
            raise HTTPException(status_code=400, detail="Invalid course ID")
        
        course = await db.courses.find_one({
            "_id": ObjectId(schedule.course_id),
            "user_id": user_id
        })
        
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        
        course_name = course["course_name"]
    
    schedule_dict = schedule.dict()
    schedule_dict["user_id"] = user_id
    schedule_dict["created_at"] = datetime.utcnow()
    
    result = await db.schedules.insert_one(schedule_dict)
    created_schedule = await db.schedules.find_one({"_id": result.inserted_id})
    
    # Send email notification
    try:
        await send_schedule_notification(
            user_email=current_user["email"],
            schedule_title=created_schedule["title"],
            start_time=created_schedule["start_time"],
            end_time=created_schedule["end_time"]
        )
    except Exception as e:
        print(f"Failed to send email notification: {str(e)}")
    
    return ScheduleResponse(
        id=str(created_schedule["_id"]),
        title=created_schedule["title"],
        description=created_schedule.get("description"),
        course_id=str(created_schedule["course_id"]) if created_schedule.get("course_id") else None,
        course_name=course_name,
        start_time=created_schedule["start_time"],
        end_time=created_schedule["end_time"],
        day_of_week=created_schedule.get("day_of_week"),
        location=created_schedule.get("location"),
        created_at=created_schedule.get("created_at", datetime.utcnow())
    )

@router.get("/", response_model=List[ScheduleResponse])
async def get_schedules(user_id: str = Depends(get_current_user_id)):
    """Get all schedules for the current user"""
    db = await get_database()
    
    schedules = await db.schedules.find({"user_id": user_id}).sort("start_time", 1).to_list(length=None)
    
    result = []
    for schedule in schedules:
        course_name = None
        if schedule.get("course_id"):
            course = await db.courses.find_one({"_id": ObjectId(schedule["course_id"])})
            course_name = course["course_name"] if course else None
        
        result.append(ScheduleResponse(
            id=str(schedule["_id"]),
            title=schedule["title"],
            description=schedule.get("description"),
            course_id=str(schedule["course_id"]) if schedule.get("course_id") else None,
            course_name=course_name,
            start_time=schedule["start_time"],
            end_time=schedule["end_time"],
            day_of_week=schedule.get("day_of_week"),
            location=schedule.get("location"),
            created_at=schedule.get("created_at", datetime.utcnow())
        ))
    
    return result

@router.get("/{schedule_id}", response_model=ScheduleResponse)
async def get_schedule(
    schedule_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """Get a specific schedule"""
    db = await get_database()
    
    if not ObjectId.is_valid(schedule_id):
        raise HTTPException(status_code=400, detail="Invalid schedule ID")
    
    schedule = await db.schedules.find_one({
        "_id": ObjectId(schedule_id),
        "user_id": user_id
    })
    
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    course_name = None
    if schedule.get("course_id"):
        course = await db.courses.find_one({"_id": ObjectId(schedule["course_id"])})
        course_name = course["course_name"] if course else None
    
    return ScheduleResponse(
        id=str(schedule["_id"]),
        title=schedule["title"],
        description=schedule.get("description"),
        course_id=str(schedule["course_id"]) if schedule.get("course_id") else None,
        course_name=course_name,
        start_time=schedule["start_time"],
        end_time=schedule["end_time"],
        day_of_week=schedule.get("day_of_week"),
        location=schedule.get("location"),
        created_at=schedule.get("created_at", datetime.utcnow())
    )

@router.put("/{schedule_id}", response_model=ScheduleResponse)
async def update_schedule(
    schedule_id: str,
    schedule: ScheduleCreate,
    user_id: str = Depends(get_current_user_id)
):
    """Update a schedule"""
    db = await get_database()
    
    if not ObjectId.is_valid(schedule_id):
        raise HTTPException(status_code=400, detail="Invalid schedule ID")
    
    # Verify course exists if course_id is provided
    course_name = None
    if schedule.course_id:
        if not ObjectId.is_valid(schedule.course_id):
            raise HTTPException(status_code=400, detail="Invalid course ID")
        
        course = await db.courses.find_one({
            "_id": ObjectId(schedule.course_id),
            "user_id": user_id
        })
        
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        
        course_name = course["course_name"]
    
    result = await db.schedules.update_one(
        {"_id": ObjectId(schedule_id), "user_id": user_id},
        {"$set": schedule.dict()}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    updated_schedule = await db.schedules.find_one({"_id": ObjectId(schedule_id)})
    
    return ScheduleResponse(
        id=str(updated_schedule["_id"]),
        title=updated_schedule["title"],
        description=updated_schedule.get("description"),
        course_id=str(updated_schedule["course_id"]) if updated_schedule.get("course_id") else None,
        course_name=course_name,
        start_time=updated_schedule["start_time"],
        end_time=updated_schedule["end_time"],
        day_of_week=updated_schedule.get("day_of_week"),
        location=updated_schedule.get("location"),
        created_at=updated_schedule.get("created_at", datetime.utcnow())
    )

@router.delete("/{schedule_id}")
async def delete_schedule(
    schedule_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """Delete a schedule"""
    db = await get_database()
    
    if not ObjectId.is_valid(schedule_id):
        raise HTTPException(status_code=400, detail="Invalid schedule ID")
    
    result = await db.schedules.delete_one({
        "_id": ObjectId(schedule_id),
        "user_id": user_id
    })
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    return {"message": "Schedule deleted successfully"}
