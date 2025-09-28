"""Configuration settings for the A2A agent platform."""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Google AI Configuration
GOOGLE_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY")
GOOGLE_GENAI_USE_VERTEXAI: bool = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "FALSE").upper() == "TRUE"
GOOGLE_CLOUD_PROJECT: Optional[str] = os.getenv("GOOGLE_CLOUD_PROJECT")
GOOGLE_CLOUD_LOCATION: str = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

# Platform Configuration
PLATFORM_HOST: str = os.getenv("PLATFORM_HOST", "127.0.0.1")
SECRETARY_PORT: int = int(os.getenv("SECRETARY_PORT", "10000"))
HIRING_MANAGER_PORT: int = int(os.getenv("HIRING_MANAGER_PORT", "10001"))
EMPLOYEE_BASE_PORT: int = int(os.getenv("EMPLOYEE_BASE_PORT", "10002"))

# Logging
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

# Model Configuration
DEFAULT_MODEL: str = "gemini-2.0-flash-001"

# Validation
def validate_config() -> None:
    """Validate configuration settings."""
    if not GOOGLE_GENAI_USE_VERTEXAI and not GOOGLE_API_KEY:
        raise ValueError(
            "Either GOOGLE_API_KEY must be set or GOOGLE_GENAI_USE_VERTEXAI must be TRUE"
        )
    
    if GOOGLE_GENAI_USE_VERTEXAI and not GOOGLE_CLOUD_PROJECT:
        raise ValueError(
            "GOOGLE_CLOUD_PROJECT must be set when using Vertex AI"
        )

# Set up Google AI environment variables
if GOOGLE_GENAI_USE_VERTEXAI:
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "TRUE"
    os.environ["GOOGLE_CLOUD_PROJECT"] = GOOGLE_CLOUD_PROJECT or ""
    os.environ["GOOGLE_CLOUD_LOCATION"] = GOOGLE_CLOUD_LOCATION
elif GOOGLE_API_KEY:
    os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
