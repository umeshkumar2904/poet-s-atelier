import random
import streamlit as st
from database import init_db, save_or_update_poem, get_all_poems, delete_poem
from poetry_engine import analyze_poem, generate_book_plan
from book_exporter import build_book_docx

init_db()
st.set_page_config(
    page_title="Poet's Atelier — Luminous Verse & Anthology Studio",
    page_icon="🪶",
    layout="wide"
)

# --- CURATED POETIC QUOTES & DEMO VERSES ---
MUSE_QUOTES = [
    ("“A poet is, before anything else, a person who is passionately in love with language.”", "W.H. Auden"),
    ("“Poetry is when an emotion has found its thought and the thought has found words.”", "Robert Frost"),
    ("“Fill your paper with the breathings of your heart.”", "William Wordsworth"),
    ("“We make out of the quarrel with others, rhetoric, but of the quarrel with ourselves, poetry.”", "W.B. Yeats"),
]

SAMPLE_POEMS = {
    "Select a sample poem to test...": ("", ""),
    "Monsoon Over Old Delhi (Draft with Flaws)": (
        "Monsoon Over Old Delhi",
        "The heavy clouds gather in the sky so blue,\n"
        "Raindrops fall down upon the ancient street,\n"
        "I sit alone and think of only you,\n"
        "The thunder makes a very loud beat.\n\n"
        "Neon reflections shimmer in the puddle,\n"
        "While jasmine scents drift through the evening air,\n"
        "My tangled thoughts are caught inside a muddle,\n"
        "And golden lanterns flicker everywhere."
    ),
    "Sonnet to a Fading Star": (
        "Sonnet to a Fading Star",
        "Beyond the velvet curtain of the night,\n"
        "A solitary ember burns alone,\n"
        "Outliving kingdoms swallowed by the light,\n"
        "A silent sentinel on silver throne.\n\n"
        "Though centuries may dim thy amber grace,\n"
        "Thy ancient fire still guides the wandering sea,\n"
        "A fleeting spark across the void of space,\n"
        "That whispers songs of immortality."
    )
}

# --- VIBRANT JEWEL-TONE & GOLD GLASSMORPHISM CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@700&family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,400;1,600&family=Lora:ital,wght@0,400;0,500;1,400&display=swap');

/* Transparent Streamlit Shell */
[data-testid="stAppViewContainer"] {
    background: transparent !important;
}
[data-testid="stHeader"] {
    background: rgba(19, 13, 22, 0.45) !important;
    backdrop-filter: blur(12px);
}

/* Vibrant HD Moving Velvet & Gold Aurora Canvas */
.velvet-canvas {
    position: fixed;
    inset: 0;
    z-index: -2;
    background: linear-gradient(-45deg, #120A18, #28112B, #3B142A, #1B1836, #2C1A1D);
    background-size: 400% 400%;
    animation: velvetFlow 20s ease infinite;
}

.velvet-canvas::before,
.velvet-canvas::after {
    content: "";
    position: absolute;
    border-radius: 50%;
    filter: blur(95px);
    animation: luminousDrift 16s ease-in-out infinite alternate;
}
.velvet-canvas::before {
    width: 52vw;
    height: 52vw;
    top: -12%;
    left: -8%;
    background: radial-gradient(circle, rgba(245, 158, 11, 0.26) 0%, rgba(225, 29, 72, 0.12) 45%, transparent 72%);
}
.velvet-canvas::after {
    width: 55vw;
    height: 55vw;
    bottom: -15%;
    right: -10%;
    background: radial-gradient(circle, rgba(168, 85, 247, 0.25) 0%, rgba(244, 63, 94, 0.15) 45%, transparent 72%);
    animation-delay: -8s;
}

@keyframes velvetFlow {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes luminousDrift {
    0%   { transform: translate(0px, 0px) scale(1); }
    50%  { transform: translate(70px, 45px) scale(1.15); }
    100% { transform: translate(-45px, 65px) scale(0.95); }
}

/* Floating Gold & Rose Starlight Motes */
.starlight-layer {
    position: fixed;
    inset: 0;
    z-index: -1;
    pointer-events: none;
    overflow: hidden;
}
.mote {
    position: absolute;
    bottom: -20px;
    border-radius: 50%;
    background: radial-gradient(circle, #FDE68A 0%, #F59E0B 50%, transparent 100%);
    box-shadow: 0 0 14px rgba(245, 158, 11, 0.75);
    animation: floatUp linear infinite;
}
.mote:nth-child(1)  { left: 7%;  width: 6px;  height: 6px;  animation-duration: 15s; animation-delay: 0s; }
.mote:nth-child(2)  { left: 17%; width: 10px; height: 10px; animation-duration: 22s; animation-delay: 2s; }
.mote:nth-child(3)  { left: 28%; width: 5px;  height: 5px;  animation-duration: 13s; animation-delay: 5s; }
.mote:nth-child(4)  { left: 39%; width: 11px; height: 11px; animation-duration: 25s; animation-delay: 1s; }
.mote:nth-child(5)  { left: 51%; width: 7px;  height: 7px;  animation-duration: 18s; animation-delay: 4s; }
.mote:nth-child(6)  { left: 63%; width: 9px;  height: 9px;  animation-duration: 20s; animation-delay: 6s; }
.mote:nth-child(7)  { left: 74%; width: 6px;  height: 6px;  animation-duration: 14s; animation-delay: 3s; }
.mote:nth-child(8)  { left: 85%; width: 10px; height: 10px; animation-duration: 23s; animation-delay: 7s; }
.mote:nth-child(9)  { left: 93%; width: 7px;  height: 7px;  animation-duration: 17s; animation-delay: 9s; }

@keyframes floatUp {
    0%   { transform: translateY(0) translateX(0) scale(0.7); opacity: 0; }
    20%  { opacity: 0.9; }
    80%  { opacity: 0.7; }
    100% { transform: translateY(-108vh) translateX(40px) scale(1.25); opacity: 0; }
}

/* Typography */
html, body, [class*="css"] {
    font-family: 'Lora', Georgia, serif;
    color: #F8F1E7;
}
h1, h2, h3, h4 {
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.03em;
    color: #FDE68A !important;
}

/* Opulent Hero Header */
.atelier-banner {
    text-align: center;
    padding: 2rem 1.5rem 1.6rem 1.5rem;
    margin-bottom: 1.6rem;
    background: linear-gradient(135deg, rgba(38, 22, 48, 0.75) 0%, rgba(58, 20, 42, 0.68) 100%);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border: 1px solid rgba(245, 158, 11, 0.38);
    border-radius: 18px;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.45), inset 0 0 24px rgba(245, 158, 11, 0.08);
}
.atelier-brand {
    font-family: 'Cinzel Decorative', 'Cormorant Garamond', serif;
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(90deg, #FDE68A 0%, #F59E0B 45%, #FDA4AF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.25rem;
    letter-spacing: 0.04em;
}
.atelier-flourish {
    color: #F59E0B;
    font-size: 1.25rem;
    letter-spacing: 0.35em;
    margin: 0.25rem 0 0.45rem 0;
}
.atelier-epigraph {
    font-family: 'Cormorant Garamond', serif;
    font-style: italic;
    font-size: 1.22rem;
    color: #E9D8FD;
}

/* Smoked Glass Inputs & Poetry Writing Desk */
textarea {
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    font-size: 1.32rem !important;
    line-height: 1.85 !important;
    color: #FFFBEB !important;
    background: rgba(24, 15, 31, 0.78) !important;
    backdrop-filter: blur(14px);
    border: 1px solid rgba(245, 158, 11, 0.35) !important;
    border-radius: 12px !important;
    padding: 1.15rem !important;
    box-shadow: inset 0 2px 14px rgba(0, 0, 0, 0.45);
}
textarea:focus, input[type="text"]:focus {
    border-color: #F59E0B !important;
    box-shadow: 0 0 0 2px rgba(245, 158, 11, 0.25) !important;
}
input[type="text"] {
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    font-size: 1.25rem !important;
    color: #FFFBEB !important;
    background: rgba(24, 15, 31, 0.78) !important;
    border: 1px solid rgba(245, 158, 11, 0.35) !important;
    border-radius: 10px !important;
}

/* Gold & Crimson Gradient Action Buttons */
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #D97706 0%, #BE123C 100%) !important;
    color: #FFFBEB !important;
    border: 1px solid rgba(253, 230, 138, 0.45) !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.4rem !important;
    font-family: 'Lora', serif !important;
    font-weight: 500 !important;
    letter-spacing: 0.04em;
    box-shadow: 0 6px 20px rgba(190, 18, 60, 0.35);
    transition: all 0.25s ease;
}
div.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 26px rgba(245, 158, 11, 0.45);
}

/* Secondary Glass Buttons */
div.stButton > button[kind="secondary"] {
    background: rgba(39, 24, 49, 0.75) !important;
    color: #FDE68A !important;
    border: 1px solid rgba(245, 158, 11, 0.35) !important;
    border-radius: 10px !important;
}
div.stButton > button[kind="secondary"]:hover {
    border-color: #F59E0B !important;
    background: rgba(58, 33, 71, 0.85) !important;
}

/* Jewel Metric Cards */
[data-testid="stMetric"] {
    background: linear-gradient(145deg, rgba(37, 22, 47, 0.82), rgba(53, 21, 43, 0.78));
    backdrop-filter: blur(14px);
    border: 1px solid rgba(245, 158, 11, 0.35);
    border-radius: 12px;
    padding: 0.95rem 1.1rem;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35);
}
[data-testid="stMetricLabel"] {
    color: #FDA4AF !important;
    font-size: 0.8rem !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
[data-testid="stMetricValue"] {
    font-family: 'Cormorant Garamond', serif !important;
    color: #FDE68A !important;
    font-size: 1.85rem !important;
}

/* Illuminated Manuscript Card */
.manuscript-card {
    background: linear-gradient(145deg, rgba(31, 19, 40, 0.84), rgba(45, 19, 38, 0.78));
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(245, 158, 11, 0.32);
    border-left: 4px solid #F59E0B;
    border-radius: 14px;
    padding: 1.5rem 1.9rem;
    margin-bottom: 1.1rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.38);
}
.manuscript-title {
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: #FDE68A;
    margin-bottom: 0.25rem;
}
.manuscript-meta {
    font-size: 0.88rem;
    color: #FDA4AF;
    font-style: italic;
    margin-bottom: 1rem;
    padding-bottom: 0.65rem;
    border-bottom: 1px dashed rgba(245, 158, 11, 0.3);
}
.manuscript-verse {
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 1.3rem;
    line-height: 1.85;
    white-space: pre-wrap;
    color: #FAF5FF;
}

/* Rhyme & Syllable Pill Badges */
.poetic-badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    margin: 0.2rem 0.35rem 0.2rem 0;
    border-radius: 999px;
    font-size: 0.85rem;
    background: rgba(245, 158, 11, 0.16);
    border: 1px solid rgba(245, 158, 11, 0.45);
    color: #FDE68A;
}

/* Literary Archive Quote Card */
.classic-quote {
    background: rgba(28, 18, 37, 0.82);
    border-left: 3px solid #FB7185;
    border-top: 1px solid rgba(251, 113, 133, 0.22);
    padding: 1.1rem 1.4rem;
    border-radius: 0 12px 12px 0;
    margin-bottom: 0.85rem;
    font-style: italic;
    color: #F3E8FF;
}

/* Navigation Tabs */
button[data-baseweb="tab"] {
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    font-size: 1.28rem !important;
    font-weight: 700 !important;
    color: #E9D8FD !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #FDE68A !important;
}
</style>

<div class="velvet-canvas"></div>
<div class="starlight-layer">
    <div class="mote"></div><div class="mote"></div><div class="mote"></div>
    <div class="mote"></div><div class="mote"></div><div class="mote"></div>
    <div class="mote"></div><div class="mote"></div><div class="mote"></div>
</div>
""", unsafe_allow_html=True)

# --- HERO BANNER ---
quote_text, quote_author = random.choice(MUSE_QUOTES)
st.markdown(f"""
<div class="atelier-banner">
    <div class="atelier-brand">🪶 Poet’s Atelier</div>
    <div class="atelier-flourish">✦ ❧ ✦</div>
    <div class="atelier-epigraph">{quote_text} — <b>{quote_author}</b></div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs([
    "✒️ Writing Desk & Prosody Analyzer",
    "📜 Illuminated Vault",
    "📖 Anthology Book Studio"
])

