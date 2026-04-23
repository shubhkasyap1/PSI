from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil
from uuid import uuid4

from app.services.vector_service import build_vector_index  # ✅ ADD THIS

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Generate unique filename
        file_id = str(uuid4())
        file_extension = file.filename.split(".")[-1]
        new_filename = f"{file_id}.{file_extension}"

        file_path = os.path.join(UPLOAD_DIR, new_filename)

        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 🔥 BUILD VECTOR INDEX (THIS WAS MISSING)
        result = build_vector_index(file_id)
        print("INDEX RESULT:", result)

        return {
            "file_id": file_id,
            "original_filename": file.filename,
            "stored_filename": new_filename,
            "file_path": file_path,
            "content_type": file.content_type
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))