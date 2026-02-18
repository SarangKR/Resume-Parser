from fastapi import FastAPI, UploadFile, File, HTTPException, Form, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import shutil
import tempfile
import os
from typing import Optional
try:
    from .resume_parser import ResumeParser
    from .email_service import EmailService
except ImportError:
    from resume_parser import ResumeParser
    from email_service import EmailService

app = FastAPI(title="Resume Parser API")
router = APIRouter()

email_service = EmailService()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@router.get("/")
async def root():
    return {"message": "Resume Parser API is running"}

@router.post("/parse")
async def parse_resume(
    file: UploadFile = File(...),
    required_skills: Optional[str] = Form(None),
    recruiter_email: Optional[str] = Form(None)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    # Save uploaded file temporarily using tempfile
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            shutil.copyfileobj(file.file, tmp_file)
            temp_filename = tmp_file.name
            
        # Initialize parser with file path
        parser = ResumeParser(temp_filename)
        data = parser.parse()
        
        # Calculate Base Confidence (Data Completeness)
        extracted_skills = [s.lower() for s in data.get("Skills", [])]
        completeness = 0
        if data.get('Email'): completeness += 40
        if data.get('Phone'): completeness += 40
        if len(extracted_skills) > 0: completeness += 20
        
        # Calculate Job Match Score (if requirements provided)
        match_details = None
        is_shortlisted = False
        
        if required_skills:
            req_skill_list = [s.strip().lower() for s in required_skills.split(",") if s.strip()]
            if req_skill_list:
                matching_skills = [s for s in req_skill_list if s in extracted_skills]
                match_percentage = int((len(matching_skills) / len(req_skill_list)) * 100)
                
                # Shortlist Criteria: > 50% match
                email_sent = False
                if match_percentage >= 50:
                    is_shortlisted = True
                    if recruiter_email:
                        email_sent = email_service.send_shortlist_email(
                            recruiter_email, 
                            data, 
                            match_percentage, 
                            [s.title() for s in matching_skills]
                        )
                
                match_details = {
                    "score": match_percentage,
                    "matching_skills": [s.title() for s in matching_skills],
                    "missing_skills": [s.title() for s in req_skill_list if s not in extracted_skills],
                    "is_shortlisted": is_shortlisted,
                    "email_sent": email_sent,
                    "recruiter_email": recruiter_email
                }
        
        return {
            "success": True,
            "data": data,
            "meta": {
                "confidence_score": completeness,
                "skills_count": len(extracted_skills),
                "job_match": match_details
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        # Clean up temp file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

# Mount the router at both root and /api for compatibility
app.include_router(router)
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
