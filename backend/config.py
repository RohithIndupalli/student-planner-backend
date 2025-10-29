from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # MongoDB
    MONGODB_URL: str = os.getenv(
        "MONGODB_URL",
        os.getenv(
            "MONGODB_URI",  # Fallback to MONGODB_URI if MONGODB_URL is not set
            "mongodb+srv://agentic_ai:Indup2414@cluster0.0s5q7br.mongodb.net/student_management?retryWrites=true&w=majority&appName=Cluster0"
        )
    )
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "student_management")
    
    def __init__(self, **data):
        super().__init__(**data)
        print(f"🔧 Using MongoDB URL: {self.MONGODB_URL}")
        print(f"🔧 Using Database: {self.DATABASE_NAME}")
    
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    
    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Email
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 587))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    EMAIL_FROM: str = os.getenv("EMAIL_FROM", "")

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
