import os
from datetime import datetime


def generate_timestamp() -> str:
    """
    Generate current timestamp string
    """
    return datetime.utcnow().isoformat()


def get_file_extension(filename: str) -> str:
    """
    Extract file extension safely
    """
    return filename.split(".")[-1].lower() if "." in filename else ""


def is_supported_file(filename: str) -> bool:
    """
    Validate supported file types
    """
    allowed_extensions = ["pdf", "txt", "mp3", "wav", "mp4", "mkv"]
    ext = get_file_extension(filename)
    return ext in allowed_extensions


def ensure_directory(path: str):
    """
    Create directory if not exists
    """
    if not os.path.exists(path):
        os.makedirs(path)


def format_file_size(size_bytes: int) -> str:
    """
    Convert bytes → readable format
    """
    if size_bytes == 0:
        return "0B"

    size_names = ("B", "KB", "MB", "GB")
    i = 0

    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024
        i += 1

    return f"{round(size_bytes, 2)} {size_names[i]}"