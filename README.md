````md id="readme-final"
# AI-Powered Document & Multimedia Q&A Web Application

![Tests](https://github.com/shubhkasyap1/PSI/actions/workflows/tests.yml/badge.svg)
![Coverage](https://codecov.io/gh/shubhkasyap1/PSI/branch/main/graph/badge.svg?token=a61b13c5-0f5f-440a-97b5-0ae6e54d294f)

An AI-powered system to upload PDFs, audio, and video, then chat, summarize, and retrieve timestamps.

# 🚀 Features

## 📄 File Upload Support
Upload:

- PDF Documents
- Audio Files (`mp3`, `wav`)
- Video Files (`mp4`, `mkv`)

---

## 🤖 AI Chatbot

Ask natural language questions based on uploaded files.

Examples:

- What is this document about?
- Summarize chapter 2
- What did the speaker say about AI?
- Where is pricing discussed?

---

## 📝 Smart Summary

Generate summaries for:

- PDFs
- Audio transcripts
- Video transcripts

---

## ⏱ Timestamp Extraction

For audio/video files, the chatbot returns relevant timestamps.

Example:

- Topic found at `01:42`

---

## ▶ Play Relevant Segment

Click play button to jump directly to relevant timestamp in uploaded media.

---

## 🔎 Vector Search

Uses semantic search with FAISS + embeddings for accurate answers.

---

## 🧪 Automated Testing

- Pytest based test suite
- High coverage backend testing

---

## 🐳 Dockerized Deployment

Supports:

- Backend container
- Frontend container
- Docker Compose multi-service setup

---

# 🛠 Tech Stack

## Frontend

- React
- Vite
- Tailwind CSS v4
- Axios

## Backend

- FastAPI
- Python

## AI / ML

- Groq API
- Gemini API
- Whisper
- Sentence Transformers
- FAISS

## Database

- MongoDB

## DevOps

- Docker
- Docker Compose
- GitHub Actions (CI/CD Ready)

---

# 📁 Project Structure

```bash
ai-doc-qa-app/
│
├── client/                 # React Frontend
├── server/                 # FastAPI Backend
├── docker/                 # Dockerfiles
├── docker-compose.yml
└── README.md
````

---

# ⚙️ Local Setup

## 1️⃣ Clone Repository

```bash
git clone <your-repo-url>
cd ai-doc-qa-app
```

---

## 2️⃣ Backend Setup

```bash
cd server
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend runs on:

```text
http://127.0.0.1:8000
```

Swagger Docs:

```text
http://127.0.0.1:8000/docs
```

---

## 3️⃣ Frontend Setup

```bash
cd client
npm install
npm run dev
```

Frontend runs on:

```text
http://localhost:5173
```

---

# 🐳 Docker Setup

## Run Full Project

```bash
docker compose up --build
```

Frontend:

```text
http://localhost:3000
```

Backend:

```text
http://localhost:8000/docs
```

---

# 🔐 Environment Variables

Create:

```text
server/.env
```

```env
GROQ_API_KEY=your_key
GEMINI_API_KEY=your_key
MONGO_URI=your_mongodb_uri
```

---

# 📡 API Endpoints

## Upload File

```http
POST /upload/
```

Returns:

```json
{
  "file_id": "123abc"
}
```

---

## Chat with File

```http
POST /chat/
```

Body:

```json
{
  "file_id": "123abc",
  "question": "What is this file about?"
}
```

---

## Generate Summary

```http
POST /summary/
```

Body:

```json
{
  "file_id": "123abc"
}
```

---

# 🧪 Run Tests

```bash
pytest -v
```

Coverage:

```bash
pytest --cov=app --cov-report=term-missing
```

---

# 🎯 Assignment Requirements Completed

## Backend

* FastAPI backend
* AI chatbot
* Audio/video transcription
* MongoDB integration
* Dockerfile
* Testing
* CI/CD ready

## Frontend

* React UI
* Upload interface
* Chatbot UI
* Summary UI
* Timestamp display
* Play relevant media section

## Infrastructure

* Docker Compose
* Multi-container architecture

---

# 🔥 Bonus Implemented

* FAISS Vector Search
* Semantic Retrieval
* Media Timestamp Navigation

---

# 📸 Demo

Add screenshots or video link here.

```text
https://drive.google.com/drive/folders/1xP4X2en5KXSBo8YMbcQaRtXLeQAh6CMI?usp=sharing
```

---

# 👨‍💻 Author

Shubham Kumar

---

```
```
