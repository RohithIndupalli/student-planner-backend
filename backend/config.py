import os
from dotenv import load_dotenv
from typing import Optional, Dict, Any

# Load environment variables from .env file if it exists
load_dotenv()

class Settings:
    def __init__(self):
        # MongoDB Configuration
        self.MONGODB_URL: str = os.getenv(
            "MONGODB_URL",
            os.getenv(
                "MONGODB_URI",  # Fallback to MONGODB_URI if MONGODB_URL is not set
                "mongodb+srv://agentic_ai:Indup2414@cluster0.0s5q7br.mongodb.net/student_management?retryWrites=true&w=majority&appName=Cluster0"
            )
        )
        self.DATABASE_NAME: str = os.getenv("DATABASE_NAME", "student_management")
        
        # JWT Configuration
        self.SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
        self.ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
        self.ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
        
        # OpenAI Configuration
        self.OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
        
        # SMTP Configuration
        self.SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.SMTP_PORT: int = int(os.getenv("SMTP_PORT", 587))
        self.SMTP_USER: str = os.getenv("SMTP_USER", "")
        self.SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
        self.EMAIL_FROM: str = os.getenv("EMAIL_FROM", "")
        
        # Environment
        self.ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
        
        # Print configuration for debugging
        self._print_config()
    
    def _print_config(self) -> None:
        """Print configuration details (hiding sensitive information)."""
        print(" Application Configuration:")
        print(f"- Environment: {self.ENVIRONMENT}")
        print(f"- Database: {self.DATABASE_NAME}")
        print(f"- MongoDB URL: {self._mask_sensitive(self.MONGODB_URL)}")
        print(f"- JWT Algorithm: {self.ALGORITHM}")
        print(f"- Token Expiry: {self.ACCESS_TOKEN_EXPIRE_MINUTES} minutes")
        print(f"- SMTP Server: {self.SMTP_HOST}:{self.SMTP_PORT}")
        print(f"- Email From: {self.EMAIL_FROM}")
    
    @staticmethod
    def _mask_sensitive(value: str, show_chars: int = 10) -> str:
        """Mask sensitive information in logs."""
        if not value or len(value) <= show_chars * 2:
            return "[REDACTED]"
        return f"{value[:show_chars]}...{value[-show_chars:]}"

# Create a singleton instance
settings = Settings()
