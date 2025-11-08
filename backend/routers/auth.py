from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from backend.models import UserCreate, UserResponse, Token, User
from backend.auth_utils import (
    get_password_hash, 
    verify_password, 
    create_access_token, 
    get_current_user,
    create_tokens,
    create_refresh_token  # Add this import
)
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
    if not user or not verify_password(form_data.password, user.get("hashed_password", "")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Convert ObjectId to string for the token
    user_id = str(user["_id"])
    
    # Create token with user data including type
    token_data = {
        "sub": user["email"],
        "user_id": user_id,
        "email": user["email"],
        "type": "access"  # Add type to match what get_current_user expects
    }
    
    # Create access token directly to ensure correct structure
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data=token_data,
        expires_delta=access_token_expires
    )
    
    # Create refresh token
    refresh_token = create_refresh_token(data=token_data)
    
    tokens = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
    
    return tokens

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
    
    try:
        # First try to get user by ID if available
        if current_user.get("_id"):
            user = await db.users.find_one({"_id": ObjectId(current_user["_id"])})
            if user:
                return UserResponse(
                    id=str(user["_id"]),
                    email=user.get("email", ""),
                    full_name=user.get("full_name", "")
                )
        
        # If user not found by ID or no ID, try email
        if current_user.get("email"):
            user = await db.users.find_one({"email": current_user["email"]})
            if user:
                return UserResponse(
                    id=str(user["_id"]),
                    email=user.get("email", ""),
                    full_name=user.get("full_name", "")
                )
        
        # If we get here, user not found
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
        
    except Exception as e:
        print(f"Error in get_current_user_info: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving user information"
        )
