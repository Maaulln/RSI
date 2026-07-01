"""
Configuration settings for DARSI-CS Backend
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # App settings
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    ENV: str = os.getenv("ENV", "development")
    APP_NAME: str = "DARSI-CS"
    API_VERSION: str = "1.0.0"
    
    # Server settings
    SERVER_HOST: str = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT: int = int(os.getenv("SERVER_PORT", "8000"))
    
    # Database settings
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://darsi_user:darsi_password@localhost:5432/darsi_db"
    )
    
    # Redis settings
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # CORS settings
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ]
    
    ALLOWED_HOSTS: List[str] = [
        "localhost",
        "127.0.0.1",
        "backend",
        "darsi_backend",
    ]
    
    # JWT settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # AI Services settings
    OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://localhost:11434")
    WHISPER_URL: str = os.getenv("WHISPER_URL", "http://localhost:8001")
    TTS_URL: str = os.getenv("TTS_URL", "http://localhost:8002")
    OCR_URL: str = os.getenv("OCR_URL", "http://localhost:8003")
    FACE_RECOGNITION_URL: str = os.getenv("FACE_RECOGNITION_URL", "http://localhost:8004")
    
    # LLM settings
    LLM_MODEL: str = os.getenv("LLM_MODEL", "mistral")
    LLM_MAX_TOKENS: int = 500
    LLM_TEMPERATURE: float = 0.7
    
    # External API settings
    MY_ERSIY_API_URL: str = os.getenv("MY_ERSIY_API_URL", "https://api.my-ersiy.com")
    MY_ERSIY_API_KEY: str = os.getenv("MY_ERSIY_API_KEY", "")
    
    BPJS_API_URL: str = os.getenv("BPJS_API_URL", "https://api.bpjs.com")
    BPJS_API_KEY: str = os.getenv("BPJS_API_KEY", "")
    
    SIM_RS_API_URL: str = os.getenv("SIM_RS_API_URL", "http://localhost:9000")
    SIM_RS_API_KEY: str = os.getenv("SIM_RS_API_KEY", "")
    
    # File upload settings
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "/tmp/darsi_uploads")
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # Logging settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
