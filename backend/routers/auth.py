from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from backend.models import UserCreate, UserResponse, Token, User
from backend.auth_utils import get_password_hash, verify_password, create_access_token, get_current_user
from backend.database import get_database
from backend.config import settings
from bson import ObjectId

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    """Register a new user"""
    db = await get_database()
    
    # Check if user already exists
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user_dict = user.dict()
    user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))
    
    result = await db.users.insert_one(user_dict)
    created_user = await db.users.find_one({"_id": result.inserted_id})
    
    return UserResponse(
        id=str(created_user["_id"]),
        email=created_user["email"],
        full_name=created_user["full_name"]
    )

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login and get access token"""
    db = await get_database()
    
    # Find user
    user = await db.users.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current user information"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    db = await get_database()
    
    # If _id is a string, try to convert it to ObjectId
    user_id = current_user.get("_id")
    if isinstance(user_id, str):
        try:
            user_id = ObjectId(user_id)
        except:
            pass
    
    # Try to get the user by _id or email
    user = None
    if user_id:
        user = await db.users.find_one({"_id": user_id})
    
    if not user and current_user.get("email"):
        user = await db.users.find_one({"email": current_user.get("email")})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Convert ObjectId to string for the response
    user["_id"] = str(user["_id"])
    
    return UserResponse(
        id=user["_id"],
        email=user.get("email", ""),
        full_name=user.get("full_name", "")
    )
