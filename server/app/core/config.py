import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    # App Info
    PROJECT_NAME: str = "AI Doc Q&A"
    VERSION: str = "1.0.0"

    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # MongoDB
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")

    # Upload
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "uploads")

    # Vector DB
    VECTOR_DB_DIR: str = os.getenv("VECTOR_DB_DIR", "vector_db")

    # Optional future configs
    MAX_CHUNK_SIZE: int = int(os.getenv("MAX_CHUNK_SIZE", 500))


# Create a single instance
settings = Settings()