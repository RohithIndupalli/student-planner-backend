# Quick Setup Guide

## Prerequisites Checklist

Before you begin, ensure you have:

- [ ] **Python 3.8+** installed ([Download](https://www.python.org/downloads/))
- [ ] **Node.js 16+** installed ([Download](https://nodejs.org/))
- [ ] **MongoDB** installed and running ([Download](https://www.mongodb.com/try/download/community))
- [ ] **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))
- [ ] **Gmail account** with App Password for email notifications

## Step-by-Step Setup

### 1. MongoDB Setup

**Option A: Local MongoDB**
```bash
# Install MongoDB Community Edition
# Start MongoDB service
mongod --dbpath C:\data\db
```

**Option B: MongoDB Atlas (Cloud)**
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free cluster
3. Get your connection string
4. Use it in the `.env` file

### 2. OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (you won't see it again!)

### 3. Gmail App Password

1. Go to your [Google Account](https://myaccount.google.com/)
2. Navigate to **Security**
3. Enable **2-Step Verification** (if not already enabled)
4. Go to **Security** → **App passwords**
5. Select **Mail** and your device
6. Generate password
7. Copy the 16-character password

### 4. Backend Configuration

1. Navigate to the `backend` folder
2. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```

3. Edit `.env` file with your credentials:
   ```env
   MONGODB_URL=mongodb://localhost:27017
   DATABASE_NAME=student_management
   SECRET_KEY=your-super-secret-key-change-this-in-production
   
   OPENAI_API_KEY=sk-your-openai-api-key-here
   
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=your-16-char-app-password
   EMAIL_FROM=your-email@gmail.com
   ```

### 5. Start the Application

**Easy Method (Windows):**

1. **Start Backend:**
   - Double-click `start-backend.bat`
   - Wait for "Application startup complete"

2. **Start Frontend:**
   - Double-click `start-frontend.bat`
   - Wait for "Local: http://localhost:3000"

**Manual Method:**

**Terminal 1 - Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### 6. Access the Application

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

## First Time Usage

1. **Register an Account**
   - Go to http://localhost:3000
   - Click "Sign up"
   - Enter your name, email, and password
   - Use a real email to receive notifications

2. **Add Your First Course**
   - Navigate to "Courses"
   - Click "Add Course"
   - Fill in course details

3. **Create an Assignment**
   - Navigate to "Assignments"
   - Click "Add Assignment"
   - Select a course and set due date
   - Check your email for notification!

4. **Try the AI Assistant**
   - Navigate to "AI Assistant"
   - Ask: "How should I prioritize my assignments?"
   - Get personalized advice!

## Testing Email Notifications

To test if email notifications work:

1. Create an assignment with a due date
2. Check your email inbox
3. You should receive an email immediately

To test automated reminders:
- Create an assignment due in 2 days
- Wait for 10 AM or 3 PM
- You'll receive a reminder email

## Troubleshooting

### Backend won't start
- **Error: "No module named 'fastapi'"**
  - Solution: Make sure virtual environment is activated
  - Run: `pip install -r requirements.txt`

- **Error: "Connection refused" (MongoDB)**
  - Solution: Start MongoDB service
  - Run: `mongod --dbpath C:\data\db`

### Frontend won't start
- **Error: "Cannot find module"**
  - Solution: Install dependencies
  - Run: `npm install`

### Email not sending
- **Check:**
  - Gmail App Password (not regular password)
  - 2FA is enabled on Google account
  - SMTP credentials in `.env` are correct

### AI Chatbot not working
- **Check:**
  - OpenAI API key is valid
  - You have API credits
  - Key is correctly set in `.env`

### "Model provider unreachable"
- This means the OpenAI API cannot be reached
- **Solutions:**
  - Verify your API key is correct
  - Check your internet connection
  - Ensure you have OpenAI API credits
  - Try a different OpenAI model in `ai_chatbot.py`

## Default Ports

- **Backend:** 8000
- **Frontend:** 3000
- **MongoDB:** 27017

If these ports are in use, you can change them:
- Backend: Edit `uvicorn main:app --reload --port 8001`
- Frontend: Edit `vite.config.js` → `server.port`

## Next Steps

Once everything is running:

1. ✅ Explore the dashboard
2. ✅ Add multiple courses
3. ✅ Create assignments with different priorities
4. ✅ Set up your schedule
5. ✅ Chat with the AI assistant
6. ✅ Wait for automated email reminders

## Need Help?

- Check the main `README.md` for detailed documentation
- Review API docs at http://localhost:8000/docs
- Ensure all prerequisites are installed
- Verify all environment variables are set correctly

## Security Reminder

⚠️ **Important:**
- Never commit `.env` file to version control
- Change `SECRET_KEY` before deploying to production
- Keep your OpenAI API key private
- Use environment variables for sensitive data
