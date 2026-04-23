from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.api.routes import upload, chat, summary

app = FastAPI(
    title="AI Document & Multimedia Q&A API",
    version="1.0.0"
)

# ✅ Create folders if not exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("vector_db", exist_ok=True)

# ✅ CORS (required for React frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Serve uploaded files (VERY IMPORTANT for video/audio player)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# ✅ Routes
app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(summary.router, prefix="/summary", tags=["Summary"])


@app.get("/")
def root():
    return {
        "message": "🚀 AI Doc Q&A Backend Running"
    }


# ✅ Health check (useful for deployment)
@app.get("/health")
def health():
    return {"status": "ok"}