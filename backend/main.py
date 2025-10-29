from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from backend.database import connect_to_mongo, close_mongo_connection
from backend.scheduler import start_scheduler, stop_scheduler
from backend.routers import auth, courses, assignments, schedules, chat

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    start_scheduler()
    yield
    # Shutdown
    stop_scheduler()
    await close_mongo_connection()

app = FastAPI(
    title="Student Academic Planner API",
    description="A comprehensive student time management and academic planning application",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://student-planner-frontend.onrender.com",
        "https://student-planner-backend.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(assignments.router)
app.include_router(schedules.router)
app.include_router(chat.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to Student Academic Planner API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
