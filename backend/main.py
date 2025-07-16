# backend/main.py

import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from document_handler import process_uploaded_file
from llama_chain import answer_question

app = FastAPI()

# Allow frontend (e.g., React) to call the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ✅ Model for chat input
class ChatRequest(BaseModel):
    question: str

# Route for uploading files
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        # Save file locally
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Process the uploaded file into vectorstore
        process_uploaded_file(file_path)

        return {"status": "success", "filename": file.filename}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# ✅ Route for asking questions from frontend (expects JSON)
@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        response = answer_question(req.question)
        return {"answer": response}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
