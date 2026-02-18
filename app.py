import streamlit as st
import pandas as pd
from pypdf import PdfReader
# Ensure backend is correct
from resume_parser import ResumeParser, refresh_skills_database
import base64

# ==============================================================================
# 1. PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="TalentScout | AI Resume Intelligence",
    page_icon= "C:/Users/krsar/OneDrive/Desktop/Projects/Automatic Resume Parser/TS Logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Backend
refresh_skills_database()

# ==============================================================================
# 2. CUSTOM CSS (Icon Fixes & Polished UI)
# ==============================================================================
st.markdown("""
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
<style>
    /* IMPORT FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* GLOBAL VARIABLES */
    :root {
        --primary-color: #2563EB;
        --bg-color: #F3F4F6;
        --card-bg: #FFFFFF;
        --text-dark: #111827;
        --text-gray: #6B7280;
        --sidebar-bg: #0F172A;
        --sidebar-text: #F1F5F9;
    }

    /* 1. FORCE BACKGROUND COLORS */
    .stApp {
        background-color: var(--bg-color);
    }

    /* 2. TYPOGRAPHY - Applied CAREFULLY to avoid breaking icons */
    /* We exclude 'i', 'span', and specific icon classes from the font override */
    h1, h2, h3, h4, h5, h6, p, div, li, .stMarkdown, .metric-card {
        font-family: 'Inter', sans-serif !important;
        color: var(--text-dark);
    }

    /* HIDE DEFAULT ELEMENTS */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* --- SIDEBAR STYLING --- */
    [data-testid="stSidebar"] {
        background-color: var(--sidebar-bg);
        border-right: 1px solid #1E293B;
    }

    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] div, 
    [data-testid="stSidebar"] label {
        color: var(--sidebar-text) !important;
    }

    /* FIX: SIDEBAR COLLAPSE BUTTON */
    [data-testid="stSidebarCollapseButton"] {
        color: #FFFFFF !important; /* Force white icon */
    }
    [data-testid="stSidebarCollapseButton"] img {
        display: none !important; /* Hide default Streamlit SVG if it interferes */
    }
    /* Ensure the material icon font renders correctly if Streamlit uses it */
    .material-icons {
        font-family: 'Material Icons' !important;
    }

    /* Sidebar Info Box */
    .sidebar-info {
        background-color: #1E293B;
        padding: 12px;
        border-radius: 8px;
        border: 1px solid #334155;
        margin-top: 20px;
    }

    /* --- MAIN CARDS --- */
    .metric-card {
        background-color: var(--card-bg);
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        margin-bottom: 16px;
    }

    .section-header {
        font-size: 14px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: var(--text-gray);
        margin-bottom: 12px;
    }

    .data-label {
        font-size: 12px;
        font-weight: 500;
        color: var(--text-gray);
        margin-bottom: 4px;
    }

    .data-value {
        font-size: 16px;
        font-weight: 600;
        color: var(--text-dark);
        word-break: break-all;
    }

    .skill-chip {
        display: inline-flex;
        align-items: center;
        padding: 4px 12px;
        margin: 4px;
        background-color: #EFF6FF;
        color: #1D4ED8;
        border: 1px solid #DBEAFE;
        border-radius: 9999px;
        font-size: 13px;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
    }

    /* --- UPLOAD BOX: DARK MODE FIX --- */
    [data-testid="stFileUploader"] {
        background-color: #0F172A !important; 
        padding: 30px;
        border-radius: 12px;
        border: 2px dashed #3B82F6;
    }

    /* Target specific text elements inside uploader to be white */
    [data-testid="stFileUploader"] div, 
    [data-testid="stFileUploader"] span, 
    [data-testid="stFileUploader"] small, 
    [data-testid="stFileUploader"] p,
    [data-testid="stFileUploader"] label {
        color: #FFFFFF !important;
    }

    /* Button Styling */
    [data-testid="stFileUploader"] button {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border: 1px solid #FFFFFF !important;
        padding: 8px 16px !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
    }

    /* --- EXPANDER ARROW FIX --- */
    [data-testid="stExpander"] summary svg {
        color: #2563EB !important;
        fill: #2563EB !important;
    }

    [data-testid="stExpander"] summary p {
        color: #2563EB !important;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. ICON LIBRARY
# ==============================================================================
ICONS = {
    "document": """<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" style="width:24px;height:24px;"><path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" /></svg>""",
    "mail": """<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" style="width:20px;height:20px;"><path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75" /></svg>""",
    "phone": """<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" style="width:20px;height:20px;"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 6.75c0 8.284 6.716 15 15 15h2.25a2.25 2.25 0 002.25-2.25v-1.372c0-.516-.351-.966-.852-1.091l-4.423-1.106c-.44-.11-.902.055-1.173.417l-.97 1.293c-.282.376-.769.542-1.21.38a12.035 12.035 0 01-7.143-7.143c-.162-.441.004-.928.38-1.21l1.293-.97c.363-.271.527-.734.417-1.173L6.963 3.102a1.125 1.125 0 00-1.091-.852H4.5A2.25 2.25 0 002.25 4.5v2.25z" /></svg>""",
    "cpu": """<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" style="width:20px;height:20px;"><path stroke-linecap="round" stroke-linejoin="round" d="M8.25 3v1.5M4.5 8.25H3m18 0h-1.5M4.5 15.75H3m18 0h-1.5M8.25 19.5V21M15.75 3v1.5m0 16.5V21m0-18h-1.5m-10.5 0h-1.5m10.5 18h-1.5m-10.5 0h-1.5m10.5 18h-1.5m-10.5 0h-1.5M6.75 6.75h10.5a2.25 2.25 0 012.25 2.25v10.5a2.25 2.25 0 01-2.25 2.25H6.75a2.25 2.25 0 01-2.25-2.25V9a2.25 2.25 0 012.25-2.25z" /></svg>""",
    "chart": """<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" style="width:20px;height:20px;"><path stroke-linecap="round" stroke-linejoin="round" d="M3.75 3v11.25A2.25 2.25 0 006 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0118 16.5h-2.25m-7.5 0h7.5m-7.5 0l-1 3m8.5-3l1 3m0 0l.5 1.5m-.5-1.5h-9.5m0 0l-.5 1.5m.75-9 3-3 2.148 2.148A12.061 12.061 0 0116.5 7.605" /></svg>"""
}

# ==============================================================================
# 4. SIDEBAR
# ==============================================================================
with st.sidebar:
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:20px;">
        <div style="background:#3B82F6; padding:8px; border-radius:8px; color:white;">
            {ICONS['document']}
        </div>
        <h2 style="margin:0; font-size:20px; font-weight:700;">TalentScout</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="sidebar-info">
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
            <div style="width:8px; height:8px; background:#10B981; border-radius:50%;"></div>
            <span style="font-size:14px; font-weight:600;">System Online</span>
        </div>
        <div style="font-size:12px; color:#94A3B8;">
            NLP Engine: <strong>v2.5.0</strong><br>
            Parser: <strong>Active</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:13px; color:#CBD5E1;">
        <strong>Instructions:</strong><br>
        1. Upload a PDF resume.<br>
        2. Wait for the Neural Engine to process.<br>
        3. Review extracted insights.
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 5. MAIN LAYOUT
# ==============================================================================
st.markdown("""
<h1 style="font-size: 32px; font-weight: 800; color: #111827; margin-bottom: 8px;">Resume Intelligence Dashboard</h1>
<p style="font-size: 16px; color: #6B7280; margin-bottom: 32px;">Extract, analyze, and structure candidate data automatically.</p>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload Candidate Resume (PDF)", type="pdf")

if uploaded_file:
    try:
        reader = PdfReader(uploaded_file)
        text = " ".join([page.extract_text() for page in reader.pages])
        parser = ResumeParser(text)
        data = parser.parse()
        skills = sorted(data.get("Skills", []))

        # Confidence Score Logic
        confidence_level = 0
        if data.get('Email'): confidence_level += 40
        if data.get('Phone'): confidence_level += 40
        if len(skills) > 0: confidence_level += 20
        score_color = "#10B981" if confidence_level > 80 else "#F59E0B"

        st.markdown("<br>", unsafe_allow_html=True)

        # --- ROW 1: PROFILE & SCORE ---
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(
                f"""<div class="metric-card"><div class="section-header">Candidate Profile</div><div style="display: flex; align-items: flex-start; gap: 24px;"><div style="width: 64px; height: 64px; background-color: #F3F4F6; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 24px;">👤</div><div style="flex: 1;"><div style="margin-bottom: 16px;"><div class="data-label">Full Name</div><div style="font-size: 20px; font-weight: 700; color: #111827;">{data.get('Name') or 'Not Detected'}</div></div><div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;"><div><div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">{ICONS['mail']} <span class="data-label" style="margin:0;">Email Address</span></div><div class="data-value">{data.get('Email') or 'N/A'}</div></div><div><div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">{ICONS['phone']} <span class="data-label" style="margin:0;">Phone Number</span></div><div class="data-value">{data.get('Phone') or 'N/A'}</div></div></div></div></div></div>""",
                unsafe_allow_html=True)

        with col2:
            st.markdown(
                f"""<div class="metric-card"><div class="section-header">Analysis Score</div><div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;"><span style="font-size: 14px; font-weight: 500; color: #6B7280;">Data Completeness</span><span style="font-size: 18px; font-weight: 700; color: {score_color};">{confidence_level}%</span></div><div style="width: 100%; height: 8px; background-color: #F3F4F6; border-radius: 4px; overflow: hidden;"><div style="width: {confidence_level}%; height: 100%; background-color: {score_color}; border-radius: 4px;"></div></div><div style="margin-top: 24px;"><div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">{ICONS['chart']} <span class="data-label" style="margin:0;">Skills Identified</span></div><div class="data-value" style="font-size: 24px;">{len(skills)}</div></div></div>""",
                unsafe_allow_html=True)

        # --- ROW 2: SKILLS ---
        skills_html = "".join([f'<span class="skill-chip">{s}</span>' for s in
                               skills]) if skills else "<span style='color:#6B7280; font-style:italic;'>No technical skills detected in document text.</span>"

        st.markdown(
            f"""<div class="metric-card"><div style="display: flex; align-items: center; gap: 8px; margin-bottom: 16px;">{ICONS['cpu']} <div class="section-header" style="margin:0;">Technical Competencies</div></div><div style="line-height: 2;">{skills_html}</div></div>""",
            unsafe_allow_html=True)

        # --- ROW 3: EXPERIENCE & PROJECTS ---
        col3, col4 = st.columns(2)

        # Compact HTML strings to prevent '</div>' block error
        with col3:
            exp_content = '<br><br>'.join(data.get('Experience', [])[:5]) or '<i>No experience section detected.</i>'
            if len(data.get('Experience', [])) > 5: exp_content += '<br><br><i>... (and more)</i>'
            st.markdown(
                f"""<div class="metric-card"><div class="section-header">Work Experience Summary</div><div style="font-size: 14px; color: #374151; max-height: 200px; overflow-y: auto; padding-right: 10px;">{exp_content}</div></div>""",
                unsafe_allow_html=True)

        with col4:
            proj_content = '<br><br>'.join(data.get('Projects', [])[:5]) or '<i>No projects section detected.</i>'
            if len(data.get('Projects', [])) > 5: proj_content += '<br><br><i>... (and more)</i>'
            st.markdown(
                f"""<div class="metric-card"><div class="section-header">Key Projects Summary</div><div style="font-size: 14px; color: #374151; max-height: 200px; overflow-y: auto; padding-right: 10px;">{proj_content}</div></div>""",
                unsafe_allow_html=True)

        # --- ROW 4: RAW DATA ---
        with st.expander("View Raw System Output"):
            st.json(data)

    except Exception as e:
        st.error(f"Error processing file: {str(e)}")

else:
    st.markdown(
        f"""<div style="border: 2px dashed #E5E7EB; border-radius: 12px; padding: 64px; text-align: center; background-color: #FFFFFF;"><div style="margin: 0 auto; width: 48px; height: 48px; color: #9CA3AF; margin-bottom: 16px;">{ICONS['document']}</div><h3 style="font-size: 16px; font-weight: 600; color: #111827; margin-bottom: 8px;">No Resume Uploaded</h3><p style="font-size: 14px; color: #6B7280;">Upload a PDF file to begin the extraction process.</p></div>""",
        unsafe_allow_html=True)