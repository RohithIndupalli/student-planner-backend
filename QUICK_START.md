# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Configure Environment Variables

1. Go to `backend` folder
2. Rename `.env.example` to `.env`
3. Edit `.env` and add your credentials:

```env
# MongoDB (use default for local MongoDB)
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=student_management

# Security (change this!)
SECRET_KEY=change-this-to-a-random-secret-key

# OpenAI API Key (REQUIRED for AI chatbot)
OPENAI_API_KEY=sk-your-key-here

# Gmail Settings (REQUIRED for email notifications)
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-gmail-app-password
EMAIL_FROM=your-email@gmail.com
```

### Step 2: Start MongoDB

Make sure MongoDB is running on your system:
```bash
mongod
```

### Step 3: Start Backend

**Option A - Use the batch file:**
- Double-click `start-backend.bat`

**Option B - Manual:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Step 4: Start Frontend

**Option A - Use the batch file:**
- Double-click `start-frontend.bat`

**Option B - Manual:**
```bash
cd frontend
npm install
npm run dev
```

### Step 5: Access Application

Open your browser and go to:
- **http://localhost:3000**

## 📧 Email Setup (Gmail)

1. Go to Google Account → Security
2. Enable 2-Factor Authentication
3. Go to Security → App Passwords
4. Generate password for "Mail"
5. Use this 16-character password in `.env`

## 🤖 OpenAI API Key

1. Visit https://platform.openai.com/api-keys
2. Create new API key
3. Copy and paste into `.env`

## ✅ Verify Everything Works

1. Register a new account
2. Add a course
3. Create an assignment (you should get an email!)
4. Go to AI Assistant and ask a question

## 🆘 Common Issues

**"Model provider unreachable"**
- Your OpenAI API key is missing or invalid
- Add valid key to `.env` file: `OPENAI_API_KEY=sk-...`

**Email not sending**
- Use Gmail App Password, not regular password
- Enable 2FA on your Google account first

**Backend won't start**
- Make sure MongoDB is running
- Activate virtual environment
- Install dependencies: `pip install -r requirements.txt`

**Frontend won't start**
- Run `npm install` in frontend folder
- Make sure Node.js is installed

## 📱 Features to Try

1. ✅ Dashboard - View all your academic data
2. ✅ Courses - Manage your courses
3. ✅ Assignments - Track assignments with email notifications
4. ✅ Schedule - Plan your academic calendar
5. ✅ AI Assistant - Get personalized academic advice

## 🎯 Next Steps

- Create assignments due in 2 days to test automated reminders
- Reminders are sent at 10 AM and 3 PM
- Ask the AI assistant for study planning advice
- Explore the API docs at http://localhost:8000/docs

Enjoy your Student Academic Planner! 🎓
