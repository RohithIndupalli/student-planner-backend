from fastapi import APIRouter
from backend.routers import auth, courses, assignments, schedules, chat

router = APIRouter()
router.include_router(auth.router, tags=["Authentication"])
router.include_router(courses.router, prefix="/courses", tags=["Courses"])
router.include_router(assignments.router, prefix="/assignments", tags=["Assignments"])
router.include_router(schedules.router, prefix="/schedules", tags=["Schedules"])
router.include_router(chat.router, prefix="/chat", tags=["AI Chat"])

__all__ = ["router", "auth", "courses", "assignments", "schedules", "chat"]
