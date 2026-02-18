# TalentScout - AI Resume Parser

A modern web application that parses resumes (PDF) and extracts key information using NLP.

## Architecture
- **Backend**: FastAPI (Python)
- **Frontend**: React + TailwindCSS (Vite)
- **NLP**: Spacy

## Prerequisites
1. **Python 3.9+**
2. **Node.js 18+** (Required for Frontend)

## Setup & Running

### 1. Backend
Navigate to the `backend` directory and install dependencies:
```bash
cd backend
pip install -r requirements.txt
```
*Note: Make sure to download the Spacy model if not already present:*
```bash
python -m spacy download en_core_web_sm
```

Run the server:
```bash
python -m uvicorn main:app --reload
```
The API will be available at `http://localhost:8000`.

### 2. Frontend
Navigate to the `frontend` directory:
```bash
cd frontend
```

Install dependencies (requires Node.js):
```bash
npm install
```

Run the development server:
```bash
npm run dev
```
The UI will be available at `http://localhost:5173`.

## Usage
1. Open the frontend in your browser.
2. Drag and drop a PDF resume.
3. View the extracted details and confidence score.
