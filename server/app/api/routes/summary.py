from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.llm_service import summarize_text
from app.services.file_service import extract_text

router = APIRouter()


class SummaryRequest(BaseModel):
    file_id: str


@router.post("/")
def summarize(req: SummaryRequest):
    try:
        # Extract content
        data = extract_text(req.file_id)

        if not data:
            return {
                "error": "No content found for this file."
            }

        # -----------------------------
        # PDF / TXT
        # -----------------------------
        if isinstance(data, str):
            if data.startswith("Error"):
                return {"error": data}

            text = data

        # -----------------------------
        # Audio / Video transcript list
        # -----------------------------
        elif isinstance(data, list):
            text = " ".join(
                seg.get("text", "")
                for seg in data
            )

        else:
            text = str(data)

        # Limit size for LLM
        text = text[:5000]

        # Generate summary
        summary = summarize_text(text)

        return {
            "file_id": req.file_id,
            "summary": summary
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )