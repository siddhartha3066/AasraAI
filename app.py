import os
import re

import streamlit as st
from dotenv import load_dotenv
from groq import Groq


# Load environment variables
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")


# Page configuration
st.set_page_config(
    page_title="AasraAI",
    page_icon="🤝",
    layout="wide"
)


# ---------------------------------------------------------------------------
# Design system
# ---------------------------------------------------------------------------
# Palette
#   Ink        #1B2140   text
#   Mist       #F4F6FB   page background
#   Indigo     #4F46E5   Understand
#   Teal       #0D9488   Recommend
#   Amber      #D97706   Act
# Typeface: Plus Jakarta Sans (falls back to system fonts if offline)

STYLES = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

:root {
    --ink: #1B2140;
    --ink-soft: #5B6385;
    --mist: #F4F6FB;
    --line: #E1E5F0;
    --indigo: #4F46E5;
    --indigo-tint: #EEEFFE;
    --teal: #0D9488;
    --teal-tint: #E3F6F3;
    --amber: #D97706;
    --amber-tint: #FEF1DC;
}

/* Base ------------------------------------------------------------------ */
html, body, .stApp, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont,
                 'Segoe UI', Roboto, sans-serif;
}
.stApp {
    background:
        radial-gradient(900px 400px at 0% 0%, #E8EAFE 0%, transparent 60%),
        radial-gradient(800px 400px at 100% 0%, #DDF4F0 0%, transparent 55%),
        var(--mist);
    color: var(--ink);
}
.stApp p, .stApp li, .stApp span, .stApp label, .stApp h1, .stApp h2,
.stApp h3, .stApp h4 {
    color: var(--ink);
}
.block-container {
    max-width: 980px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}

/* Hide default Streamlit chrome */
#MainMenu, footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }

/* Hero ------------------------------------------------------------------ */
.hero {
    background: linear-gradient(125deg, #2A2F7A 0%, #4338CA 45%, #0F766E 100%);
    border-radius: 24px;
    padding: 2.6rem 2.4rem;
    box-shadow: 0 18px 40px -18px rgba(67, 56, 202, 0.55);
}
.hero * { color: #FFFFFF !important; }
.hero-brand {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-size: 2.5rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1.1;
    margin: 0;
}
.hero-brand .logo {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 3.2rem;
    height: 3.2rem;
    font-size: 1.7rem;
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.16);
    border: 1px solid rgba(255, 255, 255, 0.28);
}
.hero-tagline {
    font-size: 1.35rem;
    font-weight: 600;
    margin: 1rem 0 0.4rem 0;
    letter-spacing: -0.01em;
}
.hero-copy {
    max-width: 560px;
    font-size: 1rem;
    line-height: 1.6;
    opacity: 0.88;
    margin: 0;
}
.hero-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 1.4rem;
}
.hero-pill {
    font-size: 0.85rem;
    font-weight: 600;
    padding: 0.35rem 0.8rem;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.14);
    border: 1px solid rgba(255, 255, 255, 0.25);
}

/* Workflow -------------------------------------------------------------- */
.flow {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
    gap: 1rem;
    margin: 1.6rem 0 0.4rem 0;
}
.flow-step {
    position: relative;
    display: flex;
    gap: 0.9rem;
    align-items: flex-start;
    background: #FFFFFF;
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 1.1rem 1.1rem;
    box-shadow: 0 8px 22px -16px rgba(27, 33, 64, 0.35);
}
.flow-icon {
    flex: 0 0 auto;
    width: 2.6rem;
    height: 2.6rem;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
}
.flow-step.s1 .flow-icon { background: var(--indigo-tint); }
.flow-step.s2 .flow-icon { background: var(--teal-tint); }
.flow-step.s3 .flow-icon { background: var(--amber-tint); }
.flow-step.s1 { border-top: 3px solid var(--indigo); }
.flow-step.s2 { border-top: 3px solid var(--teal); }
.flow-step.s3 { border-top: 3px solid var(--amber); }
.flow-label {
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--ink-soft) !important;
    margin: 0;
}
.flow-title {
    font-size: 1.05rem;
    font-weight: 700;
    margin: 0.05rem 0 0.25rem 0;
}
.flow-text {
    font-size: 0.9rem;
    line-height: 1.5;
    color: var(--ink-soft) !important;
    margin: 0;
}

/* Cards (bordered containers) ------------------------------------------ */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF;
    border: 1px solid var(--line) !important;
    border-radius: 20px !important;
    box-shadow: 0 12px 30px -20px rgba(27, 33, 64, 0.4);
    padding: 0.4rem 0.6rem;
}

.section-title {
    font-size: 1.15rem;
    font-weight: 700;
    letter-spacing: -0.01em;
    margin: 0 0 0.15rem 0;
}
.section-sub {
    font-size: 0.92rem;
    color: var(--ink-soft) !important;
    margin: 0 0 0.6rem 0;
}

