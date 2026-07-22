import streamlit as st
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

st.markdown(
    """
    <meta name="color-scheme" content="light only">
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500;600&display=swap');

    :root {{
        color-scheme: light only;
    }}
    html, body {{
        color-scheme: light only;
    }}

    html, body, [class*="css"]  {{
        font-family: 'Inter', sans-serif;
    }}

    .stApp {{
        background-color: {CREAM};
    }}

    /* Force readable text everywhere, even if dark mode is active */
    .stApp, .stApp p, .stApp span, .stApp li, .stApp label,
    .stMarkdown, .stMarkdown p, .stMarkdown li,
    div[data-testid="stMetricValue"], div[data-testid="stMetricLabel"],
    div[data-testid="stCaptionContainer"] {{
        color: {SLATE} !important;
    }}

    /* Tab labels — catch any inner element Streamlit renders (p, div, span) */
    button[data-baseweb="tab"], button[data-baseweb="tab"] * {{
        color: {NAVY} !important;
        font-weight: 600 !important;
    }}
    button[data-baseweb="tab"][aria-selected="true"],
    button[data-baseweb="tab"][aria-selected="true"] * {{
        color: {GOLD} !important;
    }}
    div[data-baseweb="tab-highlight"] {{
        background-color: {GOLD} !important;
    }}

    /* Chat message text */
    div[data-testid="stChatMessage"] p, div[data-testid="stChatMessage"] li {{
        color: {SLATE} !important;
    }}

    /* Radio button labels in sidebar stay light on navy */
    section[data-testid="stSidebar"] .stMarkdown, 
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {{
        color: #f0f6ff !important;
    }}

    /* Top banner */
    .site-header {{
        background: linear-gradient(135deg, {NAVY_DEEP} 0%, {NAVY} 60%, {TEAL} 100%);
        padding: 2.6rem 2rem 2.2rem 2rem;
        border-radius: 0 0 18px 18px;
        margin-bottom: 1.5rem;
        box-shadow: 0 6px 18px rgba(8,26,51,0.25);
    }}
    .site-header h1 {{
        font-family: 'Playfair Display', serif;
        color: {CREAM} !important;
        font-size: 2.6rem;
        margin-bottom: 0.3rem;
        letter-spacing: 0.3px;
    }}
    .site-header p, .site-header p * {{
        color: {CREAM} !important;
        font-size: 1.05rem;
        font-weight: 500;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin: 0;
    }}
    .site-header .tagline, .site-header .tagline * {{
        color: {CREAM} !important;
        text-transform: none;
        font-weight: 400;
        font-size: 1rem;
        margin-top: 0.6rem;
        letter-spacing: 0;
    }}

    /* Section headings */
    .section-title {{
        font-family: 'Playfair Display', serif;
        color: {NAVY};
        font-size: 1.7rem;
        border-left: 5px solid {GOLD};
        padding-left: 0.7rem;
        margin: 1.4rem 0 1rem 0;
    }}

    /* Theory cards */
    .theory-card {{
        background: #ffffff;
        border: 1px solid #e7e2d6;
        border-radius: 14px;
        padding: 1.1rem 1.3rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 6px rgba(11,37,69,0.05);
    }}
    .theory-card h4 {{
        color: {NAVY};
        margin-bottom: 0.4rem;
        font-family: 'Playfair Display', serif;
    }}
    .theory-card p, .theory-card li {{
        color: {SLATE};
        font-size: 0.95rem;
        line-height: 1.5rem;
    }}

    /* Stat pills */
    .stat-box {{
        background: #ffffff;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        border: 1px solid #e7e2d6;
    }}
    .stat-box .num {{
        font-family: 'Playfair Display', serif;
        color: {GOLD};
        font-size: 1.8rem;
        font-weight: 700;
    }}
    .stat-box .label {{
        color: {SLATE};
        font-size: 0.85rem;
    }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background-color: {NAVY_DEEP};
    }}
    section[data-testid="stSidebar"] * {{
        color: #f0f6ff !important;
    }}

    /* Chat bubbles */
    div[data-testid="stChatMessage"] {{
        background-color: #ffffff;
        border: 1px solid #e7e2d6;
        border-radius: 14px;
        padding: 0.6rem 0.9rem;
        margin-bottom: 0.4rem;
    }}

    footer {{visibility: hidden;}}
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
    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = [build_system_message(language)]
        st.session_state.active_language = language
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
            Guidance on IT jobs, government exams, internships, resumes, and
            interview preparation — built for our students, in the language you're
            most comfortable with.
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

# ===========================================================
# NAVIGATION TABS
# ===========================================================
tab_home, tab_academics, tab_chat, tab_contact = st.tabs(
    ["🏠 Home", "📚 Career Guidance", "💬 Chat Assistant", "📞 Contact"]
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
            "their career path with practical, step-by-step guidance — from choosing "
            "between IT and government job tracks, to building a strong resume and "
            "clearing interviews. Chat with the assistant in English, Telugu, Hinglish, "
            "or Telgish, whichever feels most natural."
        )
        c1, c2, c3 = st.columns(3)
        for col, num, label in [
            (c1, "500+", "Students Guided"),
            (c2, "4", "Languages Supported"),
            (c3, "24/7", "Assistant Availability"),
        ]:
            with col:
                st.markdown(
                    f'<div class="stat-box"><div class="num">{num}</div>'
                    f'<div class="label">{label}</div></div>',
                    unsafe_allow_html=True,
                )
    with col2:
        st.image(
            "https://picsum.photos/id/1074/900/600",
            caption="Anurag University students",
            use_container_width=True,
        )

    st.markdown('<div class="section-title">How It Works</div>', unsafe_allow_html=True)
    steps = st.columns(4)
    step_content = [
        ("1️⃣", "Pick your language", "Choose English, Telugu, Hinglish, or Telgish from the sidebar."),
        ("2️⃣", "Ask your question", "Type anything about jobs, resumes, coding, or interviews."),
        ("3️⃣", "Get actionable advice", "Receive clear, step-by-step guidance you can act on today."),
        ("4️⃣", "Explore Career Guidance", "Browse the theory tab for structured tips on every topic."),
    ]
    for col, (icon, title, desc) in zip(steps, step_content):
        with col:
            st.markdown(
                f'<div class="theory-card"><h4>{icon} {title}</h4><p>{desc}</p></div>',
                unsafe_allow_html=True,
            )

# -----------------------------------------------------------
# TAB 2 — CAREER GUIDANCE (theory + images)
# -----------------------------------------------------------
with tab_academics:
    st.markdown('<div class="section-title">Career Guidance Topics</div>', unsafe_allow_html=True)
    st.write("Structured, easy-to-follow guidance on the topics students ask about most.")

    topics = [
        {
            "title": "💻 IT Jobs & Coding Basics",
            "image": "https://picsum.photos/id/0/900/600",
            "points": [
                "Start with one language (Python or Java) and build small projects before job hunting.",
                "Learn Git, basic SQL, and one framework relevant to your target role.",
                "Apply to internships early — real project experience matters more than certificates alone.",
            ],
        },
        {
            "title": "🏛️ Government Jobs",
            "image": "https://picsum.photos/id/1029/900/600",
            "points": [
                "Identify exams matching your degree: SSC, bank PO, state PSC, railway, or defence exams.",
                "Build a fixed daily study timetable and revise previous years' question papers.",
                "Track official notifications from state and central recruitment boards regularly.",
            ],
        },
        {
            "title": "🧑‍💼 Internships",
            "image": "https://picsum.photos/id/1076/900/600",
            "points": [
                "Use LinkedIn, Internshala, and your college placement cell to find openings.",
                "Even unpaid internships in your first year build skills and references.",
                "Ask for a Letter of Recommendation at the end of every internship.",
            ],
        },
        {
            "title": "📄 Resume Building",
            "image": "https://picsum.photos/id/1050/900/600",
            "points": [
                "Keep it to one page with clear sections: Education, Skills, Projects, Experience.",
                "Use action verbs and numbers (e.g. 'Built a website used by 200+ students').",
                "Tailor your resume slightly for each job — match keywords from the job posting.",
            ],
        },
        {
            "title": "🗣️ Communication Skills",
            "image": "https://picsum.photos/id/1062/900/600",
            "points": [
                "Practice speaking English or Hindi/Telugu for 10 minutes daily on familiar topics.",
                "Join college clubs, debates, or group discussions to build confidence.",
                "Record yourself answering common interview questions and review your clarity.",
            ],
        },
        {
            "title": "🤝 Interview Preparation",
            "image": "https://picsum.photos/id/1027/900/600",
            "points": [
                "Research the company and role before every interview — even a small startup.",
                "Prepare 3–4 stories about your projects using the Situation-Task-Action-Result format.",
                "Always prepare 2 thoughtful questions to ask the interviewer at the end.",
            ],
        },
    ]

    for i in range(0, len(topics), 2):
        cols = st.columns(2)
        for col, topic in zip(cols, topics[i : i + 2]):
            with col:
                st.image(topic["image"], use_container_width=True)
                bullets = "".join(f"<li>{p}</li>" for p in topic["points"])
                st.markdown(
                    f'<div class="theory-card"><h4>{topic["title"]}</h4>'
                    f'<ul>{bullets}</ul></div>',
                    unsafe_allow_html=True,
                )

# -----------------------------------------------------------
# TAB 3 — CHAT ASSISTANT
# -----------------------------------------------------------
with tab_chat:
    st.markdown('<div class="section-title">Chat with the Assistant</div>', unsafe_allow_html=True)

    AVATARS = {"user": "🧑‍🎓", "assistant": "🎓"}

    for msg in st.session_state.messages:
        if msg["role"] == "system":
            continue
        with st.chat_message(msg["role"], avatar=AVATARS.get(msg["role"])):
            st.write(msg["content"])

    user_input = st.chat_input(PLACEHOLDER_TEXT.get(language, "Type your question..."))

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar=AVATARS["user"]):
            st.write(user_input)

        with st.chat_message("assistant", avatar=AVATARS["assistant"]):
            placeholder = st.empty()
            placeholder.markdown("_Thinking..._")
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

# -----------------------------------------------------------
# TAB 4 — CONTACT
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
