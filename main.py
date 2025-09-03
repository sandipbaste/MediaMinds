from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
from typing import Optional

# Try to import modules with fallbacks
try:
    from pdf_processor import process_pdf
except ImportError:
    # Fallback to alternative PDF processing
    import pdfplumber
    import re
    
    def process_pdf(file_path: str) -> str:
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")
        text = re.sub(r'\s+', ' ', text)
        return text

try:
    from text_generator import generate_explanation
except ImportError:
    def generate_explanation(text: str, prompt: str) -> str:
        return f"Explanation: {text[:500]}... [Text generator not available]"

try:
    from audio_generator import text_to_speech
except ImportError:
    def text_to_speech(text: str, file_id: str) -> str:
        # Create a dummy audio file
        audio_path = f"static/audio/{file_id}.mp3"
        os.makedirs(os.path.dirname(audio_path), exist_ok=True)
        with open(audio_path, "w") as f:
            f.write("dummy audio file")
        return audio_path

try:
    from video_generator import create_video
except ImportError:
    def create_video(audio_path: str, text: str, file_id: str) -> str:
        # Create a dummy video file
        video_path = f"static/videos/{file_id}.mp4"
        os.makedirs(os.path.dirname(video_path), exist_ok=True)
        with open(video_path, "w") as f:
            f.write("dummy video file")
        return video_path

app = FastAPI(title="PDF Explainer API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create directories if they don't exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("static/audio", exist_ok=True)
os.makedirs("static/videos", exist_ok=True)
os.makedirs("static/temp", exist_ok=True)

@app.post("/process-pdf/")
async def process_pdf_endpoint(
    file: UploadFile = File(...),
    prompt: Optional[str] = "Explain this content in simple terms with practical examples"
):
    try:
        # Save uploaded file
        file_id = str(uuid.uuid4())
        file_path = os.path.join("uploads", f"{file_id}_{file.filename}")
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Process PDF
        text_content = process_pdf(file_path)
        
        # Generate explanation
        explanation = generate_explanation(text_content, prompt)
        
        # Generate audio
        audio_path = text_to_speech(explanation, file_id)
        
        # Generate video
        video_path = create_video(audio_path, explanation, file_id)
        
        return {
            "file_id": file_id,
            "explanation": explanation,
            "audio_url": f"/audio/{file_id}.mp3",
            "video_url": f"/video/{file_id}.mp4"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/audio/{file_id}")
async def get_audio(file_id: str):
    audio_path = f"static/audio/{file_id}.mp3"
    if os.path.exists(audio_path):
        return FileResponse(audio_path, media_type="audio/mpeg")
    raise HTTPException(status_code=404, detail="Audio not found")

@app.get("/video/{file_id}")
async def get_video(file_id: str):
    video_path = f"static/videos/{file_id}.mp4"
    if os.path.exists(video_path):
        return FileResponse(video_path, media_type="video/mp4")
    raise HTTPException(status_code=404, detail="Video not found")

@app.get("/")
async def root():
    return {"message": "PDF Explainer API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)