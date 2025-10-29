# Student Time Management & Academic Planning Application

A full-stack application with AI chatbot, email notifications, and interactive dashboard built with FastAPI backend and React frontend.

## Features

✅ **User Authentication**
- Secure login and registration system
- JWT-based authentication
- User email storage for notifications

✅ **Interactive Dashboard**
- Real-time overview of assignments, courses, and schedules
- Visual statistics and progress tracking
- Quick action buttons

✅ **Course Management**
- Add, edit, and delete courses
- Store course names, codes, instructors, and descriptions
- Associate assignments with courses

✅ **Assignment Management**
- Create assignments with course association
- Set due dates and priority levels
- Mark assignments as complete
- Email notifications when assignments are added

✅ **Schedule/Calendar Management**
- Add and view academic schedules
- Set start/end times and locations
- Optional course association
- Email notifications for new schedules

✅ **Email Notifications**
- Instant notifications when assignments/schedules are added
- Automated reminders at 10 AM and 3 PM
- Reminders sent 2 days before assignment due dates
- Includes course name and due date details

✅ **AI Chatbot**
- Powered by LangGraph and OpenAI
- Context-aware responses based on user's courses and assignments
- Academic planning assistance
- Study schedule recommendations
- Time management advice

✅ **Modern UI**
- Clean, professional design with TailwindCSS
- Responsive layout for all devices
- Real-time notifications with toast messages
- Lucide icons for visual appeal

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **MongoDB** - NoSQL database with Motor async driver
- **LangGraph** - AI workflow orchestration
- **OpenAI GPT-3.5** - AI chatbot intelligence
- **APScheduler** - Automated email reminders
- **JWT** - Secure authentication
- **SMTP** - Email notifications

### Frontend
- **React 18** - UI library
- **Vite** - Fast build tool
- **TailwindCSS** - Utility-first CSS framework
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **date-fns** - Date formatting
- **Lucide React** - Icon library
- **React Hot Toast** - Notifications

## Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- MongoDB (local or cloud)
- OpenAI API key
- Gmail account for SMTP (or other email provider)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create a `.env` file from the example:
```bash
copy .env.example .env
```

6. Configure your `.env` file:
```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=student_management
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI API Key
OPENAI_API_KEY=your-openai-api-key-here

# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password-here
EMAIL_FROM=your-email@gmail.com
```

**Important Email Setup:**
- For Gmail, you need to create an **App Password**:
  1. Go to Google Account settings
  2. Enable 2-Factor Authentication
  3. Go to Security → App Passwords
  4. Generate a new app password for "Mail"
  5. Use this password in `SMTP_PASSWORD`

7. Start the backend server:
```bash
uvicorn main:app --reload
```

The backend will run on `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will run on `http://localhost:3000`

## Usage

### 1. Register an Account
- Navigate to `http://localhost:3000`
- Click "Sign up" and create an account with your email
- Your email will be used for notifications

### 2. Add Courses
- Go to the "Courses" page
- Click "Add Course"
- Fill in course details (name, code, instructor, description)

### 3. Create Assignments
- Go to the "Assignments" page
- Click "Add Assignment"
- Select a course, set due date, priority, and description
- You'll receive an email notification immediately
- Automated reminders will be sent 2 days before the due date at 10 AM and 3 PM

### 4. Manage Schedule
- Go to the "Schedule" page
- Click "Add Schedule"
- Set event details, time, and location
- You'll receive an email notification

### 5. Use AI Assistant
- Go to the "AI Assistant" page
- Ask questions about time management, study planning, or academic advice
- The AI has context about your courses, assignments, and schedules
- Get personalized recommendations

## API Documentation

Once the backend is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Main Endpoints

**Authentication**
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get token
- `GET /api/auth/me` - Get current user info

**Courses**
- `GET /api/courses/` - Get all courses
- `POST /api/courses/` - Create course
- `PUT /api/courses/{id}` - Update course
- `DELETE /api/courses/{id}` - Delete course

**Assignments**
- `GET /api/assignments/` - Get all assignments
- `POST /api/assignments/` - Create assignment (sends email)
- `PUT /api/assignments/{id}` - Update assignment
- `PATCH /api/assignments/{id}/complete` - Toggle completion
- `DELETE /api/assignments/{id}` - Delete assignment

**Schedules**
- `GET /api/schedules/` - Get all schedules
- `POST /api/schedules/` - Create schedule (sends email)
- `PUT /api/schedules/{id}` - Update schedule
- `DELETE /api/schedules/{id}` - Delete schedule

**AI Chat**
- `POST /api/chat/` - Send message to AI assistant

## Email Reminder System

The application includes an automated reminder system:

- **Schedule**: Runs at 10:00 AM and 3:00 PM daily
- **Trigger**: Checks for assignments due within 2 days
- **Content**: Includes assignment title, course name, and due date
- **Status**: Marks reminders as sent to avoid duplicates

## AI Chatbot Features

The AI assistant can help with:
- Analyzing your current workload
- Prioritizing assignments based on due dates
- Creating study schedules
- Balancing course loads
- Time management strategies
- Academic planning advice

The chatbot has full context of your:
- Enrolled courses
- Pending assignments with due dates
- Upcoming scheduled events

## Project Structure

```
AI/
├── backend/
│   ├── routers/
│   │   ├── auth.py
│   │   ├── courses.py
│   │   ├── assignments.py
│   │   ├── schedules.py
│   │   └── chat.py
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── auth.py
│   ├── config.py
│   ├── ai_chatbot.py
│   ├── email_service.py
│   ├── scheduler.py
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── Layout.jsx
│   │   ├── context/
│   │   │   └── AuthContext.jsx
│   │   ├── pages/
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Courses.jsx
│   │   │   ├── Assignments.jsx
│   │   │   ├── Schedule.jsx
│   │   │   └── Chat.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## Troubleshooting

### Email Not Sending
- Verify SMTP credentials in `.env`
- For Gmail, ensure you're using an App Password, not your regular password
- Check if 2FA is enabled on your Google account
- Verify SMTP_HOST and SMTP_PORT are correct

### AI Chatbot Not Working
- Ensure OPENAI_API_KEY is set in `.env`
- Check if you have sufficient OpenAI API credits
- Verify the API key is valid

### MongoDB Connection Issues
- Ensure MongoDB is running
- Check MONGODB_URL in `.env`
- Verify database permissions

### Frontend Not Connecting to Backend
- Ensure backend is running on port 8000
- Check CORS settings in `main.py`
- Verify API base URL in `frontend/src/services/api.js`

## Security Notes

- Change `SECRET_KEY` in production
- Never commit `.env` file to version control
- Use environment variables for sensitive data
- Enable HTTPS in production
- Implement rate limiting for API endpoints

## Future Enhancements

- Calendar view for schedules
- Assignment categories and tags
- File attachments for assignments
- Grade tracking
- Study session timer
- Mobile app
- Push notifications
- Collaboration features
- Export to PDF/CSV

## License

MIT License - feel free to use this project for learning and development.

## Support

For issues or questions, please create an issue in the repository.
