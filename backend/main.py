from fastapi import FastAPI, Response, Request, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from backend.database import connect_to_mongo, close_mongo_connection
from backend.scheduler import start_scheduler, stop_scheduler
from backend.routers import auth, courses, assignments, schedules, chat

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        await connect_to_mongo()
        print("✅ Successfully connected to MongoDB")
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        raise
        
    try:
        start_scheduler()
        print("✅ Scheduler started successfully")
    except Exception as e:
        print(f"❌ Failed to start scheduler: {e}")
        raise
        
    yield
    
    # Shutdown
    try:
        stop_scheduler()
        print("🛑 Scheduler stopped")
    except Exception as e:
        print(f"⚠️ Error stopping scheduler: {e}")
        
    try:
        await close_mongo_connection()
        print("🛑 MongoDB connection closed")
    except Exception as e:
        print(f"⚠️ Error closing MongoDB connection: {e}")

app = FastAPI(
    title="Student Academic Planner API",
    description="A comprehensive student time management and academic planning application",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only - replace with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Handle OPTIONS method for CORS preflight
@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    if request.method == "OPTIONS":
        response = Response(
            status_code=status.HTTP_200_OK,
            content="OK",
            media_type="text/plain"
        )
    else:
        response = await call_next(request)
    
    origin = request.headers.get('Origin', '*')
    response.headers["Access-Control-Allow-Origin"] = origin
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Expose-Headers"] = "*"
    return response

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