# --- TAB 1: ANALYZE & SAVE ---
with tab1:
    editing_id = st.session_state.get("edit_poem_id", None)
    default_title = st.session_state.get("edit_title", "")
    default_content = st.session_state.get("edit_content", "")

    # Top Quick-Load Bar (Sample Poems or Revision Notice)
    top_col1, top_col2 = st.columns([2, 1])
    with top_col1:
        if editing_id:
            st.info(f"🖋️ Revising Saved Manuscript #{editing_id} — Refine your verses and preserve your new draft.")
    with top_col2:
        chosen_sample = st.selectbox("✨ Try a Sample Poem:", list(SAMPLE_POEMS.keys()), label_visibility="collapsed")
        if chosen_sample != "Select a sample poem to test...":
            s_title, s_body = SAMPLE_POEMS[chosen_sample]
            if st.session_state.get("last_loaded_sample") != chosen_sample:
                st.session_state["last_loaded_sample"] = chosen_sample
                st.session_state["edit_poem_id"] = None
                st.session_state["edit_title"] = s_title
                st.session_state["edit_content"] = s_body
                st.rerun()

    if editing_id:
        if st.button("✨ Start Fresh Blank Manuscript"):
            st.session_state.pop("edit_poem_id", None)
            st.session_state.pop("edit_title", None)
            st.session_state.pop("edit_content", None)
            st.rerun()

    col_editor, col_results = st.columns([1.05, 1], gap="large")

    with col_editor:
        st.markdown("### Your Manuscript")
        poem_title = st.text_input("Title of the Piece", value=default_title, placeholder="e.g., Nocturne in Crimson & Gold")
        poem_text = st.text_area(
            "Stanzas",
            value=default_content,
            height=350,
            placeholder="Inscribe your verses here...\nLet rhythm, rhyme, and imagery shimmer across each line."
        )

        # Live line & stanza counter
        lines = [ln for ln in poem_text.splitlines() if ln.strip()]
        stanzas = [s for s in poem_text.strip().split("\n\n") if s.strip()] if poem_text.strip() else []
        st.caption(f"🕯️ {len(lines)} lines · {len(stanzas)} stanzas · {len(poem_text.split())} words")

        btn_col1, btn_col2 = st.columns([1.2, 1])
        with btn_col1:
            analyze_clicked = st.button("✨ Examine Verse & Rhyme", type="primary", use_container_width=True)
        with btn_col2:
            if "last_analysis" in st.session_state and poem_title.strip() and poem_text.strip():
                if st.button("📥 Preserve in Vault", use_container_width=True):
                    analysis = st.session_state["last_analysis"]
                    save_or_update_poem(
                        title=poem_title,
                        content=poem_text,
                        rhyme_scheme=analysis.rhyme_scheme,
                        theme=analysis.primary_theme,
                        feedback=analysis.strengths,
                        poem_id=editing_id
                    )
                    st.toast("Preserved in your Illuminated Vault!", icon="📜")
                    st.success("Saved! View or revise it anytime in the Illuminated Vault tab.")

        if analyze_clicked:
            if not poem_title.strip() or not poem_text.strip():
                st.warning("Please inscribe both a title and at least one stanza before examining.")
            else:
                with st.spinner("Tracing rhyme schemes, scanning meter, and consulting classic archives..."):
                    analysis, similar = analyze_poem(poem_title, poem_text)
                    st.session_state["last_analysis"] = analysis
                    st.session_state["last_similar"] = similar

    with col_results:
        st.markdown("### Editorial Critique")
        if "last_analysis" not in st.session_state:
            st.markdown("""
            <div class="manuscript-card" style="text-align:center; padding: 3.5rem 1.8rem;">
                <div style="font-size: 2.4rem; margin-bottom: 0.6rem;">🕯️</div>
                <div style="font-family: 'Cormorant Garamond', serif; font-size: 1.5rem; font-style: italic; color: #E9D8FD;">
                    Your writing desk is lit.<br>
                    Compose a verse—or pick a sample poem above—and click <b style="color:#FDE68A;">Examine Verse & Rhyme</b> to reveal its prosody, flaws, and classic literary echoes.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            analysis = st.session_state["last_analysis"]

            m1, m2, m3 = st.columns(3)
            m1.metric("Rhyme Scheme", analysis.rhyme_scheme)
            m2.metric("Theme", analysis.primary_theme)
            m3.metric("Craft Score", f"{analysis.overall_score}/100")

            # Poetic Devices as glowing jewel badges
            badges_html = "".join([f"<span class='poetic-badge'>✦ {dev}</span>" for dev in analysis.literary_devices_used])
            st.markdown(f"<div style='margin: 0.8rem 0;'>{badges_html}</div>", unsafe_allow_html=True)

            st.markdown(f"**Meter & Cadence:** {analysis.meter_and_rhythm}")
            st.success(f"**Editor's Praise:** {analysis.strengths}")

            st.markdown("#### Line-by-Line Refinement Notes")
            if not analysis.line_by_line_mistakes:
                st.write("No technical flaws detected—your cadence and rhyme ring true.")
            else:
                for idx, item in enumerate(analysis.line_by_line_mistakes):
                    with st.expander(f"Line {item.line_number} · {item.issue_type} — “{item.original_line}”", expanded=(idx == 0)):
                        st.write(f"**Observation:** {item.explanation}")
                        st.markdown(f"**Suggested Revision:** `{item.suggested_rewrite}`")
                        if st.button("🪄 Apply This Revision", key=f"apply_fix_{idx}_{item.line_number}"):
                            updated_poem = poem_text.replace(item.original_line.strip(), item.suggested_rewrite.strip(), 1)
                            st.session_state["edit_title"] = poem_title
                            st.session_state["edit_content"] = updated_poem
                            st.toast("Applied revision to your manuscript!", icon="🪄")
                            st.rerun()

            if st.session_state.get("last_similar"):
                st.markdown("#### Echoes from the Poetry Foundation Archive")
                for sim in st.session_state["last_similar"]:
                    st.markdown(f"""
                    <div class="classic-quote">
                        <b style="color:#FDE68A;">{sim['title']}</b> — <i style="color:#FDA4AF;">{sim['poet']}</i><br><br>
                        <span style="white-space: pre-wrap;">{sim['excerpt']}</span>
                    </div>
                    """, unsafe_allow_html=True)

# --- TAB 2: SAVED POEMS VAULT ---
with tab2:
    st.markdown("### Your Collected Manuscripts")
    saved = get_all_poems()
    if not saved:
        st.info("Your vault awaits its first poem. Examine a verse on the Writing Desk and preserve it here.")
    else:
        for p in saved:
            col_card, col_actions = st.columns([5, 1])
            with col_card:
                st.markdown(f"""
                <div class="manuscript-card">
                    <div class="manuscript-title">{p['title']}</div>
                    <div class="manuscript-meta">
                        Theme: {p['primary_theme']}  •  Rhyme: {p['rhyme_scheme']}  •  Revised: {p['updated_at']}
                    </div>
                    <div class="manuscript-verse">{p['content']}</div>
                </div>
                """, unsafe_allow_html=True)
            with col_actions:
                st.write("")
                st.write("")
                if st.button("✒️ Revise", key=f"edit_{p['id']}", use_container_width=True):
                    st.session_state["edit_poem_id"] = p["id"]
                    st.session_state["edit_title"] = p["title"]
                    st.session_state["edit_content"] = p["content"]
                    st.toast("Loaded onto the Writing Desk!", icon="✒️")
                if st.button("🗑️ Discard", key=f"del_{p['id']}", use_container_width=True):
                    delete_poem(p["id"])
                    st.rerun()

# --- TAB 3: AUTO-DRAFT POETRY BOOK ---
with tab3:
    st.markdown("### Compile Your Debut Anthology")
    saved = get_all_poems()

    col_setup, col_preview = st.columns([1, 1.4], gap="large")

    with col_setup:
        st.markdown(f"""
        <div class="manuscript-card">
            <div class="manuscript-title">Anthology Readiness</div>
            <div class="manuscript-meta">Archived Poems Available: <b style="color:#FDE68A;">{len(saved)}</b></div>
            <p style="font-size: 0.96rem; color: #F3E8FF;">
                Our literary editor will weave your saved poems into thematic chapters, compose poetic epigraphs, write a preface, and typeset a downloadable <b>.docx</b> book draft.
            </p>
        </div>
        """, unsafe_allow_html=True)

        author_name = st.text_input("Poet's Pen Name", value="Anonymous Poet")

        if len(saved) < 2:
            st.warning("Preserve at least 2 poems in your Vault to weave an anthology.")
        else:
            if st.button("📖 Weave & Typeset Book Draft", type="primary", use_container_width=True):
                with st.spinner("Curating chapters, composing preface, and binding pages..."):
                    book_plan = generate_book_plan(saved, author_name)
                    docx_file = build_book_docx(book_plan, saved, author_name)
                    st.session_state["book_plan"] = book_plan
                    st.session_state["book_docx"] = docx_file

    with col_preview:
        if "book_plan" not in st.session_state:
            st.markdown("""
            <div class="manuscript-card" style="text-align:center; padding: 3.5rem 1.8rem;">
                <div style="font-size: 2.4rem; margin-bottom: 0.6rem;">📚</div>
                <div style="font-family: 'Cormorant Garamond', serif; font-size: 1.45rem; font-style: italic; color: #E9D8FD;">
                    Enter your pen name on the left to generate your anthology’s title, preface, and chapter architecture.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            plan = st.session_state["book_plan"]
            st.markdown(f"""
            <div class="manuscript-card" style="text-align:center;">
                <div style="font-size: 0.85rem; letter-spacing: 0.16em; text-transform: uppercase; color: #FDA4AF;">First Edition Manuscript</div>
                <div style="font-family: 'Cinzel Decorative', 'Cormorant Garamond', serif; font-size: 2.2rem; font-weight: 700; color: #FDE68A; margin-top: 0.4rem;">
                    {plan.suggested_book_title}
                </div>
                <div style="font-style: italic; color: #E9D8FD; margin-bottom: 0.8rem;">{plan.subtitle}</div>
                <div style="font-size: 0.95rem; color: #FDE68A;">By <b>{author_name}</b></div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("#### Preface")
            st.write(plan.preface)
            st.markdown("<div style='text-align:center; color:#F59E0B; letter-spacing:0.3em;'>✦ ❧ ✦</div>", unsafe_allow_html=True)

            for ch in plan.chapters:
                st.markdown(f"#### Chapter {ch.chapter_number}: {ch.chapter_title}")
                st.caption(f"“{ch.chapter_epigraph}”")
                st.write("**Included Poems:** " + " · ".join(ch.poem_titles))

            st.download_button(
                label="📥 Download Typeset Book Manuscript (.docx)",
                data=st.session_state["book_docx"],
                file_name=f"{plan.suggested_book_title.replace(' ', '_')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                type="primary",
                use_container_width=True
            )