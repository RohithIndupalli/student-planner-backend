@echo off
echo Starting Student Academic Planner Backend...
echo.

cd backend

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting FastAPI server...
echo Backend will be available at http://localhost:8000
echo API Documentation at http://localhost:8000/docs
echo.

python -m uvicorn main:app --reload
pause