/* Input ----------------------------------------------------------------- */
.stTextArea label p {
    font-weight: 600;
    font-size: 0.95rem;
    color: var(--ink) !important;
}
.stTextArea textarea {
    background: #FBFCFE !important;
    color: var(--ink) !important;
    border: 1px solid #D5DAEA !important;
    border-radius: 14px !important;
    font-size: 1rem;
    line-height: 1.55;
    padding: 0.9rem 1rem;
}
.stTextArea textarea::placeholder { color: #8A91AE !important; }
.stTextArea textarea:focus {
    border-color: var(--indigo) !important;
    box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.18) !important;
}

/* Primary button -------------------------------------------------------- */
.stButton > button[kind="primary"],
button[data-testid="stBaseButton-primary"] {
    background: linear-gradient(120deg, #4F46E5 0%, #0D9488 100%);
    color: #FFFFFF;
    border: none;
    border-radius: 12px;
    padding: 0.65rem 1.6rem;
    font-weight: 700;
    font-size: 1rem;
    box-shadow: 0 10px 22px -10px rgba(79, 70, 229, 0.7);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.stButton > button[kind="primary"]:hover,
button[data-testid="stBaseButton-primary"]:hover {
    color: #FFFFFF;
    transform: translateY(-1px);
    box-shadow: 0 14px 26px -10px rgba(79, 70, 229, 0.8);
}
.stButton > button[kind="primary"]:focus-visible,
button[data-testid="stBaseButton-primary"]:focus-visible {
    outline: 3px solid rgba(79, 70, 229, 0.35);
    outline-offset: 2px;
}
.stButton > button[kind="primary"] p,
button[data-testid="stBaseButton-primary"] p { color: #FFFFFF !important; }

/* Results --------------------------------------------------------------- */
.results-head {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin: 2rem 0 0.9rem 0;
}
.results-head h2 {
    font-size: 1.4rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    margin: 0;
    padding: 0;
}
.res-head {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 0.4rem;
}
.res-icon {
    width: 2.6rem;
    height: 2.6rem;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
}
.res-title {
    font-size: 1.2rem;
    font-weight: 800;
    letter-spacing: -0.01em;
    line-height: 1.2;
}
.res-sub {
    font-size: 0.88rem;
    color: var(--ink-soft) !important;
}
.res-understand .res-icon { background: var(--indigo-tint); }
.res-recommend .res-icon { background: var(--teal-tint); }
.res-act .res-icon { background: var(--amber-tint); }
.res-understand .res-title { color: var(--indigo) !important; }
.res-recommend .res-title { color: var(--teal) !important; }
.res-act .res-title { color: var(--amber) !important; }

/* Readable markdown inside result cards */
div[data-testid="stMarkdownContainer"] p,
div[data-testid="stMarkdownContainer"] li {
    line-height: 1.65;
}

/* Footer note ----------------------------------------------------------- */
.note {
    text-align: center;
    font-size: 0.85rem;
    color: var(--ink-soft) !important;
    margin-top: 2.2rem;
}

/* Small screens --------------------------------------------------------- */
@media (max-width: 640px) {
    .block-container { padding-top: 1.2rem; }
    .hero { padding: 1.8rem 1.4rem; border-radius: 20px; }
    .hero-brand { font-size: 2rem; }
    .hero-tagline { font-size: 1.15rem; }
}

@media (prefers-reduced-motion: reduce) {
    * { transition: none !important; }
}
</style>
"""


def html(markup: str) -> str:
    """Collapse indentation/newlines so Markdown never treats HTML as code."""
    return "".join(line.strip() for line in markup.splitlines())


st.markdown(STYLES, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Result presentation helpers
# ---------------------------------------------------------------------------
SECTIONS = [
    {
        "key": "UNDERSTAND",
        "css": "res-understand",
        "icon": "🔍",
        "title": "Understand",
        "subtitle": "What's going on and what matters",
    },
    {
        "key": "RECOMMEND",
        "css": "res-recommend",
        "icon": "🧭",
        "title": "Recommend",
        "subtitle": "Your best next steps",
    },
    {
        "key": "ACT",
        "css": "res-act",
        "icon": "✍️",
        "title": "Act",
        "subtitle": "Ready-to-use drafts and checklists",
    },
]


def split_sections(text: str):
    """Split the model's markdown into its UNDERSTAND / RECOMMEND / ACT parts."""
    pattern = re.compile(
        r"^[ \t]*#{1,6}[ \t]*(UNDERSTAND|RECOMMEND|ACT)\b[^\n]*(?:\n|$)",
        re.IGNORECASE | re.MULTILINE,
    )
    matches = list(pattern.finditer(text))

    if not matches:
        return "", {}

    intro = text[: matches[0].start()].strip()
    found = {}

    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        found.setdefault(match.group(1).upper(), text[match.end():end].strip())

    return intro, found


def render_response(answer: str):
    """Show the AI answer as three workflow cards (falls back to plain markdown)."""
    st.markdown(
        html("""
        <div class="results-head">
            <span style="font-size:1.5rem">🤖</span>
            <h2>AasraAI's Response</h2>
        </div>
        """),
        unsafe_allow_html=True,
    )

    intro, found = split_sections(answer)

    if not found:
        with st.container(border=True):
            st.markdown(answer)
        return

    if intro:
        st.markdown(intro)

    for section in SECTIONS:
        body = found.get(section["key"])

        if not body:
            continue

        with st.container(border=True):
            st.markdown(
                html(f"""
                <div class="res-head {section['css']}">
                    <div class="res-icon">{section['icon']}</div>
                    <div>
                        <div class="res-title">{section['title']}</div>
                        <div class="res-sub">{section['subtitle']}</div>
                    </div>
                </div>
                """),
                unsafe_allow_html=True,
            )
            st.markdown(body)


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown(
    html("""
    <div class="hero">
        <h1 class="hero-brand"><span class="logo">🤝</span>AasraAI</h1>
        <p class="hero-tagline">Understand. Recommend. Act.</p>
        <p class="hero-copy">
            An AI-powered support system that helps people understand
            problems, find solutions, and take action.
        </p>
        <div class="hero-pills">
            <span class="hero-pill">💬 Plain-language answers</span>
            <span class="hero-pill">🧭 Practical next steps</span>
            <span class="hero-pill">📄 Drafts you can use</span>
        </div>
    </div>
    """),
    unsafe_allow_html=True,
)


# Workflow overview
st.markdown(
    html("""
    <div class="flow">
        <div class="flow-step s1">
            <div class="flow-icon">🔍</div>
            <div>
                <p class="flow-label">Step 1</p>
                <p class="flow-title">Understand</p>
                <p class="flow-text">We break down your situation and pick out the details that matter.</p>
            </div>
        </div>
        <div class="flow-step s2">
            <div class="flow-icon">🧭</div>
            <div>
                <p class="flow-label">Step 2</p>
                <p class="flow-title">Recommend</p>
                <p class="flow-text">You get clear, practical steps you can follow right away.</p>
            </div>
        </div>
        <div class="flow-step s3">
            <div class="flow-icon">✍️</div>
            <div>
                <p class="flow-label">Step 3</p>
                <p class="flow-title">Act</p>
                <p class="flow-text">We draft the letter, email, or checklist you need to move forward.</p>
            </div>
        </div>
    </div>
    """),
    unsafe_allow_html=True,
)

st.write("")


# ---------------------------------------------------------------------------
# User input
# ---------------------------------------------------------------------------
with st.container(border=True):

    st.markdown(
        html("""
        <p class="section-title">What do you need help with?</p>
        <p class="section-sub">
            Share what happened, who is involved, and any deadlines.
            The more detail you give, the more useful the answer.
        </p>
        """),
        unsafe_allow_html=True,
    )

    problem = st.text_area(
        "Tell AasraAI about your problem",
        placeholder=(
            "Example: My scholarship application was rejected "
            "and I don't know what to do next..."
        ),
        height=170
    )

    get_help = st.button("Get Help", type="primary")


# ---------------------------------------------------------------------------
# Process problem
# ---------------------------------------------------------------------------
if get_help:

    if not problem.strip():

        st.warning("Please describe your problem first.")

    elif not api_key:

        st.error(
            "GROQ_API_KEY is not configured. "
            "Please check your .env file."
        )

    else:

        try:

            # Connect to Groq
            client = Groq(api_key=api_key)

            # Ask the AI
            with st.spinner("AasraAI is working on your problem..."):

                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {
                            "role": "system",
                            "content": """
You are AasraAI, an AI-powered support assistant.

Your purpose is to help people move from a problem
to a practical action.

Always structure your response into three sections:

## UNDERSTAND
Explain what the user's problem appears to be
and identify important details.

## RECOMMEND
Give clear, practical next steps the user can follow.

## ACT
Create an actionable output when appropriate.

Examples include:
- complaint letters
- appeal letters
- applications
- emails
- checklists
- follow-up messages

Never claim that you contacted an organization,
submitted a form, booked an appointment, or completed
an external action unless an actual external tool
has performed that action.

If important information is missing, clearly explain
what information the user should provide.

Be empathetic, practical, and concise.
"""
                        },
                        {
                            "role": "user",
                            "content": problem
                        }
                    ],
                    temperature=0.3,
                    max_completion_tokens=1500
                )

            # Get AI response
            answer = response.choices[0].message.content

            # Display result
            render_response(answer)

        except Exception as e:

            st.error(f"Something went wrong: {e}")


# Footer
st.markdown(
    html("""
    <p class="note">
        AasraAI offers general guidance, not legal, medical, or financial advice.
        Review any draft before you send it.
    </p>
    """),
    unsafe_allow_html=True,
)