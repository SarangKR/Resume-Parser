import io
import os
import re
import smtplib
import json
import traceback
from typing import Optional, List, Dict, Any
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from fastapi import FastAPI, UploadFile, File, HTTPException, Form, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Third-party imports
import spacy
from spacy.pipeline import EntityRuler
from pypdf import PdfReader
import pandas as pd # Kept if needed, though mostly unused in current parser logic

# ==========================================
# 1. CONSTANTS & CONFIG
# ==========================================
SKILLS_LIST = [
    "Python", "Java", "C++", "JavaScript", "TypeScript", "React", "Angular", "Vue",
    "Node.js", "Django", "Flask", "FastAPI", "SQL", "NoSQL", "PostgreSQL", "MongoDB",
    "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "Git", "Jenkins",
    "Machine Learning", "Deep Learning", "Data Science", "NLP", "TensorFlow", "PyTorch",
    "Pandas", "NumPy", "Scikit-Learn", "Tableau", "Power BI", "Excel"
]

# ==========================================
# 2. SERVICES
# ==========================================
class EmailService:
    def __init__(self):
        # In a real scenario, these would come from environment variables
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = os.getenv("SENDER_EMAIL", "noreply@talentscout.ai")
        self.sender_password = os.getenv("SENDER_PASSWORD", "mock_password")
        self.mock_mode = True # Set to False if you configure real credentials

    def send_shortlist_email(self, recipient_email, candidate_data, match_score, matching_skills):
        subject = f"Candidate Shortlisted: Match Score {match_score}%"
        
        body = f"""
        <html>
        <body>
            <h2>Candidate Shortlisted</h2>
            <p>A candidate has matched your job requirements.</p>
            
            <h3>Match Details</h3>
            <ul>
                <li><strong>Match Score:</strong> {match_score}%</li>
                <li><strong>Matching Skills:</strong> {', '.join(matching_skills)}</li>
            </ul>
            
            <h3>Candidate Details</h3>
            <ul>
                <li><strong>Name:</strong> {candidate_data.get('Name', 'N/A')}</li>
                <li><strong>Email:</strong> {candidate_data.get('Email', 'N/A')}</li>
                <li><strong>Phone:</strong> {candidate_data.get('Phone', 'N/A')}</li>
            </ul>
            
            <p><em>This is an automated message from TalentScout AI.</em></p>
        </body>
        </html>
        """

        if self.mock_mode or not recipient_email:
            print(f"\n[MOCK EMAIL SERVICE]\nTo: {recipient_email}\nSubject: {subject}\nBody Summary: Candidate matched with {match_score}% score.\n")
            return True

        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'html'))

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
            server.quit()
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False

