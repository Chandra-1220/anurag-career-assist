"""
Anurag University Career & Placement Assistant
================================================
Run with:  streamlit run career_assistant_app.py

Required packages (add to requirements.txt):
    streamlit
    openai
    pdfplumber
    reportlab
    plotly
    python-docx   (optional, for .docx resume uploads)

Add your key to .streamlit/secrets.toml as:
    OPENAI_API_KEY = "sk-..."
"""

import io
import re
import json
import random
from datetime import datetime

import streamlit as st
import plotly.graph_objects as go
from openai import OpenAI

# ===========================================================
# PAGE CONFIG
# ===========================================================
st.set_page_config(
    page_title="Anurag University Career Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ===========================================================
# DESIGN TOKENS — academic navy & gold theme
# ===========================================================
NAVY = "#0B2545"
NAVY_DEEP = "#081A33"
GOLD = "#C9A24B"
CREAM = "#F7F5EF"
SLATE = "#233044"
TEAL = "#2F6690"
GREEN = "#2E8B57"
RED = "#C0392B"
AMBER = "#C98A2C"

st.markdown('<meta name="color-scheme" content="light only">', unsafe_allow_html=True)

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500;600;700&display=swap');

    :root {{ color-scheme: light only; }}
    html, body {{ color-scheme: light only; }}
    html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
    .stApp {{ background-color: {CREAM}; }}

    .stApp, .stApp p, .stApp span, .stApp li, .stApp label,
    .stMarkdown, .stMarkdown p, .stMarkdown li,
    div[data-testid="stMetricValue"], div[data-testid="stMetricLabel"],
    div[data-testid="stCaptionContainer"] {{ color: {SLATE} !important; }}

    button[data-baseweb="tab"], button[data-baseweb="tab"] * {{
        color: {NAVY} !important; font-weight: 600 !important;
    }}
    button[data-baseweb="tab"][aria-selected="true"],
    button[data-baseweb="tab"][aria-selected="true"] * {{ color: {GOLD} !important; }}
    div[data-baseweb="tab-highlight"] {{ background-color: {GOLD} !important; }}

    div[data-testid="stChatMessage"] p, div[data-testid="stChatMessage"] li {{ color: {SLATE} !important; }}

    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {{ color: #f0f6ff !important; }}

    .site-header {{
        background: linear-gradient(135deg, {NAVY_DEEP} 0%, {NAVY} 60%, {TEAL} 100%);
        padding: 2.6rem 2rem 2.2rem 2rem;
        border-radius: 0 0 18px 18px;
        margin-bottom: 1.5rem;
        box-shadow: 0 6px 18px rgba(8,26,51,0.25);
    }}
    .site-header h1 {{
        font-family: 'Playfair Display', serif; color: {GOLD} !important;
        font-size: 2.6rem; margin-bottom: 0.3rem; letter-spacing: 0.3px;
    }}
    .site-header p, .site-header p * {{
        color: {CREAM} !important; font-size: 1.05rem; font-weight: 500;
        letter-spacing: 0.5px; text-transform: uppercase; margin: 0;
    }}
    .site-header .tagline, .site-header .tagline * {{
        color: {CREAM} !important; text-transform: none; font-weight: 400;
        font-size: 1rem; margin-top: 0.6rem; letter-spacing: 0;
    }}

    .section-title {{
        font-family: 'Playfair Display', serif; color: {NAVY}; font-size: 1.7rem;
        border-left: 5px solid {GOLD}; padding-left: 0.7rem; margin: 1.4rem 0 1rem 0;
    }}

    .theory-card {{
        background: #ffffff; border: 1px solid #e7e2d6; border-radius: 14px;
        padding: 1.1rem 1.3rem; margin-bottom: 1rem; box-shadow: 0 2px 6px rgba(11,37,69,0.05);
    }}
    .theory-card h4 {{ color: {NAVY}; margin-bottom: 0.4rem; font-family: 'Playfair Display', serif; }}
    .theory-card p, .theory-card li {{ color: {SLATE}; font-size: 0.95rem; line-height: 1.5rem; }}

    .stat-box {{
        background: #ffffff; border-radius: 12px; padding: 1rem; text-align: center;
        border: 1px solid #e7e2d6;
    }}
    .stat-box .num {{
        font-family: 'Playfair Display', serif; color: {GOLD}; font-size: 1.8rem; font-weight: 700;
    }}
    .stat-box .label {{ color: {SLATE}; font-size: 0.85rem; }}

    section[data-testid="stSidebar"] {{ background-color: {NAVY_DEEP}; }}
    section[data-testid="stSidebar"] * {{ color: #f0f6ff !important; }}

    div[data-testid="stChatMessage"] {{
        background-color: #ffffff; border: 1px solid #e7e2d6; border-radius: 14px;
        padding: 0.6rem 0.9rem; margin-bottom: 0.4rem;
    }}

    div[data-testid="stChatInput"] textarea,
    div[data-testid="stChatInputTextArea"] textarea,
    .stChatInput textarea {{
        background-color: #ffffff !important; color: {SLATE} !important;
        caret-color: {SLATE} !important; border: 1px solid #d8d2c2 !important; border-radius: 12px !important;
    }}
    div[data-testid="stChatInput"] textarea::placeholder,
    .stChatInput textarea::placeholder {{ color: #8a8f98 !important; opacity: 1 !important; }}
    div[data-testid="stChatInput"] {{ background-color: #ffffff !important; border-radius: 12px !important; }}

    /* ---- New feature UI ---- */
    .feature-banner {{
        background: linear-gradient(120deg, #ffffff 0%, #fbf8f1 100%);
        border: 1px solid #e7e2d6; border-left: 5px solid {GOLD};
        border-radius: 12px; padding: 0.9rem 1.2rem; margin-bottom: 1.2rem;
        color: {SLATE}; font-size: 0.95rem;
    }}

    .score-badge {{
        display: inline-block; padding: 0.35rem 0.9rem; border-radius: 999px;
        font-weight: 700; font-size: 0.95rem; color: #fff;
    }}
    .chip {{
        display: inline-block; padding: 0.3rem 0.75rem; margin: 0.2rem;
        border-radius: 999px; font-size: 0.85rem; font-weight: 600;
    }}
    .chip-yes {{ background: #e6f4ea; color: {GREEN}; border: 1px solid #bfe3c9; }}
    .chip-no {{ background: #fdecea; color: {RED}; border: 1px solid #f4c7c1; }}

    .roadmap-card {{
        background: #ffffff; border: 1px solid #e7e2d6; border-left: 5px solid {TEAL};
        border-radius: 12px; padding: 1rem 1.2rem; margin-bottom: 0.9rem;
    }}
    .roadmap-week {{
        display: inline-block; background: {NAVY}; color: {GOLD} !important;
        font-weight: 700; border-radius: 8px; padding: 0.15rem 0.6rem;
        font-family: 'Playfair Display', serif; margin-right: 0.5rem;
    }}

    .job-card {{
        background: #ffffff; border: 1px solid #e7e2d6; border-radius: 14px;
        padding: 1rem 1.2rem; margin-bottom: 0.9rem; border-top: 4px solid {GOLD};
    }}
    .job-card h4 {{ color: {NAVY}; margin: 0 0 0.3rem 0; }}
    .match-pill {{
        float: right; background: {NAVY}; color: {CREAM} !important; font-weight: 700;
        padding: 0.2rem 0.7rem; border-radius: 999px; font-size: 0.85rem;
    }}

    .interview-q {{
        background: linear-gradient(135deg, {NAVY_DEEP} 0%, {NAVY} 100%);
        color: {CREAM} !important; border-radius: 14px; padding: 1rem 1.3rem;
        margin-bottom: 1rem; font-size: 1.05rem;
    }}
    .interview-q * {{ color: {CREAM} !important; }}

    /* ---- Chat Assistant redesign ---- */
    .chat-hero {{
        background: linear-gradient(135deg, {NAVY_DEEP} 0%, {NAVY} 55%, {TEAL} 100%);
        border-radius: 16px; padding: 1.4rem 1.6rem; margin-bottom: 1.1rem;
        box-shadow: 0 6px 16px rgba(11,37,69,0.2);
        display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 0.8rem;
    }}
    .chat-hero .chat-hero-text h3 {{
        color: {GOLD} !important; font-family: 'Playfair Display', serif; margin: 0 0 0.2rem 0; font-size: 1.4rem;
    }}
    .chat-hero .chat-hero-text p {{ color: {CREAM} !important; margin: 0; font-size: 0.92rem; }}
    .chat-hero .chat-hero-emoji {{ font-size: 2.4rem; }}
    .chat-status-pill {{
        display: inline-flex; align-items: center; gap: 0.4rem; background: rgba(201,162,75,0.18);
        border: 1px solid {GOLD}; color: {GOLD} !important; padding: 0.3rem 0.8rem; border-radius: 999px;
        font-size: 0.8rem; font-weight: 600;
    }}
    .chat-status-dot {{
        width: 8px; height: 8px; border-radius: 50%; background: #4CD964; display: inline-block;
        box-shadow: 0 0 0 0 rgba(76,217,100,0.6); animation: pulse-dot 1.6s infinite;
    }}
    @keyframes pulse-dot {{
        0% {{ box-shadow: 0 0 0 0 rgba(76,217,100,0.6); }}
        70% {{ box-shadow: 0 0 0 6px rgba(76,217,100,0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(76,217,100,0); }}
    }}

    .empty-chat-card {{
        background: #ffffff; border: 1px dashed #d8d2c2; border-radius: 16px;
        padding: 1.6rem; text-align: center; margin-bottom: 1rem;
    }}
    .empty-chat-card .big-emoji {{ font-size: 2.4rem; margin-bottom: 0.4rem; }}
    .empty-chat-card h4 {{ color: {NAVY}; font-family: 'Playfair Display', serif; margin-bottom: 0.3rem; }}
    .empty-chat-card p {{ color: {SLATE}; font-size: 0.92rem; margin-bottom: 0; }}

    /* Suggestion chip buttons */
    div[data-testid="stHorizontalBlock"] .stButton button {{
        background: #ffffff !important; color: {NAVY} !important; border: 1px solid {GOLD} !important;
        border-radius: 999px !important; font-size: 0.82rem !important; font-weight: 600 !important;
        padding: 0.35rem 0.9rem !important; box-shadow: none !important; white-space: normal !important;
    }}
    div[data-testid="stHorizontalBlock"] .stButton button:hover {{
        background: {NAVY} !important; color: {GOLD} !important; border: 1px solid {NAVY} !important;
    }}

    /* Chat bubbles — align user right, assistant left, distinct colors */
    div[data-testid="stChatMessage"] {{
        max-width: 88%;
        box-shadow: 0 2px 8px rgba(11,37,69,0.06);
    }}
    div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {{
        margin-left: auto; margin-right: 0;
        background: linear-gradient(135deg, {NAVY} 0%, {TEAL} 100%) !important;
        border: none !important; border-bottom-right-radius: 4px !important;
        flex-direction: row-reverse;
    }}
    div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) p,
    div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) li,
    div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) span {{
        color: {CREAM} !important;
    }}
    div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {{
        margin-right: auto; margin-left: 0;
        border-left: 4px solid {GOLD} !important; border-bottom-left-radius: 4px !important;
    }}

    .typing-indicator {{ display: inline-flex; gap: 4px; align-items: center; padding: 0.2rem 0; }}
    .typing-indicator span {{
        width: 7px; height: 7px; border-radius: 50%; background: {TEAL}; display: inline-block;
        animation: typing-bounce 1.2s infinite ease-in-out;
    }}
    .typing-indicator span:nth-child(2) {{ animation-delay: 0.2s; }}
    .typing-indicator span:nth-child(3) {{ animation-delay: 0.4s; }}
    @keyframes typing-bounce {{
        0%, 60%, 100% {{ transform: translateY(0); opacity: 0.5; }}
        30% {{ transform: translateY(-5px); opacity: 1; }}
    }}

    /* ---- Hardened form controls: always pair a background with its text color ---- */
    .stTextInput input, .stTextArea textarea, .stNumberInput input,
    .stSelectbox div[data-baseweb="select"] > div,
    .stMultiSelect div[data-baseweb="select"] > div {{
        background-color: #ffffff !important; color: {SLATE} !important;
        border: 1px solid #d8d2c2 !important; caret-color: {SLATE} !important;
    }}
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {{
        color: #8a8f98 !important; opacity: 1 !important;
    }}
    /* Dropdown / multiselect popover menus (BaseWeb renders these in a portal, outside .stApp) */
    div[data-baseweb="popover"] ul, div[data-baseweb="popover"] li,
    div[data-baseweb="menu"] {{
        background-color: #ffffff !important; color: {SLATE} !important;
    }}
    div[data-baseweb="popover"] li:hover {{ background-color: #f2eee2 !important; }}
    /* Multiselect selected-item tags */
    span[data-baseweb="tag"] {{
        background-color: {NAVY} !important; color: {CREAM} !important;
    }}
    span[data-baseweb="tag"] * {{ color: {CREAM} !important; }}

    /* Alerts (st.info / st.warning / st.error / st.success) — force light-theme-safe pairs */
    div[data-testid="stAlert"] {{ background-color: #ffffff !important; border: 1px solid #e7e2d6 !important; }}
    div[data-testid="stAlert"] p, div[data-testid="stAlert"] span, div[data-testid="stAlert"] div {{
        color: {SLATE} !important;
    }}

    /* Radio / checkbox labels inside the main app (not sidebar) */
    section[data-testid="stMain"] div[data-testid="stRadio"] label,
    section[data-testid="stMain"] div[data-testid="stCheckbox"] label {{
        color: {SLATE} !important;
    }}

    /* File uploader dropzone */
    div[data-testid="stFileUploaderDropzone"] {{
        background-color: #ffffff !important; border: 1px dashed #d8d2c2 !important;
    }}
    div[data-testid="stFileUploaderDropzone"] * {{ color: {SLATE} !important; }}

    /* Expander */
    div[data-testid="stExpander"] {{ background-color: #ffffff !important; border: 1px solid #e7e2d6 !important; }}
    div[data-testid="stExpander"] * {{ color: {SLATE} !important; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ===========================================================
# LANGUAGE CONFIGURATION
# ===========================================================
LANGUAGE_PROMPTS = {
    "English": "Reply strictly in clear, simple English. Avoid using any other language.",
    "Telugu": (
        "Reply strictly in Telugu script (తెలుగు). Use simple, everyday Telugu words "
        "that a degree-college student can easily understand."
    ),
    "Hinglish": (
        "Reply in Hinglish — a natural mix of Hindi and English written in Roman "
        "(English) script, the way Indian students commonly chat. Keep it friendly "
        "and easy to understand."
    ),
    "Telgish": (
        "Reply in 'Telgish' — a natural mix of Telugu and English written in Roman "
        "(English) script, the way Telugu students commonly chat online (e.g. "
        "'Nenu resume prepare cheyali, ela start cheyyali?'). Keep it friendly and easy."
    ),
}
LANGUAGE_ICON = {"English": "🇬🇧", "Telugu": "🇮🇳", "Hinglish": "🗣️", "Telgish": "💬"}

BASE_SYSTEM_PROMPT = (
    "You are the official career and placement assistant for Anurag University. "
    "Guide students on IT jobs, government jobs, internships, resume building, "
    "communication skills, coding basics, interview preparation, and practical "
    "career paths. Give realistic, actionable, step-by-step advice. Keep answers "
    "concise and practical."
)

def build_system_message(language: str) -> dict:
    return {"role": "system", "content": f"{BASE_SYSTEM_PROMPT} {LANGUAGE_PROMPTS[language]}"}

PLACEHOLDER_TEXT = {
    "English": "Ask something about careers, jobs, or placements...",
    "Telugu": "కెరీర్, జాబ్స్, ప్లేస్‌మెంట్స్ గురించి అడగండి...",
    "Hinglish": "Career, jobs ya placements ke baare mein kuch pucho...",
    "Telgish": "Career, jobs, placements gurinchi emaina adagandi...",
}

# ===========================================================
# ROLE / SKILL DATABASE (used by ATS scoring, skill gap,
# roadmap, and job recommendation engine)
# ===========================================================
ROLE_SKILLS = {
    "Software Developer": [
        "Python", "Java", "C++", "Git", "SQL", "Data Structures", "Algorithms",
        "OOP", "REST APIs", "Problem Solving", "Debugging", "Unit Testing",
    ],
    "Web Developer": [
        "HTML", "CSS", "JavaScript", "React", "Node.js", "Git", "REST APIs",
        "Responsive Design", "MongoDB", "SQL", "TypeScript",
    ],
    "Data Analyst": [
        "Python", "SQL", "Excel", "Power BI", "Statistics", "Data Visualization",
        "Pandas", "NumPy", "Data Cleaning", "Communication",
    ],
    "Data Scientist / ML Engineer": [
        "Python", "Machine Learning", "Statistics", "Pandas", "NumPy",
        "Scikit-learn", "Deep Learning", "SQL", "Data Visualization", "Mathematics",
    ],
    "Cybersecurity Analyst": [
        "Networking", "Linux", "Security Fundamentals", "Python", "Ethical Hacking",
        "Risk Assessment", "SIEM Tools", "Cryptography",
    ],
    "Business/System Analyst": [
        "Excel", "SQL", "Communication", "Requirement Gathering", "Documentation",
        "Process Mapping", "Stakeholder Management", "Power BI",
    ],
    "Government Job Aspirant": [
        "General Knowledge", "Quantitative Aptitude", "Reasoning", "English",
        "Current Affairs", "Time Management", "Mock Test Practice",
    ],
}

ALL_SKILLS = sorted({s for skills in ROLE_SKILLS.values() for s in skills})

ACTION_VERBS = [
    "built", "developed", "led", "designed", "managed", "created", "implemented",
    "improved", "analyzed", "launched", "automated", "optimized", "collaborated",
    "presented", "organized", "achieved",
]
RESUME_SECTIONS = ["education", "experience", "skills", "projects", "certification", "summary", "objective", "achievements"]

# ===========================================================
# HELPERS
# ===========================================================
def gauge_chart(value, title, color=GOLD):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": title, "font": {"size": 15, "color": SLATE}},
        number={"suffix": "%", "font": {"color": NAVY, "size": 30}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": SLATE},
            "bar": {"color": color},
            "bgcolor": "white",
            "borderwidth": 1,
            "bordercolor": "#e7e2d6",
            "steps": [
                {"range": [0, 40], "color": "#fdecea"},
                {"range": [40, 70], "color": "#fff4e0"},
                {"range": [70, 100], "color": "#e8f5e9"},
            ],
        },
    ))
    fig.update_layout(height=230, margin=dict(l=15, r=15, t=45, b=10), paper_bgcolor="rgba(0,0,0,0)")
    return fig


def score_color(score):
    if score >= 75:
        return GREEN
    if score >= 50:
        return AMBER
    return RED


def score_badge_html(score, label=""):
    c = score_color(score)
    return f'<span class="score-badge" style="background:{c};">{label} {score}/100</span>'


def extract_text_from_upload(uploaded_file) -> str:
    """Extract raw text from an uploaded resume (pdf, txt, or docx)."""
    name = uploaded_file.name.lower()
    data = uploaded_file.read()
    try:
        if name.endswith(".pdf"):
            import pdfplumber
            text = ""
            with pdfplumber.open(io.BytesIO(data)) as pdf:
                for page in pdf.pages:
                    text += (page.extract_text() or "") + "\n"
            return text
        elif name.endswith(".docx"):
            try:
                import docx
                doc = docx.Document(io.BytesIO(data))
                return "\n".join(p.text for p in doc.paragraphs)
            except ImportError:
                st.warning("python-docx not installed — please paste your resume text instead.")
                return ""
        elif name.endswith(".txt"):
            return data.decode("utf-8", errors="ignore")
        else:
            st.warning("Unsupported file type. Please upload PDF, DOCX, or TXT — or paste the text.")
            return ""
    except Exception as e:
        st.error(f"Could not read file: {e}")
        return ""


def compute_ats_score(resume_text: str, role: str):
    """Rule-based ATS-style scoring out of 100, plus a breakdown."""
    text_lower = resume_text.lower()
    keywords = ROLE_SKILLS.get(role, [])

    matched = [k for k in keywords if k.lower() in text_lower]
    missing = [k for k in keywords if k not in matched]
    keyword_score = (len(matched) / len(keywords)) * 40 if keywords else 0

    found_sections = [s for s in RESUME_SECTIONS if s in text_lower]
    section_score = min(len(found_sections) / 5, 1) * 20

    contact_score = 0
    if re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", resume_text):
        contact_score += 5
    if re.search(r"(\+?\d[\d\-\s]{8,}\d)", resume_text):
        contact_score += 5

    verb_count = sum(text_lower.count(v) for v in ACTION_VERBS)
    verb_score = min(verb_count / 8, 1) * 15

    word_count = len(resume_text.split())
    if 300 <= word_count <= 900:
        length_score = 20
    elif word_count > 0:
        length_score = 10
    else:
        length_score = 0

    total = round(keyword_score + section_score + contact_score + verb_score + length_score)
    total = max(0, min(100, total))

    breakdown = {
        "Keyword Match": round(keyword_score, 1),
        "Resume Structure": round(section_score, 1),
        "Contact Info": round(contact_score, 1),
        "Action Verbs": round(verb_score, 1),
        "Length & Density": round(length_score, 1),
    }
    return total, breakdown, matched, missing, word_count


def ask_ai(messages, temperature=0.6, max_tokens=900):
    try:
        resp = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error contacting the assistant: {e}"


def build_resume_pdf(data: dict) -> bytes:
    """Generate a clean one-page resume PDF using reportlab."""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, ListFlowable, ListItem
    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib import colors

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        topMargin=18 * mm, bottomMargin=16 * mm, leftMargin=18 * mm, rightMargin=18 * mm,
    )
    styles = getSampleStyleSheet()
    navy = colors.HexColor(NAVY)
    slate = colors.HexColor(SLATE)
    gold = colors.HexColor(GOLD)

    name_style = ParagraphStyle("Name", parent=styles["Title"], alignment=TA_CENTER, textColor=navy, fontSize=22, spaceAfter=2)
    contact_style = ParagraphStyle("Contact", parent=styles["Normal"], alignment=TA_CENTER, textColor=slate, fontSize=9.5, spaceAfter=10)
    heading_style = ParagraphStyle("Heading", parent=styles["Heading2"], textColor=navy, fontSize=12.5, spaceBefore=10, spaceAfter=4, borderColor=gold)
    body_style = ParagraphStyle("Body", parent=styles["Normal"], textColor=slate, fontSize=9.8, leading=13.5)
    bullet_style = ParagraphStyle("Bullet", parent=styles["Normal"], textColor=slate, fontSize=9.8, leading=13.5, leftIndent=8)

    story = [
        Paragraph(data.get("name", "Your Name"), name_style),
        Paragraph(
            " • ".join(filter(None, [data.get("email"), data.get("phone"), data.get("linkedin"), data.get("location")])),
            contact_style,
        ),
    ]

    def section(title, content_flowables):
        story.append(HRFlowable(width="100%", color=gold, thickness=1.2, spaceAfter=2))
        story.append(Paragraph(title.upper(), heading_style))
        story.extend(content_flowables)

    if data.get("summary"):
        section("Career Objective", [Paragraph(data["summary"], body_style)])

    if data.get("skills"):
        items = [ListItem(Paragraph(s.strip(), bullet_style)) for s in data["skills"].split(",") if s.strip()]
        section("Skills", [ListFlowable(items, bulletType="bullet", start="•")])

    if data.get("education"):
        section("Education", [Paragraph(line, body_style) for line in data["education"].split("\n") if line.strip()])

    if data.get("projects"):
        items = [ListItem(Paragraph(p.strip(), bullet_style)) for p in data["projects"].split("\n") if p.strip()]
        section("Projects", [ListFlowable(items, bulletType="bullet", start="•")])

    if data.get("experience"):
        items = [ListItem(Paragraph(p.strip(), bullet_style)) for p in data["experience"].split("\n") if p.strip()]
        section("Experience", [ListFlowable(items, bulletType="bullet", start="•")])

    if data.get("certifications"):
        items = [ListItem(Paragraph(c.strip(), bullet_style)) for c in data["certifications"].split("\n") if c.strip()]
        section("Certifications", [ListFlowable(items, bulletType="bullet", start="•")])

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


def job_match_percentages(current_skills):
    """Return sorted list of (role, match_pct, matched, missing) for all roles."""
    results = []
    current_set = {s.lower() for s in current_skills}
    for role, skills in ROLE_SKILLS.items():
        matched = [s for s in skills if s.lower() in current_set]
        missing = [s for s in skills if s.lower() not in current_set]
        pct = round((len(matched) / len(skills)) * 100) if skills else 0
        results.append((role, pct, matched, missing))
    results.sort(key=lambda x: x[1], reverse=True)
    return results


# ===========================================================
# SIDEBAR
# ===========================================================
with st.sidebar:
    st.markdown("### ⚙️ Assistant Settings")
    language = st.radio(
        "Choose reply language",
        options=list(LANGUAGE_PROMPTS.keys()),
        format_func=lambda l: f"{LANGUAGE_ICON[l]}  {l}",
        index=0,
        key="language_choice",
    )
    st.markdown("---")
    st.markdown("### 🎯 Your Target Role")
    target_role = st.selectbox("Used across Resume Analyzer, Career Path & Dashboard", list(ROLE_SKILLS.keys()), key="target_role")
    st.markdown("---")
    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = [build_system_message(language)]
        st.session_state.active_language = language
        st.rerun()
    if st.button("♻️ Reset all progress", use_container_width=True):
        for k in ["ats_score", "ats_breakdown", "matched_keywords", "missing_keywords",
                  "resume_text", "current_skills", "roadmap_text", "interview_history",
                  "interview_scores", "interview_active", "interview_question_count"]:
            st.session_state.pop(k, None)
        st.rerun()
    st.markdown("---")
    st.caption("Switching language starts a fresh chat in that language.")

# ===========================================================
# API KEY
# ===========================================================
api_key = st.secrets.get("OPENAI_API_KEY")
if not api_key:
    st.error("❌ OPENAI_API_KEY not found in Streamlit Secrets.")
    st.stop()
client = OpenAI(api_key=api_key)

# ===========================================================
# HERO / SITE HEADER
# ===========================================================
st.markdown(
    """
    <div class="site-header">
        <p>Anurag University · Placement Cell</p>
        <h1>🎓 Career &amp; Placement Assistant</h1>
        <p class="tagline">
            Resume analysis, mock interviews, skill gap tracking, personalized
            roadmaps, and job matching — all built for our students, in the
            language you're most comfortable with.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ===========================================================
# SESSION STATE
# ===========================================================
if "messages" not in st.session_state:
    st.session_state.messages = [build_system_message(language)]
    st.session_state.active_language = language

if st.session_state.get("active_language") != language:
    st.session_state.messages = [build_system_message(language)]
    st.session_state.active_language = language
    st.rerun()

st.session_state.setdefault("resume_text", "")
st.session_state.setdefault("ats_score", None)
st.session_state.setdefault("ats_breakdown", {})
st.session_state.setdefault("matched_keywords", [])
st.session_state.setdefault("missing_keywords", [])
st.session_state.setdefault("current_skills", [])
st.session_state.setdefault("roadmap_text", "")
st.session_state.setdefault("interview_history", [])
st.session_state.setdefault("interview_scores", [])
st.session_state.setdefault("interview_active", False)
st.session_state.setdefault("interview_question_count", 0)

# ===========================================================
# NAVIGATION TABS
# ===========================================================
(tab_home, tab_academics, tab_resume, tab_builder, tab_path,
 tab_interview, tab_dashboard, tab_chat, tab_contact) = st.tabs(
    ["🏠 Home", "📚 Career Guidance", "📄 Resume Analyzer", "🛠️ Resume Builder",
     "🎯 Career Path", "🎤 Mock Interview", "📊 Dashboard", "💬 Chat Assistant", "📞 Contact"]
)

# -----------------------------------------------------------
# TAB 1 — HOME
# -----------------------------------------------------------
with tab_home:
    col1, col2 = st.columns([1.3, 1])
    with col1:
        st.markdown('<div class="section-title">Welcome</div>', unsafe_allow_html=True)
        st.write(
            "The Anurag University Career & Placement Assistant helps students plan "
            "their career path with practical, step-by-step guidance — analyze your "
            "resume, practice mock interviews, track skill gaps, get a personalized "
            "roadmap, and see which roles match you best. Chat with the assistant in "
            "English, Telugu, Hinglish, or Telgish, whichever feels most natural."
        )
        c1, c2, c3, c4 = st.columns(4)
        for col, num, label in [
            (c1, "500+", "Students Guided"),
            (c2, "7", "Career Tools"),
            (c3, "4", "Languages Supported"),
            (c4, "24/7", "Assistant Availability"),
        ]:
            with col:
                st.markdown(
                    f'<div class="stat-box"><div class="num">{num}</div>'
                    f'<div class="label">{label}</div></div>',
                    unsafe_allow_html=True,
                )
    with col2:
        st.image("https://picsum.photos/id/1074/900/600", caption="Anurag University students", use_container_width=True)

    st.markdown('<div class="section-title">Explore the Toolkit</div>', unsafe_allow_html=True)
    tools = [
        ("📄", "Resume Analyzer", "Get an ATS-style score with keyword & structure breakdown."),
        ("🛠️", "Resume Builder", "Fill a form, download a polished one-page PDF resume."),
        ("🎯", "Career Path", "Skill gap analysis, personalized roadmap & job matches."),
        ("🎤", "Mock Interview", "Practice live with AI-driven questions and STAR feedback."),
    ]
    cols = st.columns(4)
    for col, (icon, title, desc) in zip(cols, tools):
        with col:
            st.markdown(f'<div class="theory-card"><h4>{icon} {title}</h4><p>{desc}</p></div>', unsafe_allow_html=True)

# -----------------------------------------------------------
# TAB 2 — CAREER GUIDANCE (theory + images)
# -----------------------------------------------------------
with tab_academics:
    st.markdown('<div class="section-title">Career Guidance Topics</div>', unsafe_allow_html=True)
    st.write("Structured, easy-to-follow guidance on the topics students ask about most.")

    topics = [
        {"title": "💻 IT Jobs & Coding Basics", "image": "https://picsum.photos/id/0/900/600", "points": [
            "Start with one language (Python or Java) and build small projects before job hunting.",
            "Learn Git, basic SQL, and one framework relevant to your target role.",
            "Apply to internships early — real project experience matters more than certificates alone.",
        ]},
        {"title": "🏛️ Government Jobs", "image": "https://picsum.photos/id/1029/900/600", "points": [
            "Identify exams matching your degree: SSC, bank PO, state PSC, railway, or defence exams.",
            "Build a fixed daily study timetable and revise previous years' question papers.",
            "Track official notifications from state and central recruitment boards regularly.",
        ]},
        {"title": "🧑‍💼 Internships", "image": "https://picsum.photos/id/1076/900/600", "points": [
            "Use LinkedIn, Internshala, and your college placement cell to find openings.",
            "Even unpaid internships in your first year build skills and references.",
            "Ask for a Letter of Recommendation at the end of every internship.",
        ]},
        {"title": "📄 Resume Building", "image": "https://picsum.photos/id/1050/900/600", "points": [
            "Keep it to one page with clear sections: Education, Skills, Projects, Experience.",
            "Use action verbs and numbers (e.g. 'Built a website used by 200+ students').",
            "Tailor your resume slightly for each job — match keywords from the job posting.",
        ]},
        {"title": "🗣️ Communication Skills", "image": "https://picsum.photos/id/1062/900/600", "points": [
            "Practice speaking English or Hindi/Telugu for 10 minutes daily on familiar topics.",
            "Join college clubs, debates, or group discussions to build confidence.",
            "Record yourself answering common interview questions and review your clarity.",
        ]},
        {"title": "🤝 Interview Preparation", "image": "https://picsum.photos/id/1027/900/600", "points": [
            "Research the company and role before every interview — even a small startup.",
            "Prepare 3–4 stories about your projects using the Situation-Task-Action-Result format.",
            "Always prepare 2 thoughtful questions to ask the interviewer at the end.",
        ]},
    ]

    for i in range(0, len(topics), 2):
        cols = st.columns(2)
        for col, topic in zip(cols, topics[i:i + 2]):
            with col:
                st.image(topic["image"], use_container_width=True)
                bullets = "".join(f"<li>{p}</li>" for p in topic["points"])
                st.markdown(f'<div class="theory-card"><h4>{topic["title"]}</h4><ul>{bullets}</ul></div>', unsafe_allow_html=True)

# -----------------------------------------------------------
# TAB 3 — RESUME ANALYZER (ATS SCORE)
# -----------------------------------------------------------
with tab_resume:
    st.markdown('<div class="section-title">📄 Resume Analyzer — ATS Score</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="feature-banner">Upload your resume (PDF / TXT) or paste the text below. '
        'We\'ll score it like an Applicant Tracking System would, then the AI adds specific '
        'improvement suggestions for your target role.</div>',
        unsafe_allow_html=True,
    )

    colu, colr = st.columns([1.4, 1])
    with colu:
        uploaded = st.file_uploader("Upload resume (PDF or TXT)", type=["pdf", "txt", "docx"])
        pasted = st.text_area("...or paste your resume text here", height=180, placeholder="Paste your resume content...")
    with colr:
        st.markdown(f"**Analyzing for role:** {target_role}")
        st.caption("Change the target role from the sidebar.")
        analyze_clicked = st.button("🔍 Analyze My Resume", use_container_width=True, type="primary")

    if analyze_clicked:
        resume_text = ""
        if uploaded is not None:
            resume_text = extract_text_from_upload(uploaded)
        if not resume_text.strip() and pasted.strip():
            resume_text = pasted
        if not resume_text.strip():
            st.warning("Please upload a resume file or paste your resume text first.")
        else:
            with st.spinner("Scoring your resume..."):
                score, breakdown, matched, missing, wc = compute_ats_score(resume_text, target_role)
                st.session_state.resume_text = resume_text
                st.session_state.ats_score = score
                st.session_state.ats_breakdown = breakdown
                st.session_state.matched_keywords = matched
                st.session_state.missing_keywords = missing

    if st.session_state.ats_score is not None:
        score = st.session_state.ats_score
        breakdown = st.session_state.ats_breakdown
        st.markdown("---")
        g1, g2 = st.columns([1, 1.6])
        with g1:
            st.plotly_chart(gauge_chart(score, "Overall ATS Score", score_color(score)), use_container_width=True)
        with g2:
            st.markdown("#### Score Breakdown")
            max_pts = {"Keyword Match": 40, "Resume Structure": 20, "Contact Info": 10, "Action Verbs": 15, "Length & Density": 20}
            for k, v in breakdown.items():
                pct = int((v / max_pts[k]) * 100) if max_pts[k] else 0
                st.write(f"**{k}** — {v}/{max_pts[k]} pts")
                st.progress(min(max(pct, 0), 100))

        st.markdown("#### Keyword Match for " + target_role)
        chips = "".join(f'<span class="chip chip-yes">✓ {k}</span>' for k in st.session_state.matched_keywords)
        chips += "".join(f'<span class="chip chip-no">✗ {k}</span>' for k in st.session_state.missing_keywords)
        st.markdown(chips if chips else "_No keywords found yet._", unsafe_allow_html=True)

        if st.button("🤖 Get AI Feedback on This Resume"):
            with st.spinner("Reading your resume like a recruiter would..."):
                prompt = (
                    f"You are an expert resume reviewer for the role of {target_role}. "
                    f"Here is the candidate's resume text:\n\n{st.session_state.resume_text[:4000]}\n\n"
                    "Give: 1) 3 specific strengths, 2) 4 specific, actionable improvements "
                    "(mention exact lines/sections where possible), 3) one rewritten example "
                    "bullet point showing the 'before vs after' style. Keep it concise and practical."
                )
                feedback = ask_ai([
                    build_system_message(language),
                    {"role": "user", "content": prompt},
                ])
                st.markdown("#### 🤖 AI Reviewer Feedback")
                st.write(feedback)

# -----------------------------------------------------------
# TAB 4 — RESUME PDF GENERATOR
# -----------------------------------------------------------
with tab_builder:
    st.markdown('<div class="section-title">🛠️ Resume PDF Generator</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="feature-banner">Fill in your details below and download a clean, '
        'one-page, ATS-friendly PDF resume in the university theme.</div>',
        unsafe_allow_html=True,
    )

    with st.form("resume_builder_form"):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Full Name", placeholder="e.g. K. Sai Teja")
            email = st.text_input("Email", placeholder="you@example.com")
            phone = st.text_input("Phone", placeholder="+91 90000 00000")
        with c2:
            linkedin = st.text_input("LinkedIn / Portfolio URL", placeholder="linkedin.com/in/yourname")
            location = st.text_input("Location", placeholder="Hyderabad, India")

        summary = st.text_area("Career Objective (2-3 lines)", height=80,
                                placeholder="Final-year CSE student seeking a Software Developer role...")
        skills_in = st.text_input("Skills (comma separated)", placeholder="Python, SQL, Git, React, ...")
        education_in = st.text_area("Education (one line per entry)", height=80,
                                     placeholder="B.Tech CSE, Anurag University, 2022-2026, CGPA 8.5")
        projects_in = st.text_area("Projects (one bullet per line)", height=100,
                                    placeholder="Built a placement chatbot using Streamlit and OpenAI API")
        experience_in = st.text_area("Experience / Internships (one bullet per line)", height=100,
                                      placeholder="Intern, XYZ Pvt Ltd — Automated report generation, saving 5 hrs/week")
        certs_in = st.text_area("Certifications (one per line)", height=70,
                                 placeholder="AWS Cloud Practitioner (2025)")

        submitted = st.form_submit_button("📥 Generate Resume PDF", type="primary")

    if submitted:
        if not name.strip():
            st.warning("Please enter at least your name to generate the resume.")
        else:
            data = {
                "name": name, "email": email, "phone": phone, "linkedin": linkedin,
                "location": location, "summary": summary, "skills": skills_in,
                "education": education_in, "projects": projects_in,
                "experience": experience_in, "certifications": certs_in,
            }
            with st.spinner("Building your PDF..."):
                pdf_bytes = build_resume_pdf(data)
            st.success("Your resume is ready!")
            st.download_button(
                "⬇️ Download Resume PDF",
                data=pdf_bytes,
                file_name=f"{name.replace(' ', '_')}_Resume.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

# -----------------------------------------------------------
# TAB 5 — CAREER PATH (Skill Gap + Roadmap + Job Recommendations)
# -----------------------------------------------------------
with tab_path:
    st.markdown('<div class="section-title">🎯 Career Path Planner</div>', unsafe_allow_html=True)

    st.markdown("#### 1️⃣ Skill Gap Analysis")
    st.markdown(f'<div class="feature-banner">Select the skills you currently have. We will compare them against what a <b>{target_role}</b> role typically needs.</div>', unsafe_allow_html=True)

    current_skills = st.multiselect(
        "Your current skills",
        options=ALL_SKILLS,
        default=st.session_state.current_skills,
        placeholder="Start typing to search skills...",
    )
    st.session_state.current_skills = current_skills

    required = ROLE_SKILLS[target_role]
    have = [s for s in required if s in current_skills]
    missing = [s for s in required if s not in current_skills]
    gap_pct = round((len(have) / len(required)) * 100) if required else 0

    colg1, colg2 = st.columns([1, 1.6])
    with colg1:
        st.plotly_chart(gauge_chart(gap_pct, f"Match for {target_role}", score_color(gap_pct)), use_container_width=True)
    with colg2:
        st.markdown("**You already have:**")
        st.markdown("".join(f'<span class="chip chip-yes">✓ {s}</span>' for s in have) or "_None yet_", unsafe_allow_html=True)
        st.markdown("**Still to learn:**")
        st.markdown("".join(f'<span class="chip chip-no">✗ {s}</span>' for s in missing) or "_You're fully covered!_", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 2️⃣ Personalized Career Roadmap")
    weeks = st.slider("Timeframe (weeks) to prepare for this role", 4, 24, 8)
    if st.button("🗺️ Generate My Roadmap", type="primary"):
        with st.spinner("Building your week-by-week plan..."):
            prompt = (
                f"Create a {weeks}-week, week-by-week career preparation roadmap for a student "
                f"targeting the role of '{target_role}'. They already know: {', '.join(have) or 'nothing yet'}. "
                f"They still need to learn: {', '.join(missing) or 'nothing, they are fully ready'}. "
                "For each week give a short title and 2-3 concrete tasks (courses, practice, projects, mock tests). "
                "Format strictly as: 'Week N: Title\\n- task\\n- task' for every week, no extra preamble."
            )
            roadmap = ask_ai([build_system_message(language), {"role": "user", "content": prompt}], max_tokens=1400)
            st.session_state.roadmap_text = roadmap

    if st.session_state.roadmap_text:
        st.markdown("##### Your Roadmap")
        blocks = re.split(r"(?=Week\s*\d+\s*:)", st.session_state.roadmap_text)
        for block in blocks:
            block = block.strip()
            if not block:
                continue
            m = re.match(r"Week\s*(\d+)\s*:\s*(.*)", block)
            if m:
                wk, rest = m.group(1), m.group(2)
                title_line, *body_lines = rest.split("\n")
                body = "<br>".join(l.strip() for l in body_lines if l.strip())
                st.markdown(
                    f'<div class="roadmap-card"><span class="roadmap-week">Week {wk}</span>'
                    f'<b>{title_line.strip()}</b><br>{body}</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(f'<div class="roadmap-card">{block}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 3️⃣ Job Recommendation Engine")
    st.markdown('<div class="feature-banner">Based on the skills you selected above, here are the roles that match you best right now.</div>', unsafe_allow_html=True)
    if not current_skills:
        st.info("Select your current skills above to see job recommendations.")
    else:
        matches = job_match_percentages(current_skills)
        for role, pct, matched_r, missing_r in matches[:5]:
            st.markdown(
                f'<div class="job-card"><span class="match-pill">{pct}% match</span>'
                f'<h4>{role}</h4>'
                f'<p><b>You have:</b> {", ".join(matched_r) if matched_r else "—"}</p>'
                f'<p><b>To build:</b> {", ".join(missing_r) if missing_r else "Nothing — you\'re ready!"}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )

# -----------------------------------------------------------
# TAB 6 — AI MOCK INTERVIEW
# -----------------------------------------------------------
with tab_interview:
    st.markdown('<div class="section-title">🎤 AI Mock Interview</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="feature-banner">Practice a live interview for <b>{target_role}</b>. '
        'The assistant asks one question at a time, scores your answer using the STAR method, '
        'then moves to the next question.</div>',
        unsafe_allow_html=True,
    )

    colb1, colb2, colb3 = st.columns(3)
    with colb1:
        if st.button("▶️ Start New Interview", use_container_width=True, type="primary"):
            st.session_state.interview_history = []
            st.session_state.interview_scores = []
            st.session_state.interview_question_count = 0
            st.session_state.interview_active = True
            with st.spinner("Preparing your first question..."):
                q = ask_ai([
                    {"role": "system", "content": (
                        f"You are a professional interviewer hiring for {target_role}. "
                        "Ask exactly ONE realistic interview question (behavioral or technical, mix it up). "
                        "Output ONLY the question, no preamble."
                    )},
                    {"role": "user", "content": "Ask the first question."},
                ], max_tokens=120)
                st.session_state.interview_history.append({"role": "assistant", "content": q})
                st.session_state.interview_question_count = 1
    with colb2:
        if st.button("⏹️ End Interview", use_container_width=True):
            st.session_state.interview_active = False
    with colb3:
        st.metric("Questions Asked", st.session_state.interview_question_count)

    if st.session_state.interview_history:
        st.markdown("---")
        last_q = None
        for msg in st.session_state.interview_history:
            if msg["role"] == "assistant":
                st.markdown(f'<div class="interview-q">🎙️ {msg["content"]}</div>', unsafe_allow_html=True)
                last_q = msg["content"]
            else:
                with st.chat_message("user", avatar="🧑‍🎓"):
                    st.write(msg["content"])

        if st.session_state.interview_active:
            answer = st.chat_input("Type your answer to the question above...")
            if answer:
                st.session_state.interview_history.append({"role": "user", "content": answer})
                with st.spinner("Evaluating your answer..."):
                    critique_prompt = (
                        f"Interview question: {last_q}\nCandidate's answer: {answer}\n\n"
                        "Evaluate this answer for a candidate targeting the role of "
                        f"{target_role}. Give: a score out of 10 on the first line as "
                        "'Score: X/10', then 2-3 lines of specific feedback using the STAR "
                        "framework (Situation, Task, Action, Result) — note what was missing. "
                        "Then ask the NEXT interview question on a new line starting with 'Next Question:'."
                    )
                    result = ask_ai([
                        {"role": "system", "content": f"You are a professional interviewer for {target_role}."},
                        {"role": "user", "content": critique_prompt},
                    ], max_tokens=350)

                score_match = re.search(r"Score:\s*(\d+)", result)
                if score_match:
                    st.session_state.interview_scores.append(int(score_match.group(1)))

                parts = re.split(r"Next Question:", result)
                feedback_text = parts[0].strip()
                next_q = parts[1].strip() if len(parts) > 1 else "Tell me about a recent project you're proud of."

                st.session_state.interview_history.append({"role": "assistant", "content": f"**Feedback:** {feedback_text}"})
                st.session_state.interview_history.append({"role": "assistant", "content": next_q})
                st.session_state.interview_question_count += 1
                st.rerun()

    if st.session_state.interview_scores:
        avg = sum(st.session_state.interview_scores) / len(st.session_state.interview_scores)
        st.markdown("---")
        st.markdown(f"**Average interview score so far:** {round(avg, 1)} / 10 across {len(st.session_state.interview_scores)} answers")

# -----------------------------------------------------------
# TAB 7 — PLACEMENT READINESS DASHBOARD
# -----------------------------------------------------------
with tab_dashboard:
    st.markdown('<div class="section-title">📊 Placement Readiness Dashboard</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="feature-banner">This pulls together your Resume Analyzer score, '
        'Skill Gap match, and Mock Interview performance into one readiness view. '
        'Complete each tool to fill in the picture.</div>',
        unsafe_allow_html=True,
    )

    resume_score = st.session_state.ats_score
    skill_match = round((len([s for s in ROLE_SKILLS[target_role] if s in st.session_state.current_skills])
                          / len(ROLE_SKILLS[target_role])) * 100) if st.session_state.current_skills else None
    interview_avg = (round((sum(st.session_state.interview_scores) / len(st.session_state.interview_scores)) * 10)
                      if st.session_state.interview_scores else None)

    d1, d2, d3, d4 = st.columns(4)
    with d1:
        if resume_score is not None:
            st.plotly_chart(gauge_chart(resume_score, "Resume Score", score_color(resume_score)), use_container_width=True)
        else:
            st.info("Complete **Resume Analyzer** to see this score.")
    with d2:
        if skill_match is not None:
            st.plotly_chart(gauge_chart(skill_match, "Skill Match", score_color(skill_match)), use_container_width=True)
        else:
            st.info("Select your skills in **Career Path** to see this score.")
    with d3:
        if interview_avg is not None:
            st.plotly_chart(gauge_chart(interview_avg, "Interview Score", score_color(interview_avg)), use_container_width=True)
        else:
            st.info("Complete a **Mock Interview** to see this score.")
    with d4:
        available = [v for v in [resume_score, skill_match, interview_avg] if v is not None]
        overall = round(sum(available) / len(available)) if available else 0
        st.plotly_chart(gauge_chart(overall, "Overall Readiness", score_color(overall)), use_container_width=True)

    st.markdown("---")
    st.markdown("#### Recommended Next Steps")
    tips = []
    if resume_score is None:
        tips.append("Run your resume through the **Resume Analyzer** tab to get an ATS score.")
    elif resume_score < 70:
        tips.append("Your resume score has room to grow — check the AI feedback in **Resume Analyzer** and revise.")
    if skill_match is None:
        tips.append("Select your current skills in **Career Path** to see your match for " + target_role + ".")
    elif skill_match < 70:
        tips.append("Follow the personalized roadmap in **Career Path** to close your skill gaps.")
    if interview_avg is None:
        tips.append("Try a session in **Mock Interview** to practice under realistic conditions.")
    elif interview_avg < 70:
        tips.append("Keep practicing mock interviews — focus on structuring answers with STAR.")
    if not tips:
        tips.append("Great work — you're strong across all three areas! Keep applying and stay consistent.")
    for t in tips:
        st.markdown(f"- {t}")

# -----------------------------------------------------------
# TAB 8 — CHAT ASSISTANT
# -----------------------------------------------------------
with tab_chat:
    AVATARS = {"user": "🧑‍🎓", "assistant": "🎓"}
    real_msg_count = len([m for m in st.session_state.messages if m["role"] != "system"])

    st.markdown(
        f"""
        <div class="chat-hero">
            <div class="chat-hero-text">
                <h3><span class="chat-hero-emoji">🎓</span>&nbsp; Chat with Your Career Assistant</h3>
                <p>Ask about resumes, interviews, coding, internships, or government exams — anytime.</p>
            </div>
            <div class="chat-status-pill"><span class="chat-status-dot"></span> Online · replying in {language}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    SUGGESTIONS = [
        "🧑‍💻 How do I start preparing for IT jobs?",
        "🏛️ Government job vs private job — which is better for me?",
        "📄 What should my resume include as a fresher?",
        "🎤 How do I answer 'Tell me about yourself'?",
    ]

    pending_prompt = None

    if real_msg_count == 0:
        st.markdown(
            """
            <div class="empty-chat-card">
                <div class="big-emoji">💬</div>
                <h4>No messages yet — say hello!</h4>
                <p>Try one of the quick questions below, or type your own in the box.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        s1, s2 = st.columns(2)
        s3, s4 = st.columns(2)
        for col, sug in zip([s1, s2, s3, s4], SUGGESTIONS):
            with col:
                if st.button(sug, use_container_width=True, key=f"sugg_{sug}"):
                    pending_prompt = sug.split(" ", 1)[1]

    for msg in st.session_state.messages:
        if msg["role"] == "system":
            continue
        with st.chat_message(msg["role"], avatar=AVATARS.get(msg["role"])):
            st.write(msg["content"])

    typed_input = st.chat_input(PLACEHOLDER_TEXT.get(language, "Type your question..."))
    user_input = typed_input or pending_prompt

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar=AVATARS["user"]):
            st.write(user_input)

        with st.chat_message("assistant", avatar=AVATARS["assistant"]):
            placeholder = st.empty()
            placeholder.markdown('<div class="typing-indicator"><span></span><span></span><span></span></div>', unsafe_allow_html=True)
            try:
                response = client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=st.session_state.messages,
                )
                ai_reply = response.choices[0].message.content
                placeholder.write(ai_reply)
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            except Exception as e:
                placeholder.write(f"⚠️ Error: {str(e)}")

        if pending_prompt:
            st.rerun()

# -----------------------------------------------------------
# TAB 9 — CONTACT
# -----------------------------------------------------------
with tab_contact:
    st.markdown('<div class="section-title">Get in Touch</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
            <div class="theory-card">
                <h4>🏫 Placement Cell</h4>
                <p>Anurag University<br>
                Venkatapur, Ghatkesar, Medchal-Malkajgiri District,<br>
                Telangana, India</p>
                <p>📧 placements@anurag.edu.in<br>
                📞 +91-XXXXXXXXXX</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div class="theory-card">
                <h4>🕐 Office Hours</h4>
                <p>Monday – Saturday: 9:00 AM – 5:00 PM<br>
                Sunday: Closed</p>
                <p>This assistant is available 24/7 for quick guidance,
                but visit the Placement Cell in person for document
                verification and interview scheduling.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
