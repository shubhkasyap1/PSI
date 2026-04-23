from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.llm_service import ask_llm
from app.services.vector_service import get_relevant_chunks

router = APIRouter()


class ChatRequest(BaseModel):
    file_id: str
    question: str


@router.post("/")
def chat(req: ChatRequest):
    try:
        # -----------------------------
        # Retrieve relevant chunks
        # -----------------------------
        context_chunks = get_relevant_chunks(
            req.file_id,
            req.question
        )

        if not context_chunks:
            return {
                "question": req.question,
                "answer": "No relevant context found for this file.",
                "timestamp": None,
                "context_used": []
            }

        # -----------------------------
        # Build context text for LLM
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

        # -----------------------------
        # Ask LLM
        # -----------------------------
        answer = ask_llm(
            req.question,
            context
        )

        # -----------------------------
        # Timestamp support
        # -----------------------------
        top_result = context_chunks[0]

        if isinstance(top_result, dict):
            timestamp = top_result.get("timestamp")
        else:
            timestamp = None

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