class ResumeParser:
    def __init__(self, input_data):
        self.nlp = self._load_model()

        # Handle File Path vs Stream vs Text
        if isinstance(input_data, str) and os.path.exists(input_data) and input_data.endswith(".pdf"):
            self.text = self._extract_text_from_file(input_data)
        elif hasattr(input_data, 'read'): # File-like object (stream)
            self.text = self._extract_text_from_file(input_data)
        else:
            self.text = input_data

        # Pre-process text for section extraction
        self.lines = [line.strip() for line in self.text.split('\n') if line.strip()]
        self.clean_text = " ".join(self.lines)
        self.doc = self.nlp(self.clean_text)

    def _load_model(self):
        try:
            import en_core_web_sm
            nlp = en_core_web_sm.load()
        except ImportError:
            # Fallback for local development if the module isn't found but 'en_core_web_sm' is linked
            try:
                nlp = spacy.load("en_core_web_sm")
            except Exception:
                # Absolute fallback if model is missing (should not happen if requirements are correct)
                nlp = spacy.blank("en")
        
        if "entity_ruler" not in nlp.pipe_names:
            ruler = nlp.add_pipe("entity_ruler", before="ner")
            patterns = [{"label": "SKILL", "pattern": [{"LOWER": s.lower()}]} for s in SKILLS_LIST]
            ruler.add_patterns(patterns)
        return nlp

    def _extract_text_from_file(self, file_source):
        try:
            reader = PdfReader(file_source)
            # Use newline to preserve structure
            return "\n".join([page.extract_text() for page in reader.pages])
        except Exception:
            return ""

    # --- SECTION EXTRACTION LOGIC ---
    def extract_sections(self):
        sections = {
            "Experience": [],
            "Projects": [],
            "Education": []
        }

        # Keywords that signal a section start
        header_patterns = {
            "Experience": [r'experience', r'work history', r'employment', r'professional background'],
            "Projects": [r'projects', r'academic projects', r'personal projects', r'key projects'],
            "Education": [r'education', r'academic qualification', r'qualifications'],
            # Sections to explicitly ignore
            "Ignored": [r'extracurricular', r'activities', r'achievements', r'certifications', r'interests', r'skills', r'languages', r'references']
        }

        current_section = None

        for line in self.lines:
            # Check if this line is a header
            is_header = False
            lower_line = line.lower()

            for section_name, patterns in header_patterns.items():
                if any(re.search(p, lower_line) for p in patterns):
                    # Heuristic: Headers are usually short
                    if len(line.split()) < 5:
                        current_section = section_name
                        is_header = True
                        break

            if is_header:
                continue  # Skip the header line itself

            # If we are inside a recognized section, append the line
            if current_section and current_section in sections:
                is_bullet = re.match(r'^[\s]*[\-\*•●○▪▫➢→>\d\.\)]+', line)
                
                if not sections[current_section]:
                    sections[current_section].append(line)
                    continue

                if is_bullet:
                    sections[current_section].append(line)
                else:
                    prev_line = sections[current_section][-1]
                    starts_lower = line[0].islower()
                    prev_signals_continuation = re.search(r'(,|and|with|to|for|of|in|on|at|by|from|&)\s*$', prev_line, re.IGNORECASE)

                    if starts_lower or prev_signals_continuation:
                        sections[current_section][-1] += " " + line
                    else:
                        sections[current_section].append(line)

        return sections

    def extract_name(self):
        forbidden_words = ["resume", "curriculum", "vitae", "cv", "data", "analyst", "scientist", "manager",
                           "developer", "engineer"]

        # Strategy 1: Spacy
        for ent in self.doc.ents:
            if ent.label_ == "PERSON":
                name = ent.text.strip()
                if (len(name.split()) >= 2 and
                        not any(char.isdigit() for char in name) and
                        not any(w in name.lower() for w in forbidden_words)):
                    return name

        # Strategy 2: Fallback (Top of file)
        for line in self.lines[:10]:
            clean_line = line.strip()
            if (2 <= len(clean_line.split()) <= 4 and
                    clean_line.replace(" ", "").isalpha() and
                    clean_line[0].isupper() and
                    not any(w in clean_line.lower() for w in forbidden_words)):
                return clean_line
        return None

    def extract_contact_info(self):
        email = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', self.text)
        phone = re.search(r'(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}', self.text)
        return {
            "email": email.group() if email else None,
            "phone": phone.group() if phone else None
        }

    def parse(self):
        contact = self.extract_contact_info()
        skills = sorted(list(set([ent.text for ent in self.doc.ents if ent.label_ == "SKILL"])))
        sections = self.extract_sections()

        return {
            "Name": self.extract_name(),
            "Email": contact["email"],
            "Phone": contact["phone"],
            "Skills": skills,
            "Experience": sections["Experience"],
            "Projects": sections["Projects"]
        }

# ==========================================
# 3. FASTAPI APP
# ==========================================
app = FastAPI(title="Resume Parser API")
router = APIRouter()
email_service = EmailService()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    
    try:
        # Read file into memory
        file_content = await file.read()
        file_stream = io.BytesIO(file_content)
            
        # Initialize parser with file stream
        parser = ResumeParser(file_stream)
        data = parser.parse()
        
        # Calculate Logic
        extracted_skills = [s.lower() for s in data.get("Skills", [])]
        completeness = 0
        if data.get('Email'): completeness += 40
        if data.get('Phone'): completeness += 40
        if len(extracted_skills) > 0: completeness += 20
        
        # Job Matching
        match_details = None
        is_shortlisted = False
        
        if required_skills:
            req_skill_list = [s.strip().lower() for s in required_skills.split(",") if s.strip()]
            if req_skill_list:
                matching_skills = [s for s in req_skill_list if s in extracted_skills]
                match_percentage = int((len(matching_skills) / len(req_skill_list)) * 100)
                
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
        print(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={"detail": f"Internal Server Error: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"}
        )

# Mount Routes
app.include_router(router)
app.include_router(router, prefix="/api")

# Global Exception Handler (optional but good for safety)
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Unhandled Server Error: {str(exc)}\n\nTraceback:\n{traceback.format_exc()}"}
    )
