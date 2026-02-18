import spacy
import re
import pandas as pd
import os
from spacy.pipeline import EntityRuler
from pypdf import PdfReader


# ==========================================
# 1. SKILLS CONSTANTS
# ==========================================
SKILLS_LIST = [
    "Python", "Java", "C++", "JavaScript", "TypeScript", "React", "Angular", "Vue",
    "Node.js", "Django", "Flask", "FastAPI", "SQL", "NoSQL", "PostgreSQL", "MongoDB",
    "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "Git", "Jenkins",
    "Machine Learning", "Deep Learning", "Data Science", "NLP", "TensorFlow", "PyTorch",
    "Pandas", "NumPy", "Scikit-Learn", "Tableau", "Power BI", "Excel"
]

# ==========================================
# 2. PARSER CLASS
# ==========================================
class ResumeParser:
    def __init__(self, input_data):
        self.nlp = self._load_model()

        # Handle File vs Text
        if os.path.exists(str(input_data)) and str(input_data).endswith(".pdf"):
            self.text = self._extract_text_from_file(input_data)
        else:
            self.text = input_data

        # Pre-process text for section extraction
        self.lines = [line.strip() for line in self.text.split('\n') if line.strip()]
        self.clean_text = " ".join(self.lines)
        self.doc = self.nlp(self.clean_text)

    def _load_model(self):
        # In serverless/Vercel, we assume the model is installed via requirements.txt
        # using the direct URL to the wheel.
        try:
            nlp = spacy.load("en_core_web_sm")
        except OSError:
            # Fallback purely for local dev if model missing, though requirements.txt should handle it
            print("Model not found. Attempting to download...")
            from spacy.cli import download
            download("en_core_web_sm")
            nlp = spacy.load("en_core_web_sm")

        if "entity_ruler" not in nlp.pipe_names:
            ruler = nlp.add_pipe("entity_ruler", before="ner")
            patterns = [{"label": "SKILL", "pattern": [{"LOWER": s.lower()}]} for s in SKILLS_LIST]
            ruler.add_patterns(patterns)
        return nlp

    def _extract_text_from_file(self, file_path):
        try:
            reader = PdfReader(file_path)
            # Use newline to preserve structure
            return "\n".join([page.extract_text() for page in reader.pages])
        except Exception:
            return ""

    # --- SECTION EXTRACTION LOGIC ---
    def extract_sections(self):
        """
        Scans for headers like 'Experience', 'Education', 'Projects'
        and captures the text following them.
        """
        sections = {
            "Experience": [],
            "Projects": [],
            "Education": []
        }

        # Keywords that signal a section start
        # We use strict matching (must appear at start of line, usually Uppercase)
        header_patterns = {
            "Experience": [r'experience', r'work history', r'employment', r'professional background'],
            "Projects": [r'projects', r'academic projects', r'personal projects', r'key projects'],
            "Education": [r'education', r'academic qualification', r'qualifications'],
            # Sections to explicitly ignore (prevents them from merging into Projects)
            "Ignored": [r'extracurricular', r'activities', r'achievements', r'certifications', r'interests', r'skills', r'languages', r'references']
        }

        current_section = None

        for line in self.lines:
            # Check if this line is a header
            is_header = False
            lower_line = line.lower()

            for section_name, patterns in header_patterns.items():
                if any(re.search(p, lower_line) for p in patterns):
                    # Heuristic: Headers are usually short (e.g., "Work Experience" vs "I have work experience in...")
                    if len(line.split()) < 5:
                        current_section = section_name
                        is_header = True
                        break

            if is_header:
                continue  # Skip the header line itself

            # If we are inside a recognized section, append the line
            if current_section and current_section in sections:
                # LINE MERGING LOGIC
                # Expanded Regex for common bullet points including:
                # - Standard: -, *, •
                # - Unicode: ● (Black Circle), ○, ▪, ▫, ➢, →, >
                # - Numbered: 1., 1), a., a)
                is_bullet = re.match(r'^[\s]*[\-\*•●○▪▫➢→>\d\.\)]+', line)
                
                if not sections[current_section]:
                    sections[current_section].append(line)
                    continue

                if is_bullet:
                    sections[current_section].append(line)
                else:
                    # HEURISTIC: When to merge vs. Start new line
                    # Merge if:
                    # 1. Line starts with lowercase (strong indicator of sentence continuation)
                    # 2. Previous line explicitly signals continuation (ends with , or "and", "with", etc.)
                    
                    prev_line = sections[current_section][-1]
                    starts_lower = line[0].islower()
                    prev_signals_continuation = re.search(r'(,|and|with|to|for|of|in|on|at|by|from|&)\s*$', prev_line, re.IGNORECASE)

                    if starts_lower or prev_signals_continuation:
                        sections[current_section][-1] += " " + line
                    else:
                        # Otherwise, assume it's a new block (e.g., a "Side Heading" like "Project Alpha")
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
            "Experience": sections["Experience"],  # Returns a list of text lines
            "Projects": sections["Projects"]  # Returns a list of text lines
        }