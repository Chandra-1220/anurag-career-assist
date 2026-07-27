st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500;600;700&display=swap');

    /* ===========================================================
       1. DESIGN TOKENS (CSS custom properties — single source of truth)
       =========================================================== */
    :root {{
        color-scheme: light only;
        --navy: {NAVY};
        --navy-deep: {NAVY_DEEP};
        --gold: {GOLD};
        --cream: {CREAM};
        --slate: {SLATE};
        --teal: {TEAL};
        --green: {GREEN};
        --red: {RED};
        --amber: {AMBER};

        --surface: #ffffff;
        --surface-muted: #fbf8f1;
        --border: #e7e2d6;
        --border-strong: #d8d2c2;
        --text-muted: #6b7480;
        --placeholder: #8a8f98;

        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 14px;
        --radius-xl: 18px;

        --shadow-sm: 0 2px 6px rgba(11, 37, 69, 0.05);
        --shadow-md: 0 4px 14px rgba(11, 37, 69, 0.10);
        --shadow-lg: 0 8px 24px rgba(11, 37, 69, 0.16);

        --transition-fast: 0.15s ease;
        --transition-base: 0.25s cubic-bezier(0.4, 0, 0.2, 1);

        --font-display: 'Playfair Display', serif;
        --font-body: 'Inter', sans-serif;
    }}

    html, body {{ color-scheme: light only; }}
    html, body, [class*="css"] {{ font-family: var(--font-body); }}

    .stApp {{ background-color: var(--cream); }}

    /* ===========================================================
       2. BASE TEXT COLOR — apply once, broadly
       =========================================================== */
    .stApp, .stApp p, .stApp span, .stApp li, .stApp label,
    .stMarkdown, .stMarkdown p, .stMarkdown li,
    div[data-testid="stMetricValue"], div[data-testid="stMetricLabel"],
    div[data-testid="stCaptionContainer"],
    div[data-testid="stChatMessage"] p, div[data-testid="stChatMessage"] li {{
        color: var(--slate) !important;
    }}

    /* Smooth, subtle motion across the whole app rather than repeated per-element */
    .stApp * {{ transition: background-color var(--transition-fast), border-color var(--transition-fast),
                            box-shadow var(--transition-fast), transform var(--transition-fast), color var(--transition-fast); }}

    /* ===========================================================
       3. LAYOUT — page header / hero
       =========================================================== */
    .site-header {{
        background: linear-gradient(135deg, var(--navy-deep) 0%, var(--navy) 60%, var(--teal) 100%);
        padding: 2.6rem 2rem 2.2rem 2rem;
        border-radius: 0 0 var(--radius-xl) var(--radius-xl);
        margin-bottom: 1.5rem;
        box-shadow: var(--shadow-lg);
        position: relative;
        overflow: hidden;
    }}
    .site-header::after {{
        content: "";
        position: absolute; inset: 0;
        background: radial-gradient(circle at 85% -10%, rgba(201,162,75,0.16), transparent 55%);
        pointer-events: none;
    }}
    .site-header h1 {{
        font-family: var(--font-display); color: var(--gold) !important;
        font-size: 2.6rem; margin-bottom: 0.3rem; letter-spacing: 0.3px;
    }}
    .site-header p, .site-header p * {{
        color: var(--cream) !important; font-size: 1.05rem; font-weight: 500;
        letter-spacing: 0.5px; text-transform: uppercase; margin: 0;
    }}
    .site-header .tagline, .site-header .tagline * {{
        color: var(--cream) !important; text-transform: none; font-weight: 400;
        font-size: 1rem; margin-top: 0.6rem; letter-spacing: 0; line-height: 1.55rem;
    }}

    /* Section titles used throughout every tab */
    .section-title {{
        font-family: var(--font-display); color: var(--navy); font-size: 1.7rem;
        border-left: 5px solid var(--gold); padding-left: 0.7rem; margin: 1.4rem 0 1rem 0;
    }}

    /* ===========================================================
       4. SIDEBAR
       =========================================================== */
    section[data-testid="stSidebar"] {{ background-color: var(--navy-deep); }}
    section[data-testid="stSidebar"] * {{ color: #f0f6ff !important; }}
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {{ color: #f0f6ff !important; }}
    section[data-testid="stSidebar"] hr {{ border-color: rgba(240,246,255,0.15); }}
    section[data-testid="stSidebar"] .stButton button {{
        background: rgba(201,162,75,0.12) !important; color: var(--gold) !important;
        border: 1px solid rgba(201,162,75,0.45) !important; border-radius: var(--radius-md) !important;
        font-weight: 600 !important;
    }}
    section[data-testid="stSidebar"] .stButton button:hover {{
        background: var(--gold) !important; color: var(--navy-deep) !important;
        border-color: var(--gold) !important; transform: translateY(-1px);
        box-shadow: 0 4px 10px rgba(0,0,0,0.25);
    }}
    section[data-testid="stSidebar"] div[data-baseweb="radio"] label {{
        border-radius: var(--radius-sm); padding: 0.15rem 0.3rem;
    }}
    section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {{
        background: rgba(255,255,255,0.06);
    }}

    /* ===========================================================
       5. REUSABLE CARD COMPONENTS
       =========================================================== */
    /* Generic hoverable surface card — base for theory/stat/roadmap/job cards */
    .theory-card, .stat-box, .roadmap-card, .job-card, .empty-chat-card, .feature-banner {{
        background: var(--surface);
        border: 1px solid var(--border);
        box-shadow: var(--shadow-sm);
    }}

    .theory-card {{
        border-radius: var(--radius-lg);
        padding: 1.1rem 1.3rem; margin-bottom: 1rem;
    }}
    .theory-card:hover, .job-card:hover, .roadmap-card:hover, .stat-box:hover {{
        transform: translateY(-3px);
        box-shadow: var(--shadow-md);
        border-color: var(--border-strong);
    }}
    .theory-card h4 {{ color: var(--navy); margin-bottom: 0.4rem; font-family: var(--font-display); }}
    .theory-card p, .theory-card li {{ color: var(--slate); font-size: 0.95rem; line-height: 1.5rem; }}

    .stat-box {{
        border-radius: var(--radius-md); padding: 1rem; text-align: center;
    }}
    .stat-box .num {{
        font-family: var(--font-display); color: var(--gold); font-size: 1.8rem; font-weight: 700;
    }}
    .stat-box .label {{ color: var(--slate); font-size: 0.85rem; }}

    .feature-banner {{
        background: linear-gradient(120deg, var(--surface) 0%, var(--surface-muted) 100%);
        border-left: 5px solid var(--gold);
        border-radius: var(--radius-md); padding: 0.9rem 1.2rem; margin-bottom: 1.2rem;
        color: var(--slate); font-size: 0.95rem;
    }}

    .roadmap-card {{
        border-left: 5px solid var(--teal);
        border-radius: var(--radius-md); padding: 1rem 1.2rem; margin-bottom: 0.9rem;
    }}
    .roadmap-week {{
        display: inline-block; background: var(--navy); color: var(--gold) !important;
        font-weight: 700; border-radius: var(--radius-sm); padding: 0.15rem 0.6rem;
        font-family: var(--font-display); margin-right: 0.5rem;
    }}

    .job-card {{
        border-radius: var(--radius-lg); border-top: 4px solid var(--gold);
        padding: 1rem 1.2rem; margin-bottom: 0.9rem;
    }}
    .job-card h4 {{ color: var(--navy); margin: 0 0 0.3rem 0; }}
    .match-pill {{
        float: right; background: var(--navy); color: var(--gold) !important; font-weight: 700;
        padding: 0.2rem 0.7rem; border-radius: 999px; font-size: 0.85rem;
    }}

    .interview-q {{
        background: linear-gradient(135deg, var(--navy-deep) 0%, var(--navy) 100%);
        color: var(--cream) !important; border-radius: var(--radius-lg); padding: 1rem 1.3rem;
        margin-bottom: 1rem; font-size: 1.05rem; box-shadow: var(--shadow-sm);
    }}
    .interview-q * {{ color: var(--cream) !important; }}

    /* ===========================================================
       6. BADGES & CHIPS
       =========================================================== */
    .score-badge {{
        display: inline-block; padding: 0.35rem 0.9rem; border-radius: 999px;
        font-weight: 700; font-size: 0.95rem; color: #fff;
    }}
    .chip {{
        display: inline-block; padding: 0.3rem 0.75rem; margin: 0.2rem;
        border-radius: 999px; font-size: 0.85rem; font-weight: 600;
        transition: transform var(--transition-fast);
    }}
    .chip:hover {{ transform: translateY(-1px); }}
    .chip-yes {{ background: #e6f4ea; color: var(--green); border: 1px solid #bfe3c9; }}
    .chip-no {{ background: #fdecea; color: var(--red); border: 1px solid #f4c7c1; }}

    /* ===========================================================
       7. TABS
       =========================================================== */
    button[data-baseweb="tab"] {{
        border-radius: var(--radius-sm) var(--radius-sm) 0 0;
    }}
    button[data-baseweb="tab"], button[data-baseweb="tab"] * {{
        color: var(--navy) !important; font-weight: 600 !important;
    }}
    button[data-baseweb="tab"]:hover {{ background: rgba(11,37,69,0.05); }}
    button[data-baseweb="tab"][aria-selected="true"],
    button[data-baseweb="tab"][aria-selected="true"] * {{ color: var(--gold) !important; }}
    div[data-baseweb="tab-highlight"] {{ background-color: var(--gold) !important; }}

    /* ===========================================================
       8. BUTTONS (default Streamlit buttons)
       =========================================================== */
    .stButton button {{
        border-radius: var(--radius-md) !important;
        font-weight: 600 !important;
        transition: transform var(--transition-fast), box-shadow var(--transition-fast) !important;
    }}
    .stButton button:hover {{ transform: translateY(-1px); box-shadow: var(--shadow-sm); }}
    .stButton button:active {{ transform: translateY(0); }}
    button[kind="primary"], button[data-testid="baseButton-primary"] {{
        background: linear-gradient(135deg, var(--navy) 0%, var(--teal) 100%) !important;
        border: none !important; color: var(--cream) !important;
    }}
    button[kind="primary"]:hover, button[data-testid="baseButton-primary"]:hover {{
        box-shadow: 0 6px 16px rgba(11,37,69,0.3) !important;
    }}

    /* Suggestion chip buttons (chat quick-start row) */
    div[data-testid="stHorizontalBlock"] .stButton button {{
        background: var(--surface) !important; color: var(--navy) !important; border: 1px solid var(--gold) !important;
        border-radius: 999px !important; font-size: 0.82rem !important; font-weight: 600 !important;
        padding: 0.35rem 0.9rem !important; box-shadow: none !important; white-space: normal !important;
    }}
    div[data-testid="stHorizontalBlock"] .stButton button:hover {{
        background: var(--navy) !important; color: var(--gold) !important; border: 1px solid var(--navy) !important;
    }}

    /* ===========================================================
       9. CHAT ASSISTANT
       =========================================================== */
    .chat-hero {{
        background: linear-gradient(135deg, var(--navy-deep) 0%, var(--navy) 55%, var(--teal) 100%);
        border-radius: 16px; padding: 1.4rem 1.6rem; margin-bottom: 1.1rem;
        box-shadow: var(--shadow-lg);
        display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 0.8rem;
    }}
    .chat-hero .chat-hero-text h3 {{
        color: var(--gold) !important; font-family: var(--font-display); margin: 0 0 0.2rem 0; font-size: 1.4rem;
    }}
    .chat-hero .chat-hero-text p {{ color: var(--cream) !important; margin: 0; font-size: 0.92rem; }}
    .chat-hero .chat-hero-emoji {{ font-size: 2.4rem; }}
    .chat-status-pill {{
        display: inline-flex; align-items: center; gap: 0.4rem; background: rgba(201,162,75,0.18);
        border: 1px solid var(--gold); color: var(--gold) !important; padding: 0.3rem 0.8rem; border-radius: 999px;
        font-size: 0.8rem; font-weight: 600;
    }}
    .chat-status-dot {{
        width: 8px; height: 8px; border-radius: 50%; background: #4CD964; display: inline-block;
        box-shadow: 0 0 0 0 rgba(76,217,100,0.6); animation: pulse-dot 1.6s infinite;
    }}

    .empty-chat-card {{
        border: 1px dashed var(--border-strong); border-radius: 16px;
        padding: 1.6rem; text-align: center; margin-bottom: 1rem;
    }}
    .empty-chat-card .big-emoji {{ font-size: 2.4rem; margin-bottom: 0.4rem; }}
    .empty-chat-card h4 {{ color: var(--navy); font-family: var(--font-display); margin-bottom: 0.3rem; }}
    .empty-chat-card p {{ color: var(--slate); font-size: 0.92rem; margin-bottom: 0; }}

    /* Chat bubbles — align user right, assistant left, distinct colors */
    div[data-testid="stChatMessage"] {{
        background-color: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-lg);
        padding: 0.6rem 0.9rem; margin-bottom: 0.4rem;
        max-width: 88%;
        box-shadow: 0 2px 8px rgba(11,37,69,0.06);
    }}
    div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {{
        margin-left: auto; margin-right: 0;
        background: linear-gradient(135deg, var(--navy) 0%, var(--teal) 100%) !important;
        border: none !important; border-bottom-right-radius: 4px !important;
        flex-direction: row-reverse;
    }}
    div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) p,
    div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) li,
    div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) span {{
        color: var(--cream) !important;
    }}
    div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {{
        margin-right: auto; margin-left: 0;
        border-left: 4px solid var(--gold) !important; border-bottom-left-radius: 4px !important;
    }}

    div[data-testid="stChatInput"] textarea,
    div[data-testid="stChatInputTextArea"] textarea,
    .stChatInput textarea {{
        background-color: var(--surface) !important; color: var(--slate) !important;
        caret-color: var(--slate) !important; border: 1px solid var(--border-strong) !important;
        border-radius: var(--radius-md) !important;
    }}
    div[data-testid="stChatInput"] textarea::placeholder,
    .stChatInput textarea::placeholder {{ color: var(--placeholder) !important; opacity: 1 !important; }}
    div[data-testid="stChatInput"] {{ background-color: var(--surface) !important; border-radius: var(--radius-md) !important; }}

    .typing-indicator {{ display: inline-flex; gap: 4px; align-items: center; padding: 0.2rem 0; }}
    .typing-indicator span {{
        width: 7px; height: 7px; border-radius: 50%; background: var(--teal); display: inline-block;
        animation: typing-bounce 1.2s infinite ease-in-out;
    }}
    .typing-indicator span:nth-child(2) {{ animation-delay: 0.2s; }}
    .typing-indicator span:nth-child(3) {{ animation-delay: 0.4s; }}

    /* ===========================================================
       10. KEYFRAME ANIMATIONS
       =========================================================== */
    @keyframes pulse-dot {{
        0% {{ box-shadow: 0 0 0 0 rgba(76,217,100,0.6); }}
        70% {{ box-shadow: 0 0 0 6px rgba(76,217,100,0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(76,217,100,0); }}
    }}
    @keyframes typing-bounce {{
        0%, 60%, 100% {{ transform: translateY(0); opacity: 0.5; }}
        30% {{ transform: translateY(-5px); opacity: 1; }}
    }}
    @keyframes fade-in-up {{
        from {{ opacity: 0; transform: translateY(6px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    .site-header, .theory-card, .job-card, .roadmap-card, .stat-box, .feature-banner {{
        animation: fade-in-up 0.4s ease both;
    }}

    /* ===========================================================
       11. FORM CONTROLS — always pair a background with its text color
       =========================================================== */
    .stTextInput input, .stTextArea textarea, .stNumberInput input,
    .stSelectbox div[data-baseweb="select"] > div,
    .stMultiSelect div[data-baseweb="select"] > div {{
        background-color: var(--surface) !important; color: var(--slate) !important;
        border: 1px solid var(--border-strong) !important; caret-color: var(--slate) !important;
        border-radius: var(--radius-sm) !important;
    }}
    .stTextInput input:focus, .stTextArea textarea:focus,
    .stSelectbox div[data-baseweb="select"] > div:focus-within,
    .stMultiSelect div[data-baseweb="select"] > div:focus-within {{
        border-color: var(--gold) !important; box-shadow: 0 0 0 2px rgba(201,162,75,0.2) !important;
    }}
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {{
        color: var(--placeholder) !important; opacity: 1 !important;
    }}
    /* Dropdown / multiselect popover menus (BaseWeb renders these in a portal, outside .stApp) */
    div[data-baseweb="popover"] ul, div[data-baseweb="popover"] li,
    div[data-baseweb="menu"] {{
        background-color: var(--surface) !important; color: var(--slate) !important;
    }}
    div[data-baseweb="popover"] li:hover {{ background-color: #f2eee2 !important; }}
    /* Multiselect selected-item tags */
    span[data-baseweb="tag"] {{ background-color: var(--navy) !important; color: var(--cream) !important; }}
    span[data-baseweb="tag"] * {{ color: var(--cream) !important; }}

    /* Slider */
    div[data-testid="stSlider"] div[data-baseweb="slider"] div[role="slider"] {{
        background-color: var(--gold) !important;
    }}

    /* Radio / checkbox labels inside the main app (not sidebar) */
    section[data-testid="stMain"] div[data-testid="stRadio"] label,
    section[data-testid="stMain"] div[data-testid="stCheckbox"] label {{
        color: var(--slate) !important;
    }}

    /* File uploader dropzone */
    div[data-testid="stFileUploaderDropzone"] {{
        background-color: var(--surface) !important; border: 1px dashed var(--border-strong) !important;
        border-radius: var(--radius-md) !important;
    }}
    div[data-testid="stFileUploaderDropzone"] * {{ color: var(--slate) !important; }}
    div[data-testid="stFileUploaderDropzone"]:hover {{ border-color: var(--gold) !important; }}

    /* Expander */
    div[data-testid="stExpander"] {{
        background-color: var(--surface) !important; border: 1px solid var(--border) !important;
        border-radius: var(--radius-md) !important;
    }}
    div[data-testid="stExpander"] * {{ color: var(--slate) !important; }}

    /* Alerts (st.info / st.warning / st.error / st.success) — force light-theme-safe pairs */
    div[data-testid="stAlert"] {{
        background-color: var(--surface) !important; border: 1px solid var(--border) !important;
        border-radius: var(--radius-md) !important;
    }}
    div[data-testid="stAlert"] p, div[data-testid="stAlert"] span, div[data-testid="stAlert"] div {{
        color: var(--slate) !important;
    }}

    /* Progress bars (score breakdown) */
    div[data-testid="stProgress"] div[role="progressbar"] > div {{
        background: linear-gradient(90deg, var(--teal), var(--gold)) !important;
    }}

    /* Metrics */
    div[data-testid="stMetric"] {{
        background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-md);
        padding: 0.6rem 0.8rem;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)
