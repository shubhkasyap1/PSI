from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.llm_service import ask_llm
from app.services.vector_service import get_relevant_chunks
from app.services.file_service import extract_text

router = APIRouter()


class ChatRequest(BaseModel):
    file_id: str
    question: str


@router.post("/")
def chat(req: ChatRequest):
    try:
        context_chunks = get_relevant_chunks(
            req.file_id,
            req.question
        )

        # -----------------------------
        # If no vector results found
        # fallback to full text
        # -----------------------------
        if not context_chunks:

            file_data = extract_text(req.file_id)

            if isinstance(file_data, str):
                answer = ask_llm(
                    req.question,
                    file_data[:4000]
                )

                return {
                    "question": req.question,
                    "answer": answer,
                    "timestamp": None,
                    "context_used": []
                }

            return {
                "question": req.question,
                "answer": "No useful content found.",
                "timestamp": None,
                "context_used": []
            }

        # -----------------------------
        # Build context
        # -----------------------------
        context_texts = []

        for chunk in context_chunks:
            if isinstance(chunk, dict):
                context_texts.append(
                    chunk.get("text", "")
                )
            else:
                context_texts.append(str(chunk))

        context = "\n".join(context_texts)

        answer = ask_llm(
            req.question,
            context
        )

        top_result = context_chunks[0]

        timestamp = (
            top_result.get("timestamp")
            if isinstance(top_result, dict)
            else None
        )

        return {
            "question": req.question,
            "answer": answer,
            "timestamp": timestamp,
            "context_used": context_chunks
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )