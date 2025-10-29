import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from backend.config import settings
from datetime import datetime
from typing import List

async def send_email(to_email: str, subject: str, body: str):
    """Send email notification"""
    try:
        message = MIMEMultipart("alternative")
        message["From"] = settings.EMAIL_FROM
        message["To"] = to_email
        message["Subject"] = subject
        
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f4f4f4;">
                <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h2 style="color: #4F46E5; margin-bottom: 20px;">Student Academic Planner</h2>
                    <div style="color: #333; line-height: 1.6;">
                        {body}
                    </div>
                    <hr style="margin: 20px 0; border: none; border-top: 1px solid #e0e0e0;">
                    <p style="color: #666; font-size: 12px; margin-top: 20px;">
                        This is an automated notification from your Student Academic Planner.
                    </p>
                </div>
            </body>
        </html>
        """
        
        message.attach(MIMEText(html_body, "html"))
        
        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            start_tls=True,
        )
        print(f"Email sent successfully to {to_email}")
        return True
    except Exception as e:
        print(f"Failed to send email to {to_email}: {str(e)}")
        return False

async def send_assignment_notification(user_email: str, assignment_title: str, course_name: str, due_date: datetime):
    """Send notification when a new assignment is added"""
    subject = "New Assignment Added"
    body = f"""
        <h3>New Assignment Created</h3>
        <p><strong>Assignment:</strong> {assignment_title}</p>
        <p><strong>Course:</strong> {course_name}</p>
        <p><strong>Due Date:</strong> {due_date.strftime('%B %d, %Y at %I:%M %p')}</p>
        <p>Don't forget to complete this assignment on time!</p>
    """
    await send_email(user_email, subject, body)

async def send_schedule_notification(user_email: str, schedule_title: str, start_time: datetime, end_time: datetime):
    """Send notification when a new schedule is added"""
    subject = "New Schedule Added"
    body = f"""
        <h3>New Schedule Created</h3>
        <p><strong>Event:</strong> {schedule_title}</p>
        <p><strong>Start Time:</strong> {start_time.strftime('%B %d, %Y at %I:%M %p')}</p>
        <p><strong>End Time:</strong> {end_time.strftime('%B %d, %Y at %I:%M %p')}</p>
        <p>This event has been added to your schedule.</p>
    """
    await send_email(user_email, subject, body)

async def send_assignment_reminder(user_email: str, assignment_title: str, course_name: str, due_date: datetime):
    """Send reminder for upcoming assignment"""
    subject = f"Reminder: Assignment Due Soon - {assignment_title}"
    body = f"""
        <h3 style="color: #DC2626;">⏰ Assignment Reminder</h3>
        <p><strong>Assignment:</strong> {assignment_title}</p>
        <p><strong>Course:</strong> {course_name}</p>
        <p><strong>Due Date:</strong> {due_date.strftime('%B %d, %Y at %I:%M %p')}</p>
        <p style="color: #DC2626; font-weight: bold;">This assignment is due in less than 2 days!</p>
        <p>Make sure to complete it on time to avoid any penalties.</p>
    """
    await send_email(user_email, subject, body)
