import os
from dotenv import load_dotenv

load_dotenv()

# Load enviornment variables as constants from env file
if os.environ.get("APPLICATION_MODE") == 'DEVELOPMENT':
    # Constants for authorization operations
    JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

    # LLM Credentials
    OPEN_AI_API_KEY = os.environ.get("OPEN_AI_API_KEY")
    GEMINI_API_KEY = os.environ.get("GEMINI_AI_API_KEY")
    
