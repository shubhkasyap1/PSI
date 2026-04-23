import os
from typing import List, Union
import fitz  # PyMuPDF

from app.services.transcription_service import transcribe_audio

UPLOAD_DIR = "uploads"


def get_file_path(file_id: str) -> str:
    """
    Find file path using file_id
    """
    for file in os.listdir(UPLOAD_DIR):
        if file.startswith(file_id):
            return os.path.join(UPLOAD_DIR, file)
    return None


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from PDF using PyMuPDF
    """
    text = ""

    try:
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text()

        return text

    except Exception as e:
        return f"Error reading PDF: {str(e)}"


def read_text_file(file_path: str) -> str:
    """
    Read plain text file
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"


def extract_text(file_id: str) -> Union[str, List[dict]]:
    """
    Extract content based on file type
    - PDF/TXT → returns text (str)
    - Audio/Video → returns segments with timestamps (list)
    """
    file_path = get_file_path(file_id)

    if not file_path:
        return "File not found"

    extension = file_path.split(".")[-1].lower()

    # 📄 PDF
    if extension == "pdf":
        return extract_text_from_pdf(file_path)

    # 📄 TEXT FILE
    elif extension in ["txt"]:
        return read_text_file(file_path)

    # 🎧 AUDIO / VIDEO
    elif extension in ["mp3", "wav", "mp4", "mkv"]:
        segments = transcribe_audio(file_path)

        if isinstance(segments, dict):  # error case
            return "Error in transcription"

        return segments  # ✅ return structured data

    else:
        return "Unsupported file type"


def split_text(text: str, chunk_size: int = 500) -> List[str]:
    """
    Split plain text into chunks
    """
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])

    return chunks


def split_segments_with_timestamps(segments, chunk_size: int = 3):
    """
    Convert transcription segments into chunks with timestamps
    """
    chunks = []

    for i in range(0, len(segments), chunk_size):
        group = segments[i:i + chunk_size]

        combined_text = " ".join([s["text"] for s in group])
        start_time = group[0]["start"]

        chunks.append({
            "text": combined_text,
            "timestamp": start_time
        })

    return chunks