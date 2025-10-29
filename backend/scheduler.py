from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
from backend.database import get_database
from backend.email_service import send_assignment_reminder
import asyncio

scheduler = AsyncIOScheduler()

async def check_assignment_reminders():
    """Check for assignments due in 2 days and send reminders"""
    try:
        db = await get_database()
        
        # Calculate the date range for assignments due in approximately 2 days
        now = datetime.utcnow()
        two_days_from_now = now + timedelta(days=2)
        two_days_plus_one_hour = two_days_from_now + timedelta(hours=1)
        
        # Find assignments due within the next 2 days that haven't been reminded yet
        assignments = await db.assignments.find({
            "due_date": {
                "$gte": now,
                "$lte": two_days_plus_one_hour
            },
            "completed": False,
            "reminder_sent": {"$ne": True}
        }).to_list(length=None)
        
        print(f"Found {len(assignments)} assignments needing reminders")
        
        for assignment in assignments:
            # Get user email
            user = await db.users.find_one({"_id": assignment["user_id"]})
            if not user:
                continue
            
            # Get course name
            course = await db.courses.find_one({"_id": assignment["course_id"]})
            course_name = course["course_name"] if course else "Unknown Course"
            
            # Send reminder email
            await send_assignment_reminder(
                user_email=user["email"],
                assignment_title=assignment["title"],
                course_name=course_name,
                due_date=assignment["due_date"]
            )
            
            # Mark reminder as sent
            await db.assignments.update_one(
                {"_id": assignment["_id"]},
                {"$set": {"reminder_sent": True}}
            )
            
            print(f"Sent reminder for assignment: {assignment['title']} to {user['email']}")
            
    except Exception as e:
        print(f"Error in check_assignment_reminders: {str(e)}")

def start_scheduler():
    """Start the scheduler with jobs at 10 AM and 3 PM"""
    # Schedule for 10:00 AM
    scheduler.add_job(
        check_assignment_reminders,
        CronTrigger(hour=10, minute=0),
        id="reminder_10am",
        name="Check assignment reminders at 10 AM",
        replace_existing=True
    )
    
    # Schedule for 3:00 PM (15:00)
    scheduler.add_job(
        check_assignment_reminders,
        CronTrigger(hour=15, minute=0),
        id="reminder_3pm",
        name="Check assignment reminders at 3 PM",
        replace_existing=True
    )
    
    scheduler.start()
    print("Scheduler started - Reminders will be sent at 10 AM and 3 PM")

def stop_scheduler():
    """Stop the scheduler"""
    scheduler.shutdown()
    print("Scheduler stopped")
