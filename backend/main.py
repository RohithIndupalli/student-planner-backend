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

# Allowed origins - update this list with your frontend URLs
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://student-planner-backend-1.onrender.com",
    "https://student-planner-backend-hjpl.onrender.com",
    "https://student-planner-frontend.onrender.com"  # Add your frontend URL here
]

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"],  # Expose all headers
    max_age=600  # Cache preflight response for 10 minutes
)

# Debug middleware to log CORS headers
@app.middleware("http")
async def log_cors_headers(request: Request, call_next):
    # Log the incoming request
    print(f"\n=== Incoming Request ===")
    print(f"Method: {request.method}")
    print(f"URL: {request.url}")
    print(f"Headers: {dict(request.headers)}")
    
    # Handle preflight requests
    if request.method == "OPTIONS":
        print("Handling OPTIONS preflight request")
        response = Response(
            status_code=status.HTTP_204_NO_CONTENT,
            headers={
                "Access-Control-Allow-Origin": request.headers.get("Origin", "*"),
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Max-Age": "600",
            },
        )
        return response
    
    # Process the request
    response = await call_next(request)
    
    # Add CORS headers to the response
    origin = request.headers.get("Origin")
    if origin in ALLOWED_ORIGINS:
        response.headers["Access-Control-Allow-Origin"] = origin
    else:
        # For debugging, allow any origin in development
        response.headers["Access-Control-Allow-Origin"] = "*"
    
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Expose-Headers"] = "*"
    
    # Log the response headers
    print(f"\n=== Response Headers ===")
    for key, value in response.headers.items():
        print(f"{key}: {value}")
    
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
