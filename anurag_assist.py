import streamlit as st
from openai import OpenAI

# ---------------------------------------------------------
# Page config (must be first Streamlit call)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Anurag University Career Assistant",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# Custom styling
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
    }
    .main-header {
        text-align: center;
        padding: 1.2rem 1rem 0.5rem 1rem;
    }
    .main-header h1 {
        color: #ffffff;
        font-size: 2.1rem;
        margin-bottom: 0.2rem;
    }
    .main-header p {
        color: #cfe8ff;
        font-size: 1rem;
    }
    section[data-testid="stSidebar"] {
        background-color: #10222f;
    }
    section[data-testid="stSidebar"] * {
        color: #f0f6ff !important;
    }
    div[data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.06);
        border-radius: 14px;
        padding: 0.6rem 0.9rem;
        margin-bottom: 0.4rem;
    }
    .stChatInput textarea {
        border-radius: 12px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Language configuration
# ---------------------------------------------------------
LANGUAGE_PROMPTS = {
    "English": (
        "Reply strictly in clear, simple English. Avoid using any other language."
    ),
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

LANGUAGE_ICON = {
    "English": "🇬🇧",
    "Telugu": "🇮🇳",
    "Hinglish": "🗣️",
    "Telgish": "💬",
}

BASE_SYSTEM_PROMPT = (
    "You are a placement and career assistant for students in Bhilwara. "
    "Guide them for IT jobs, government jobs, internships, resume building, "
    "communication skills, coding basics, interview preparation, and practical "
    "career paths suitable for students from small towns, degree colleges, and "
    "rural backgrounds. Give realistic, actionable, step-by-step advice for "
    "Bhilwara students. Keep answers concise and practical."
)


def build_system_message(language: str) -> dict:
    return {
        "role": "system",
        "content": f"{BASE_SYSTEM_PROMPT} {LANGUAGE_PROMPTS[language]}",
    }


# ---------------------------------------------------------
# Sidebar: API key + language selector + reset
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Settings")

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
    st.caption(
        "Tip: switching the language option starts a fresh chat in that language."
    )

# ---------------------------------------------------------
# API key
# ---------------------------------------------------------
api_key = st.secrets.get("OPENAI_API_KEY")
if not api_key:
    st.error("❌ OPENAI_API_KEY not found in Streamlit Secrets.")
    st.stop()
client = OpenAI(api_key=api_key)

# ---------------------------------------------------------
# Header
# ---------------------------------------------------------
st.markdown(
    """
    <div class="main-header">
        <h1>🎓 Anurag University Career Assistant</h1>
        <p>Your personalised career guide — jobs, internships, resumes &amp; interviews</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Session state init / language switch handling
# ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [build_system_message(language)]
    st.session_state.active_language = language

if st.session_state.get("active_language") != language:
    # Language changed via sidebar -> start a fresh conversation in new language
    st.session_state.messages = [build_system_message(language)]
    st.session_state.active_language = language
    st.rerun()

# ---------------------------------------------------------
# Display chat history (skip system message)
# ---------------------------------------------------------
AVATARS = {"user": "🧑‍🎓", "assistant": "🎓"}

for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    with st.chat_message(msg["role"], avatar=AVATARS.get(msg["role"])):
        st.write(msg["content"])

# ---------------------------------------------------------
# Chat input
# ---------------------------------------------------------
placeholder_text = {
    "English": "Ask something about careers, jobs, or placements...",
    "Telugu": "కెరీర్, జాబ్స్, ప్లేస్‌మెంట్స్ గురించి అడగండి...",
    "Hinglish": "Career, jobs ya placements ke baare mein kuch pucho...",
    "Telgish": "Career, jobs, placements gurinchi emaina adagandi...",
}

user_input = st.chat_input(placeholder_text.get(language, "Type your question..."))

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
            st.session_state.messages.append(
                {"role": "assistant", "content": ai_reply}
            )
        except Exception as e:
            placeholder.write(f"⚠️ Error: {str(e)}")
