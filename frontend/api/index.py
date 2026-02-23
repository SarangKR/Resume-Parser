import os
import json
import traceback
from typing import Optional

# Standard library imports that are safe
import io
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Try to import FastAPI - if this fails, we really can't do anything, but Vercel logs should show it.
try:
    from fastapi import FastAPI, UploadFile, File, HTTPException, Form, APIRouter, Request
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
except ImportError:
    # This will cause a 500 error on Vercel, but we can't emit JSON without FastAPI/Starlette
    raise

# Initialize App immediately so Vercel can find it
app = FastAPI(title="Resume Parser API")
router = APIRouter()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# 1. LAZY SERVICES
# ==========================================
# We define classes but import heavy dependencies inside methods

class EmailService:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = os.getenv("SENDER_EMAIL", "noreply@talentscout.ai")
        self.sender_password = os.getenv("SENDER_PASSWORD", "mock_password")
        self.mock_mode = True

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
        </body>
        </html>
        """
        if self.mock_mode or not recipient_email:
            print(f"[MOCK EMAIL] To: {recipient_email}, Score: {match_score}")
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

# ==========================================
# 2. ROUTES
# ==========================================

@router.get("/")
async def root():
    return {"message": "Resume Parser API is running", "status": "healthy"}

@router.post("/parse")
async def parse_resume(
    file: UploadFile = File(...),
    required_skills: Optional[str] = Form(None),
    recruiter_email: Optional[str] = Form(None)
):
    try:
        # 1. Lazy Import dependencies here to catch errors
        from pypdf import PdfReader
        # pandas is not strictly used in the logic below, so we can skip it or import if needed
    except ImportError as e:
        return JSONResponse(
            status_code=500,
            content={"detail": f"Dependency Error: {str(e)}. Please check requirements.txt."}
        )

    # 2. Define ResumeParser logic inline or lazily
    # We move the ResumeParser class logic here or keep it as a helper that imports things internally.
    # To keep it clean, let's define the class here or simply use functions.
    # Let's use a local class to keep imports scoped to this request if we want, 
    # but strictly speaking, once imported, they are cached.
    # But this try/except block handles the *first* import failure.

    class ResumeParser:
        SKILLS_LIST = [
            "Python", "Java", "C++", "JavaScript", "TypeScript", "React", "Angular", "Vue",
            "Node.js", "Django", "Flask", "FastAPI", "SQL", "NoSQL", "PostgreSQL", "MongoDB",
            "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "Git", "Jenkins",
            "Machine Learning", "Deep Learning", "Data Science", "NLP", "TensorFlow", "PyTorch",
            "Pandas", "NumPy", "Scikit-Learn", "Tableau", "Power BI", "Excel"
        ]

        def __init__(self, input_data):
            # We bypass model loading for size limits
            self.nlp = None
            if isinstance(input_data, str) and os.path.exists(input_data) and input_data.endswith(".pdf"):
                self.text = self._extract_text_from_file(input_data)
            elif hasattr(input_data, 'read'):
                self.text = self._extract_text_from_file(input_data)
            else:
                self.text = str(input_data) if input_data is not None else ""
            
            self.lines = [line.strip() for line in self.text.split('\n') if line.strip()]
            self.clean_text = " ".join(self.lines)
            # Spacy doc initialization removed to save bundle size

        def _load_model(self):
            return None

        def _extract_text_from_file(self, file_source):
            try:
                reader = PdfReader(file_source)
                return "\n".join([page.extract_text() for page in reader.pages])
            except Exception:
                return ""

        def extract_sections(self):
            sections = {"Experience": [], "Projects": [], "Education": []}
            header_patterns = {
                "Experience": [r'experience', r'work history', r'employment'],
                "Projects": [r'projects', r'academic projects'],
                "Education": [r'education', r'academic qualification'],
                "Ignored": [r'extracurricular', r'activities', r'interests', r'skills', r'languages']
            }
            current_section = None
            for line in self.lines:
                is_header = False
                lower_line = line.lower()
                for section_name, patterns in header_patterns.items():
                    if any(re.search(p, lower_line) for p in patterns):
                        if len(line.split()) < 5:
                            current_section = section_name
                            is_header = True
                            break
                if is_header: continue
                if current_section and current_section in sections:
                    sections[current_section].append(line)
            return sections

        def extract_name(self):
            # Lightweight Fallback Strategy (in case the heavy Spacy model is omitted)
            for line in self.lines[:5]:
                line = line.strip()
                # Match basic 2-4 word names (e.g., "John Doe", "Jane Smith Johnson")
                if 2 <= len(line.split()) <= 4 and re.match(r'^[A-Z][A-Za-z]+ [A-Z][A-Za-z]+', line):
                    if not any(word in line.lower() for word in ["resume", "curriculum", "vitae", "summary", "profile", "contact"]):
                        return line
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
            
            # Pure Regex Skills Extraction
            extracted_skills = set()
            clean_text_lower = self.clean_text.lower()
            
            for skill in self.SKILLS_LIST:
                # Use word boundaries to prevent partial matches (e.g. matching "C" inside "React")
                # Handle special characters in skills like C++ or Node.js
                escaped_skill = re.escape(skill.lower())
                pattern = r'\b' + escaped_skill + r'(?:\b|(?=\W|$))'
                if re.search(pattern, clean_text_lower):
                    extracted_skills.add(skill)
                    
            skills = sorted(list(extracted_skills))
            sections = self.extract_sections()
            
            return {
                "Name": self.extract_name(),
                "Email": contact["email"],
                "Phone": contact["phone"],
                "Skills": skills,
                "Experience": sections["Experience"],
                "Projects": sections["Projects"]
            }

    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        file_content = await file.read()
        file_stream = io.BytesIO(file_content)
        parser = ResumeParser(file_stream)
        data = parser.parse()
        
        extracted_skills = [s.lower() for s in data.get("Skills", [])]
        completeness = 0
        if data.get('Email'): completeness += 40
        if data.get('Phone'): completeness += 40
        if len(extracted_skills) > 0: completeness += 20
        
        match_details = None
        
        if required_skills:
            req_skill_list = [s.strip().lower() for s in required_skills.split(",") if s.strip()]
            if req_skill_list:
                matching_skills = [s for s in req_skill_list if s in extracted_skills]
                match_percentage = int((len(matching_skills) / len(req_skill_list)) * 100)
                
                email_service = EmailService()
                email_sent = False
                is_shortlisted = False
                if match_percentage >= 50:
                    is_shortlisted = True
                    if recruiter_email:
                        email_sent = email_service.send_shortlist_email(
                            recruiter_email, data, match_percentage, [s.title() for s in matching_skills]
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
            content={"detail": f"Runtime Error: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"}
        )

# Mount Routes
app.include_router(router)
app.include_router(router, prefix="/api")
