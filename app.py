import streamlit as st
from backend.ai_engine import generate_notes
from backend.file_reader import extract_text_from_file

# ── PAGE CONFIG ──────────────────────────────────────────────
st.set_page_config(
    page_title="RevisionAI – Exam Prep Tool",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CUSTOM CSS ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Sora', sans-serif; }

/* Background */
.stApp { background-color: #0c0c14; color: #ede9ff; }

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #14141e;
    border-right: 1px solid rgba(255,255,255,0.07);
}

/* Hide default header */
#MainMenu, header, footer { visibility: hidden; }

/* Custom header */
.custom-header {
    background: linear-gradient(135deg, #14141e, #1b1b28);
    border: 1px solid rgba(124,106,247,0.25);
    border-radius: 14px;
    padding: 20px 28px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 14px;
}
.header-title { font-size: 26px; font-weight: 700; color: #ede9ff; margin: 0; }
.header-title span { color: #a78bfa; }
.header-sub { font-size: 13px; color: #8880b8; margin: 4px 0 0; }

/* Cards */
.info-card {
    background: #14141e;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 16px;
}

/* Output box */
.output-box {
    background: #14141e;
    border: 1px solid rgba(124,106,247,0.3);
    border-radius: 14px;
    padding: 24px 28px;
    line-height: 1.8;
    color: #ddd8ff;
    font-size: 15px;
    min-height: 300px;
}

/* Mode badge */
.badge-detailed { background: rgba(52,211,153,0.13); color: #34d399; border: 1px solid rgba(52,211,153,0.3); padding: 3px 12px; border-radius: 99px; font-size: 11px; font-weight: 700; letter-spacing: 1px; }
.badge-mcq      { background: rgba(251,191,36,0.13);  color: #fbbf24; border: 1px solid rgba(251,191,36,0.3);  padding: 3px 12px; border-radius: 99px; font-size: 11px; font-weight: 700; letter-spacing: 1px; }
.badge-exam     { background: rgba(248,113,113,0.13); color: #f87171; border: 1px solid rgba(248,113,113,0.3); padding: 3px 12px; border-radius: 99px; font-size: 11px; font-weight: 700; letter-spacing: 1px; }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #7c6af7, #a78bfa) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    padding: 12px 28px !important;
    width: 100% !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.88 !important; }

/* Inputs */
.stTextArea textarea, .stTextInput input {
    background: #1b1b28 !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #ede9ff !important;
    font-family: 'Sora', sans-serif !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: #7c6af7 !important;
    box-shadow: 0 0 0 2px rgba(124,106,247,0.2) !important;
}

/* Select box */
.stSelectbox > div > div {
    background: #1b1b28 !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #ede9ff !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: #1b1b28;
    border: 2px dashed rgba(124,106,247,0.3);
    border-radius: 10px;
    padding: 12px;
}

/* Labels */
.stTextArea label, .stTextInput label, .stSelectbox label, .stFileUploader label {
    color: #8880b8 !important;
    font-size: 12px !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    font-weight: 600 !important;
}

/* Divider */
hr { border-color: rgba(255,255,255,0.07) !important; }

/* Success / error */
.stAlert { border-radius: 10px !important; }

/* Spinner */
.stSpinner > div { border-top-color: #7c6af7 !important; }

/* Sidebar labels */
[data-testid="stSidebar"] .stRadio label {
    color: #ede9ff !important;
    font-size: 14px !important;
}
[data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
    color: #8880b8;
}
</style>
""", unsafe_allow_html=True)


# ── HEADER ───────────────────────────────────────────────────
st.markdown("""
<div class="custom-header">
    <div style="font-size:36px">📚</div>
    <div>
        <div class="header-title">Revision<span>AI</span></div>
        <div class="header-sub">Last-Minute Exam Preparation Tool · Powered by Groq AI (Free)</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── SIDEBAR ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚡ Setup")
    st.markdown("<p style='color:#8880b8;font-size:12px'>Get your FREE key at<br><a href='https://console.groq.com' target='_blank' style='color:#a78bfa'>console.groq.com</a> → API Keys</p>", unsafe_allow_html=True)

    api_key = st.text_input(
        "GROQ API KEY",
        type="password",
        placeholder="gsk_...",
        help="Free forever — no credit card needed"
    )

    st.markdown("---")
    st.markdown("### 🤖 Model")
    model = st.selectbox(
        "AI MODEL",
        options=[
            "llama-3.3-70b-versatile",
            "mixtral-8x7b-32768",
            "llama3-8b-8192"
        ],
        format_func=lambda x: {
            "llama-3.3-70b-versatile": "LLaMA 3.3 70B (Best)",
            "mixtral-8x7b-32768":      "Mixtral 8x7B (Fast)",
            "llama3-8b-8192":          "LLaMA 3 8B (Fastest)"
        }[x]
    )

    st.markdown("---")
    st.markdown("### 📏 Output Length")
    length = st.selectbox(
        "LENGTH",
        options=["concise", "medium", "detailed"],
        index=1,
        format_func=lambda x: x.capitalize()
    )

    st.markdown("---")
    st.markdown("""
    <div style='font-size:11px;color:#5e5a80;text-align:center;line-height:1.6'>
        Built with ❤️ by <span style='color:#a78bfa;font-weight:700'>Your Name</span><br>
        Revision Notes Generator<br>
        Powered by Groq AI · Free
    </div>
    """, unsafe_allow_html=True)


# ── MAIN LAYOUT ───────────────────────────────────────────────
left_col, right_col = st.columns([1, 1], gap="large")

with left_col:

    # File Upload
    st.markdown("#### 📎 Upload Files *(Optional)*")
    uploaded_files = st.file_uploader(
        "SUPPORTED FORMATS",
        type=["pdf", "docx", "pptx", "txt", "md", "png", "jpg", "jpeg"],
        accept_multiple_files=True,
        help="Upload your notes, slides, or study material"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Topic Input
    st.markdown("#### ✏️ Topic / Prompt")
    topic = st.text_area(
        "ENTER YOUR TOPIC",
        placeholder="e.g. French Revolution — causes, key events, effects\n\nOr: Laws of Motion with examples\n\nOr paste your raw notes here...",
        height=150
    )
    st.caption("💡 Tip: Be specific for better results")

    st.markdown("<br>", unsafe_allow_html=True)

    # Mode Selection
    st.markdown("#### 🎛 Generation Mode")
    mode = st.radio(
        "SELECT MODE",
        options=["detailed", "mcq", "exam"],
        format_func=lambda x: {
            "detailed": "📖  Detailed Notes — Structured summaries & quick recall",
            "mcq":      "🧩  MCQ Quiz — 10 multiple choice questions with answers",
            "exam":     "🎯  Exam Mode — Predicted questions & model answers"
        }[x],
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Generate Button
    generate_clicked = st.button("✨  Generate Revision Notes", use_container_width=True)


# ── RIGHT COLUMN: OUTPUT ──────────────────────────────────────
with right_col:
    st.markdown("#### 📄 Output")

    badge_map = {
        "detailed": '<span class="badge-detailed">DETAILED NOTES</span>',
        "mcq":      '<span class="badge-mcq">MCQ QUIZ</span>',
        "exam":     '<span class="badge-exam">EXAM MODE</span>'
    }
    title_map = {
        "detailed": "📖 Revision Notes",
        "mcq":      "🧩 MCQ Practice Quiz",
        "exam":     "🎯 Predicted Exam Questions"
    }

    output_placeholder = st.empty()

    # Show placeholder until generate is clicked
    if "output_text" not in st.session_state:
        st.session_state.output_text = ""
    if "output_mode" not in st.session_state:
        st.session_state.output_mode = "detailed"

    if generate_clicked:
        # Validation
        if not api_key:
            st.error("⚠️ Please enter your Groq API key in the sidebar.")
        elif not topic and not uploaded_files:
            st.error("⚠️ Please enter a topic or upload at least one file.")
        else:
            # Extract text from files
            file_context = ""
            if uploaded_files:
                with st.spinner("📂 Reading uploaded files..."):
                    for f in uploaded_files:
                        try:
                            text = extract_text_from_file(f)
                            if text:
                                file_context += f"\n[File: {f.name}]\n{text[:4000]}\n"
                        except Exception as e:
                            st.warning(f"Could not read {f.name}: {e}")

            # Generate notes
            with st.spinner("🧠 AI is generating your notes..."):
                result = generate_notes(
                    api_key=api_key,
                    topic=topic,
                    mode=mode,
                    model=model,
                    length=length,
                    file_context=file_context
                )

            if result.get("success"):
                st.session_state.output_text = result["content"]
                st.session_state.output_mode = mode
                st.success("✅ Notes generated successfully!")
            else:
                st.error(f"❌ Error: {result.get('error', 'Unknown error')}")

    # Display output
    if st.session_state.output_text:
        current_mode = st.session_state.output_mode
        st.markdown(badge_map[current_mode], unsafe_allow_html=True)
        st.markdown(f"**{title_map[current_mode]}**")
        st.markdown("---")

        # Show the output in a scrollable text area
        st.markdown(
            f'<div class="output-box">{st.session_state.output_text.replace(chr(10), "<br>")}</div>',
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="⬇️ Download Notes",
                data=st.session_state.output_text,
                file_name=f"revision_notes_{current_mode}.txt",
                mime="text/plain",
                use_container_width=True
            )
        with col2:
            if st.button("🗑 Clear Output", use_container_width=True):
                st.session_state.output_text = ""
                st.rerun()
    else:
        st.markdown("""
        <div style="background:#14141e;border:1px dashed rgba(124,106,247,0.2);border-radius:14px;
                    padding:60px 28px;text-align:center;min-height:300px;
                    display:flex;flex-direction:column;align-items:center;justify-content:center;">
            <div style="font-size:52px;margin-bottom:16px">🧠</div>
            <div style="color:#8880b8;font-size:14px;max-width:260px;line-height:1.7">
                Enter a topic or upload your files,<br>choose a mode, and click<br>
                <strong style="color:#a78bfa">✨ Generate</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
