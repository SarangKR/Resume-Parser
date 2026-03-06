# TalentScout - AI Resume Parser

A modern web application that parses resumes (PDF) and extracts key information using lightweight regex-based natural language processing optimized for serverless environments.

## Features
- **Intelligent Parsing**: Extracts details like contact info, education, work experience, projects, and skills.
- **Job Matching Feature**: Input job requirements and a recruiter email to automatically shortlist candidates based on a match percentage.
- **Intermediate Candidate View**: View a summarized list of all parsed candidates before diving into individual details to keep your screen organized.
- **Interactive Sidebar Progress Bar**: Real-time visual tracking of your workflow through file upload, AI analysis, and data review stages.
- **Advanced UI/UX**: Clean dashboard with section-level "Read More/Show Less" toggles for extensive work history and projects.

## Architecture
- **Backend**: Python (FastAPI/Serverless) - optimized for Vercel deployment with pure regex-based feature extraction (removed heavy dependencies like Spacy to meet Lambda limits).
- **Frontend**: React (18), Vite, TailwindCSS, Framer Motion, and Lucide React.
- **Hosting**: Pre-configured for seamless Vercel deployment.

## Prerequisites
1. **Node.js 18+** 
2. **Python 3.9+**

## Setup & Running Locally

Navigate to the `frontend` directory:
```bash
cd frontend
```

### 1. Install Dependencies
Install Node modules:
```bash
npm install
```

Install Python dependencies for the backend API:
```bash
pip install -r api/requirements.txt
```

### 2. Run the Application
Start the frontend development server:
```bash
npm run dev
```

The UI will be available at `http://localhost:5173`. 
*(Note: Refer to `vite.config.js` or backend scripts to see how the Python API is locally served alongside Vite).*

## Usage
1. Open the application in your browser.
2. Drag and drop PDF resumes into the upload zone.
3. Track your progress dynamically on the left sidebar.
4. Review the parsed candidates in the Intermediate View and select individuals to see their detailed dashboards.
5. Provide job requirements in the Job Matching section to automatically filter, shortlist, and alert recruiters.

## Vercel Deployment
This repository is tailored for easy Vercel deployment. The frontend builds statically, and the `frontend/api` folder is automatically handled by Vercel's Python runtime to act as serverless functions.
