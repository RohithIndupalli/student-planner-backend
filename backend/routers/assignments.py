from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from backend.models import AssignmentCreate, AssignmentResponse
from backend.auth import get_current_user_id, get_current_user
from backend.database import get_database
from bson import ObjectId
from backend.email_service import send_assignment_notification
from datetime import datetime

router = APIRouter(prefix="/api/assignments", tags=["Assignments"])

@router.post("/", response_model=AssignmentResponse)
async def create_assignment(
    assignment: AssignmentCreate,
    user_id: str = Depends(get_current_user_id),
    current_user: dict = Depends(get_current_user)
):
    """Create a new assignment"""
    db = await get_database()
    
    # Verify course exists and belongs to user
    if not ObjectId.is_valid(assignment.course_id):
        raise HTTPException(status_code=400, detail="Invalid course ID")
    
    course = await db.courses.find_one({
        "_id": ObjectId(assignment.course_id),
        "user_id": user_id
    })
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    assignment_dict = assignment.dict()
    assignment_dict["user_id"] = user_id
    assignment_dict["completed"] = False
    assignment_dict["reminder_sent"] = False
    assignment_dict["created_at"] = datetime.utcnow()
    
    result = await db.assignments.insert_one(assignment_dict)
    created_assignment = await db.assignments.find_one({"_id": result.inserted_id})
    
    # Send email notification
    try:
        await send_assignment_notification(
            user_email=current_user["email"],
            assignment_title=created_assignment["title"],
            course_name=course["course_name"],
            due_date=created_assignment["due_date"]
        )
    except Exception as e:
        print(f"Failed to send email notification: {str(e)}")
    
    return AssignmentResponse(
        id=str(created_assignment["_id"]),
        title=created_assignment["title"],
        description=created_assignment.get("description"),
        course_id=str(created_assignment["course_id"]),
        course_name=course["course_name"],
        due_date=created_assignment["due_date"],
        priority=created_assignment["priority"],
        completed=created_assignment["completed"],
        created_at=created_assignment.get("created_at", datetime.utcnow())
    )

@router.get("/", response_model=List[AssignmentResponse])
async def get_assignments(user_id: str = Depends(get_current_user_id)):
    """Get all assignments for the current user"""
    db = await get_database()
    
    assignments = await db.assignments.find({"user_id": user_id}).sort("due_date", 1).to_list(length=None)
    
    result = []
    for assignment in assignments:
        course = await db.courses.find_one({"_id": ObjectId(assignment["course_id"])})
        course_name = course["course_name"] if course else "Unknown Course"
        
        result.append(AssignmentResponse(
            id=str(assignment["_id"]),
            title=assignment["title"],
            description=assignment.get("description"),
            course_id=str(assignment["course_id"]),
            course_name=course_name,
            due_date=assignment["due_date"],
            priority=assignment["priority"],
            completed=assignment["completed"],
            created_at=assignment.get("created_at", datetime.utcnow())
        ))
    
    return result

@router.get("/{assignment_id}", response_model=AssignmentResponse)
async def get_assignment(
    assignment_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """Get a specific assignment"""
    db = await get_database()
    
    if not ObjectId.is_valid(assignment_id):
        raise HTTPException(status_code=400, detail="Invalid assignment ID")
    
    assignment = await db.assignments.find_one({
        "_id": ObjectId(assignment_id),
        "user_id": user_id
    })
    
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    course = await db.courses.find_one({"_id": ObjectId(assignment["course_id"])})
    course_name = course["course_name"] if course else "Unknown Course"
    
    return AssignmentResponse(
        id=str(assignment["_id"]),
        title=assignment["title"],
        description=assignment.get("description"),
        course_id=str(assignment["course_id"]),
        course_name=course_name,
        due_date=assignment["due_date"],
        priority=assignment["priority"],
        completed=assignment["completed"],
        created_at=assignment.get("created_at", datetime.utcnow())
    )

@router.put("/{assignment_id}", response_model=AssignmentResponse)
async def update_assignment(
    assignment_id: str,
    assignment: AssignmentCreate,
    user_id: str = Depends(get_current_user_id)
):
    """Update an assignment"""
    db = await get_database()
    
    if not ObjectId.is_valid(assignment_id):
        raise HTTPException(status_code=400, detail="Invalid assignment ID")
    
    # Verify course exists
    if not ObjectId.is_valid(assignment.course_id):
        raise HTTPException(status_code=400, detail="Invalid course ID")
    
    course = await db.courses.find_one({
        "_id": ObjectId(assignment.course_id),
        "user_id": user_id
    })
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    result = await db.assignments.update_one(
        {"_id": ObjectId(assignment_id), "user_id": user_id},
        {"$set": assignment.dict()}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    updated_assignment = await db.assignments.find_one({"_id": ObjectId(assignment_id)})
    
    return AssignmentResponse(
        id=str(updated_assignment["_id"]),
        title=updated_assignment["title"],
        description=updated_assignment.get("description"),
        course_id=str(updated_assignment["course_id"]),
        course_name=course["course_name"],
        due_date=updated_assignment["due_date"],
        priority=updated_assignment["priority"],
        completed=updated_assignment["completed"],
        created_at=updated_assignment.get("created_at", datetime.utcnow())
    )

@router.patch("/{assignment_id}/complete")
async def toggle_assignment_completion(
    assignment_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """Toggle assignment completion status"""
    db = await get_database()
    
    if not ObjectId.is_valid(assignment_id):
        raise HTTPException(status_code=400, detail="Invalid assignment ID")
    
    assignment = await db.assignments.find_one({
        "_id": ObjectId(assignment_id),
        "user_id": user_id
    })
    
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    new_status = not assignment.get("completed", False)
    
    await db.assignments.update_one(
        {"_id": ObjectId(assignment_id)},
        {"$set": {"completed": new_status}}
    )
    
    return {"message": "Assignment status updated", "completed": new_status}

@router.delete("/{assignment_id}")
async def delete_assignment(
    assignment_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """Delete an assignment"""
    db = await get_database()
    
    if not ObjectId.is_valid(assignment_id):
        raise HTTPException(status_code=400, detail="Invalid assignment ID")
    
    result = await db.assignments.delete_one({
        "_id": ObjectId(assignment_id),
        "user_id": user_id
    })
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    return {"message": "Assignment deleted successfully"}
