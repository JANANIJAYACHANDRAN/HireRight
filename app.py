import csv
import html
import io
import re
from pathlib import Path

import pymupdf
import streamlit as st


# ==================================================
# 1. PAGE CONFIGURATION
# ==================================================
st.set_page_config(
    page_title="HireRight | Talent Screening",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==================================================
# 2. STYLING
# ==================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

    :root {
        --bg: #F2F5F5;
        --surface: #FFFFFF;
        --ink: #10292B;
        --ink-soft: #4B6467;
        --line: #DCE5E5;
        --accent: #0F766E;
        --accent-dark: #0B5A54;
        --accent-tint: #E0F2F0;
        --ok: #15803D;
        --ok-tint: #DCFCE7;
        --warn: #B45309;
        --warn-tint: #FEF3C7;
        --bad: #B91C1C;
        --bad-tint: #FEE2E2;
        --mark: #FDE68A;
    }

    html, body, .stApp, [class*="css"] {
        font-family: 'Manrope', system-ui, -apple-system, sans-serif;
        color: var(--ink);
    }

    .stApp { background-color: var(--bg); }

    #MainMenu, footer { visibility: hidden; }

    [data-testid="stHeader"] { background: transparent; }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }

    h1, h2, h3, h4 {
        color: var(--ink);
        letter-spacing: -0.02em;
        font-weight: 700;
    }

    /* ---------- Sidebar ---------- */
    [data-testid="stSidebar"] {
        background-color: var(--surface);
        border-right: 1px solid var(--line);
    }

    [data-testid="stSidebar"] .block-container { padding-top: 1rem; }

    .brand {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 4px;
    }

    .brand-mark {
        width: 34px;
        height: 34px;
        border-radius: 10px;
        background: var(--accent);
        color: #fff;
        display: grid;
        place-items: center;
        font-size: 17px;
    }

    .brand-name {
        font-size: 19px;
        font-weight: 800;
        letter-spacing: -0.03em;
    }

    .side-title {
        font-size: 13px;
        font-weight: 700;
        color: var(--ink);
        margin: 4px 0 2px 0;
    }

    .side-hint {
        font-size: 12px;
        color: var(--ink-soft);
        margin-bottom: 6px;
    }

    /* ---------- Inputs ---------- */
    .stTextInput input, .stTextArea textarea,
    [data-baseweb="input"] input,
    [data-baseweb="textarea"] textarea {
        background: #FBFDFD !important;
        background-color: #FBFDFD !important;
        color: #10292B !important;
        -webkit-text-fill-color: #10292B !important;
        caret-color: #0F766E !important;
        border: 1px solid var(--line);
        border-radius: 10px;
        font-family: 'Manrope', sans-serif;
        font-size: 14px;
    }

    [data-baseweb="input"],
    [data-baseweb="textarea"],
    [data-baseweb="base-input"] {
        background-color: #FBFDFD !important;
        border-radius: 10px;
    }

    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {
        color: #7C9395 !important;
        -webkit-text-fill-color: #7C9395 !important;
        opacity: 1;
    }

    [data-testid="stWidgetLabel"],
    [data-testid="stWidgetLabel"] *,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] label * {
        color: #10292B !important;
        -webkit-text-fill-color: #10292B !important;
        font-weight: 600;
        opacity: 1 !important;
    }

    [data-testid="stSidebar"] .brand-name {
        color: #10292B !important;
        -webkit-text-fill-color: #10292B !important;
    }

    [data-testid="stSidebar"] .side-title {
        color: #10292B !important;
    }

    [data-testid="stSidebar"] .side-hint,
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"],
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] * {
        color: #4B6467 !important;
    }

    [data-testid="stSidebar"] div.stButton > button {
        background: #FFFFFF !important;
        border: 1px solid #0F766E !important;
        color: #0F766E !important;
    }

    [data-testid="stSidebar"] div.stButton > button * {
        color: #0F766E !important;
    }

    [data-testid="stSidebar"] div.stButton > button:hover {
        background: #E0F2F0 !important;
    }

    [data-baseweb="input"],
    [data-baseweb="textarea"] {
        border: 1px solid #DCE5E5 !important;
        border-radius: 10px !important;
    }

    [data-baseweb="input"]:focus-within,
    [data-baseweb="textarea"]:focus-within {
        border-color: #0F766E !important;
        box-shadow: 0 0 0 3px #E0F2F0 !important;
    }

    [data-baseweb="input"] input,
    [data-baseweb="textarea"] textarea {
        border: none !important;
        box-shadow: none !important;
    }

    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: var(--accent);
        box-shadow: 0 0 0 3px var(--accent-tint);
    }

    /* ---------- Buttons ---------- */
    div.stButton > button {
        border-radius: 10px;
        font-weight: 600;
        font-family: 'Manrope', sans-serif;
        border: 1px solid var(--line);
        transition: background-color 0.15s, border-color 0.15s;
    }

    div.stButton > button[kind="primary"] {
        background-color: var(--accent);
        border: none;
        color: #fff;
        min-height: 45px;
        font-size: 15px;
    }

    div.stButton > button[kind="primary"]:hover {
        background-color: var(--accent-dark);
        border: none;
    }

    div.stButton > button[kind="primary"]:focus-visible {
        outline: 3px solid var(--accent-tint);
    }

    div.stDownloadButton > button {
        border-radius: 10px;
        font-weight: 600;
        border: 1px solid var(--accent);
        color: var(--accent);
        background: var(--surface);
    }

    div.stDownloadButton > button:hover {
        background: var(--accent-tint);
        color: var(--accent-dark);
        border-color: var(--accent-dark);
    }

    /* ---------- Header ---------- */
    .page-head {
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 26px 30px;
        margin-bottom: 22px;
    }

    .page-head h1 {
        font-size: 30px;
        margin: 0 0 6px 0;
        padding: 0;
    }

    .page-head p {
        color: var(--ink-soft);
        font-size: 15px;
        margin: 0;
        max-width: 640px;
        line-height: 1.55;
    }

    .req-strip {
        margin-top: 18px;
        padding-top: 16px;
        border-top: 1px solid var(--line);
        display: flex;
        flex-wrap: wrap;
        gap: 6px 8px;
        align-items: center;
    }

    .req-label {
        font-size: 13px;
        font-weight: 600;
        color: var(--ink-soft);
        margin-right: 4px;
    }

    .req-empty {
        font-size: 13px;
        color: var(--ink-soft);
    }

    /* ---------- Chips ---------- */
    .chip {
        display: inline-block;
        padding: 4px 11px;
        border-radius: 999px;
        font-size: 12.5px;
        font-weight: 600;
        line-height: 1.4;
        margin: 2px 4px 2px 0;
        border: 1px solid transparent;
        overflow-wrap: anywhere;
    }

    .chip-must { background: var(--accent); color: #fff; }
    .chip-nice { background: var(--accent-tint); color: var(--accent-dark); }
    .chip-found { background: var(--ok-tint); color: var(--ok); border-color: #BBF7D0; }
    .chip-missing { background: var(--warn-tint); color: var(--warn); border-color: #FDE68A; }
    .chip-neutral { background: #EEF2F2; color: var(--ink-soft); }

    /* ---------- Section headings ---------- */
    .sec-title {
        font-size: 20px;
        font-weight: 700;
        margin: 4px 0 2px 0;
    }

    .sec-sub {
        font-size: 14px;
        color: var(--ink-soft);
        margin-bottom: 14px;
    }

    /* ---------- Upload ---------- */
    div[data-testid="stFileUploader"] section {
        background-color: var(--surface);
        border: 1.5px dashed #9DB8B8;
        border-radius: 14px;
        padding: 12px;
    }

    div[data-testid="stFileUploader"] section:hover {
        border-color: var(--accent);
        background-color: #FAFEFE;
    }

    [data-testid="stFileUploaderDropzone"] {
        background-color: var(--surface) !important;
    }

    [data-testid="stFileUploaderDropzone"] span,
    [data-testid="stFileUploaderDropzone"] small,
    [data-testid="stFileUploaderDropzone"] div {
        color: var(--ink-soft) !important;
    }

    div[data-testid="stFileUploader"] [data-testid="stFileUploaderDropzone"] button,
    div[data-testid="stFileUploader"] section button {
        background: #0F766E !important;
        background-color: #0F766E !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }

    div[data-testid="stFileUploader"] [data-testid="stFileUploaderDropzone"] button:hover,
    div[data-testid="stFileUploader"] section button:hover {
        background: #0B5A54 !important;
        background-color: #0B5A54 !important;
    }

    div[data-testid="stFileUploader"] [data-testid="stFileUploaderDropzone"] button *,
    div[data-testid="stFileUploader"] section button * {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
    }

    [data-testid="stFileUploaderFile"],
    [data-testid="stFileUploaderFile"] * {
        color: var(--ink) !important;
    }

    /* ---------- Stat cards ---------- */
    .stat {
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 18px;
        height: 100%;
    }

    .stat-value {
        font-size: 30px;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1.1;
    }

    .stat-label {
        font-size: 13px;
        color: var(--ink-soft);
        margin-top: 4px;
    }

    .stat-accent .stat-value { color: var(--accent); }
    .stat-warn .stat-value { color: var(--warn); }

    /* ---------- Candidate card ---------- */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: var(--surface);
        border-radius: 16px;
    }

    .cand-row {
        display: flex;
        align-items: center;
        gap: 20px;
    }

    .ring {
        --size: 88px;
        --pct: 0;
        --color: var(--accent);
        width: var(--size);
        height: var(--size);
        border-radius: 50%;
        background: conic-gradient(var(--color) calc(var(--pct) * 1%), #E4ECEC 0);
        display: grid;
        place-items: center;
        flex-shrink: 0;
    }

    .ring-inner {
        width: calc(var(--size) - 16px);
        height: calc(var(--size) - 16px);
        border-radius: 50%;
        background: var(--surface);
        display: grid;
        place-items: center;
        text-align: center;
    }

    .ring-num {
        font-size: 22px;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1;
    }

    .ring-sub {
        font-size: 10.5px;
        color: var(--ink-soft);
        margin-top: 2px;
        font-weight: 600;
    }

    .cand-main { flex: 1; min-width: 0; }

    .cand-name {
        font-size: 19px;
        font-weight: 700;
        letter-spacing: -0.02em;
        overflow-wrap: anywhere;
    }

    .cand-file {
        font-size: 12.5px;
        color: var(--ink-soft);
        margin-bottom: 8px;
        overflow-wrap: anywhere;
    }

    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 8px;
        font-size: 12.5px;
        font-weight: 700;
    }

    .badge-ok { background: var(--ok-tint); color: var(--ok); }
    .badge-warn { background: var(--warn-tint); color: var(--warn); }
    .badge-bad { background: var(--bad-tint); color: var(--bad); }

    .mini-title {
        font-size: 13px;
        font-weight: 700;
        margin-bottom: 6px;
    }

    .empty-note {
        font-size: 13px;
        color: var(--ink-soft);
    }

    /* ---------- Evidence ---------- */
    .evidence {
        border-left: 3px solid var(--accent);
        background: #F7FAFA;
        padding: 9px 13px;
        border-radius: 0 8px 8px 0;
        margin: 6px 0;
        font-size: 13.5px;
        line-height: 1.55;
        overflow-wrap: anywhere;
    }

    .evidence mark {
        background: var(--mark);
        color: var(--ink);
        padding: 0 3px;
        border-radius: 3px;
        font-weight: 600;
    }

    .disclaimer {
        font-size: 12px;
        color: var(--ink-soft);
        margin-top: 10px;
        line-height: 1.5;
    }

    /* ---------- Tabs & expanders ---------- */
    button[data-baseweb="tab"] {
        font-family: 'Manrope', sans-serif;
        font-weight: 600;
    }

    div[data-baseweb="tab-highlight"] { background-color: var(--accent); }

    details {
        border-radius: 10px !important;
        border-color: var(--line) !important;
    }

    /* ---------- Comparison table ---------- */
    .cmp {
        width: 100%;
        border-collapse: collapse;
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 14px;
        overflow: hidden;
        font-size: 14px;
    }

    .cmp th {
        background: #F7FAFA;
        text-align: left;
        padding: 11px 16px;
        font-weight: 700;
        border-bottom: 1px solid var(--line);
        overflow-wrap: anywhere;
    }

    .cmp td {
        padding: 10px 16px;
        border-bottom: 1px solid #EDF2F2;
    }

    .cmp tr:last-child td { border-bottom: none; }

    .cmp-wrap { overflow-x: auto; }

    .yes { color: var(--ok); font-weight: 700; }
    .no { color: var(--warn); font-weight: 700; }

    .cmp-group td {
        background: #F7FAFA;
        font-size: 12.5px;
        font-weight: 700;
        color: var(--ink-soft);
    }

    /* ---------- Empty state ---------- */
    .empty-state {
        background: var(--surface);
        border: 1.5px dashed #B5CACA;
        border-radius: 16px;
        padding: 34px 28px;
        text-align: center;
        color: var(--ink-soft);
    }

    .empty-state b { color: var(--ink); font-size: 16px; }

    .foot {
        text-align: center;
        font-size: 12.5px;
        color: var(--ink-soft);
        margin-top: 10px;
    }

    hr { border-color: var(--line); }

    @media (max-width: 700px) {
        .cand-row { flex-direction: column; align-items: flex-start; }
        .page-head { padding: 20px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# 3. HELPER FUNCTIONS (screening logic)
# ==================================================
def extract_resume_text(uploaded_file):
    """Extract readable text from a PDF resume."""
    try:
        pdf_bytes = uploaded_file.getvalue()

        with pymupdf.open(
            stream=pdf_bytes,
            filetype="pdf",
        ) as document:
            pages = [page.get_text() for page in document]

        return "\n".join(pages).strip()

    except Exception:
        return ""


def parse_skills(skill_input):
    """Parse comma-separated skills and remove duplicates."""
    skills = [
        item.strip()
        for item in skill_input.split(",")
        if item.strip()
    ]

    unique_skills = []
    seen = set()

    for skill in skills:
        key = skill.casefold()

        if key not in seen:
            unique_skills.append(skill)
            seen.add(key)

    return unique_skills


def split_into_sentences(text):
    """Split resume text into sentences or lines."""
    parts = re.split(r"(?<=[.!?])\s+|\n+", text)

    return [
        part.strip()
        for part in parts
        if part.strip()
    ]


def build_skill_pattern(skill):
    """Build a whole-word regex for a skill keyword."""
    if re.search(r"\w", skill):
        return r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

    return re.escape(skill)


def find_skill_evidence(text, skills):
    """Find matching keywords and retain their context."""
    sentences = split_into_sentences(text)
    results = {}

    for skill in skills:
        pattern = build_skill_pattern(skill)
        evidence = []

        for sentence in sentences:
            if re.search(pattern, sentence, re.IGNORECASE):
                if sentence not in evidence:
                    evidence.append(sentence)

        results[skill] = evidence

    return results


def evaluate_resume(resume_text, mandatory, preferred):
    """Evaluate required and preferred skill keywords."""
    mandatory_evidence = find_skill_evidence(
        resume_text, mandatory
    )

    preferred_evidence = find_skill_evidence(
        resume_text, preferred
    )

    mandatory_found = [
        skill
        for skill, evidence in mandatory_evidence.items()
        if evidence
    ]

    mandatory_missing = [
        skill
        for skill, evidence in mandatory_evidence.items()
        if not evidence
    ]

    preferred_found = [
        skill
        for skill, evidence in preferred_evidence.items()
        if evidence
    ]

    preferred_missing = [
        skill
        for skill, evidence in preferred_evidence.items()
        if not evidence
    ]

    if not resume_text.strip():
        status = "Unable to evaluate"
    elif mandatory_missing:
        status = "Needs human review"
    else:
        status = "Mandatory keywords detected"

    return {
        "status": status,
        "mandatory_found": mandatory_found,
        "mandatory_missing": mandatory_missing,
        "preferred_found": preferred_found,
        "preferred_missing": preferred_missing,
        "mandatory_evidence": mandatory_evidence,
        "preferred_evidence": preferred_evidence,
    }


# ==================================================
# 4. HELPER FUNCTIONS (presentation)
# ==================================================
def esc(value):
    """HTML-escape any text before placing it in markup."""
    return html.escape(str(value), quote=True)


def chips_html(skills, kind):
    """Render skills as pill-shaped chips."""
    return "".join(
        f'<span class="chip chip-{kind}">{esc(skill)}</span>'
        for skill in skills
    )


def highlight_html(sentence, skill):
    """Escape a sentence and highlight the matched keyword."""
    pattern = build_skill_pattern(skill)
    pieces = re.split(f"({pattern})", sentence, flags=re.IGNORECASE)

    output = []

    for piece in pieces:
        if not piece:
            continue

        if re.fullmatch(pattern, piece, flags=re.IGNORECASE):
            output.append(f"<mark>{esc(piece)}</mark>")
        else:
            output.append(esc(piece))

    return "".join(output)


def candidate_label(filename):
    """Turn a file name into a readable candidate label."""
    stem = Path(filename).stem
    cleaned = re.sub(r"[_\-]+", " ", stem).strip()
    return cleaned or filename


def coverage_percent(found, total):
    """Mandatory keyword coverage as a whole number."""
    return round(found / total * 100) if total else 0


def ring_html(percent, found, total, ok):
    """Circular coverage indicator."""
    color = "var(--ok)" if ok else "var(--warn)"

    return (
        f'<div class="ring" style="--pct:{percent}; --color:{color};">'
        f'<div class="ring-inner"><div>'
        f'<div class="ring-num">{percent}%</div>'
        f'<div class="ring-sub">{found}/{total} must-have</div>'
        f"</div></div></div>"
    )


def stat_card(value, label, tone=""):
    """Small summary card."""
    return (
        f'<div class="stat {tone}">'
        f'<div class="stat-value">{value}</div>'
        f'<div class="stat-label">{esc(label)}</div>'
        f"</div>"
    )


def comparison_html(valid, mandatory, preferred):
    """Side-by-side keyword table for two candidates."""
    header = "".join(
        f"<th>{esc(candidate_label(item['filename']))}</th>"
        for item in valid
    )

    rows = [f"<tr><th>Skill</th>{header}</tr>"]

    def group(title, skills, found_key):
        if not skills:
            return

        rows.append(
            f'<tr class="cmp-group"><td colspan="{len(valid) + 1}">'
            f"{title}</td></tr>"
        )

        for skill in skills:
            cells = ""

            for item in valid:
                if skill in item["result"][found_key]:
                    cells += '<td><span class="yes">✓ Detected</span></td>'
                else:
                    cells += '<td><span class="no">– Not detected</span></td>'

            rows.append(f"<tr><td>{esc(skill)}</td>{cells}</tr>")

    group("Mandatory skills", mandatory, "mandatory_found")
    group("Preferred skills", preferred, "preferred_found")

    return (
        '<div class="cmp-wrap"><table class="cmp">'
        + "".join(rows)
        + "</table></div>"
    )


def build_csv(candidate_results, role):
    """Create a CSV summary of the screening run."""
    buffer = io.StringIO()
    writer = csv.writer(buffer)

    writer.writerow([
        "Role",
        "File",
        "Status",
        "Mandatory coverage %",
        "Mandatory detected",
        "Mandatory not detected",
        "Preferred detected",
        "Preferred not detected",
    ])

    for item in candidate_results:
        if "result" not in item:
            writer.writerow([role, item["filename"], "Not evaluated"])
            continue

        result = item["result"]
        found = len(result["mandatory_found"])
        total = found + len(result["mandatory_missing"])

        writer.writerow([
            role,
            item["filename"],
            result["status"],
            coverage_percent(found, total),
            "; ".join(result["mandatory_found"]),
            "; ".join(result["mandatory_missing"]),
            "; ".join(result["preferred_found"]),
            "; ".join(result["preferred_missing"]),
        ])

    return buffer.getvalue()


def render_evidence(evidence_map, empty_message):
    """Render expandable evidence blocks with highlighted keywords."""
    if not evidence_map:
        st.markdown(
            f'<div class="empty-note">{esc(empty_message)}</div>',
            unsafe_allow_html=True,
        )
        return

    for skill, evidence in evidence_map.items():
        count = len(evidence)
        icon = "✅" if count else "⚠️"
        suffix = f"{count} mention{'s' if count != 1 else ''}"

        with st.expander(f"{icon}  {skill}  ·  {suffix}"):
            if not evidence:
                st.info("No matching text detected for this skill.")
                continue

            for sentence in evidence[:8]:
                st.markdown(
                    f'<div class="evidence">'
                    f"{highlight_html(sentence, skill)}</div>",
                    unsafe_allow_html=True,
                )

            if count > 8:
                st.caption(f"Showing 8 of {count} mentions.")


def skill_columns(found, missing):
    """Two-column found / not found chip display."""
    found_col, missing_col = st.columns(2)

    with found_col:
        st.markdown(
            '<div class="mini-title">Detected</div>',
            unsafe_allow_html=True,
        )

        if found:
            st.markdown(chips_html(found, "found"), unsafe_allow_html=True)
        else:
            st.markdown(
                '<div class="empty-note">None detected.</div>',
                unsafe_allow_html=True,
            )

    with missing_col:
        st.markdown(
            '<div class="mini-title">Not detected</div>',
            unsafe_allow_html=True,
        )

        if missing:
            st.markdown(
                chips_html(missing, "missing"),
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="empty-note">Nothing missing.</div>',
                unsafe_allow_html=True,
            )


def load_example():
    """Fill the sidebar with an example job (button callback)."""
    st.session_state["job_role"] = "Junior Data Engineer"
    st.session_state["job_description"] = (
        "Build and maintain data pipelines, write SQL transformations, "
        "and support cloud-based ETL workflows."
    )
    st.session_state["mandatory_input"] = "Python, SQL, ETL"
    st.session_state["preferred_input"] = "PySpark, Azure Data Factory"


# ==================================================
# 5. SIDEBAR — JOB CONFIGURATION
# ==================================================
with st.sidebar:
    st.markdown(
        '<div class="brand"><div class="brand-mark">📋</div>'
        '<div class="brand-name">HireRight</div></div>'
        '<div class="side-hint">Talent screening workspace</div>',
        unsafe_allow_html=True,
    )

    st.button(
        "Fill with an example job",
        on_click=load_example,
        use_container_width=True,
    )

    st.divider()

    st.markdown(
        '<div class="side-title">Role</div>'
        '<div class="side-hint">What are you hiring for?</div>',
        unsafe_allow_html=True,
    )

    job_role = st.text_input(
        "Job title",
        placeholder="Junior Data Engineer",
        key="job_role",
    )

    job_description = st.text_area(
        "Job description",
        placeholder="Paste the job description...",
        height=150,
        key="job_description",
    )

    st.divider()

    st.markdown(
        '<div class="side-title">Skills to look for</div>'
        '<div class="side-hint">Separate each skill with a comma.</div>',
        unsafe_allow_html=True,
    )

    mandatory_input = st.text_area(
        "Mandatory skills",
        placeholder="Python, SQL, ETL",
        key="mandatory_input",
    )

    preferred_input = st.text_area(
        "Preferred skills",
        placeholder="PySpark, Azure Data Factory",
        key="preferred_input",
    )

    mandatory_skills = parse_skills(mandatory_input)
    preferred_skills = parse_skills(preferred_input)

    mandatory_names = {
        skill.casefold()
        for skill in mandatory_skills
    }

    preferred_skills = [
        skill
        for skill in preferred_skills
        if skill.casefold() not in mandatory_names
    ]

    st.divider()

    st.caption(
        "Runs locally. Reads text-based PDFs and checks keywords. "
        "No paid AI API required."
    )


# ==================================================
# 6. PAGE HEADER WITH LIVE REQUIREMENTS
# ==================================================
if mandatory_skills or preferred_skills:
    requirement_html = (
        '<span class="req-label">Looking for</span>'
        + chips_html(mandatory_skills, "must")
        + chips_html(preferred_skills, "nice")
    )
else:
    requirement_html = (
        '<span class="req-empty">Add skills in the sidebar and they '
        "will appear here.</span>"
    )

role_title = esc(job_role.strip()) if job_role.strip() else "Resume screening"

st.markdown(
    f'<div class="page-head">'
    f"<h1>{role_title}</h1>"
    f"<p>Compare resumes against your requirements and see the exact "
    f"lines of each resume behind every skill match.</p>"
    f'<div class="req-strip">{requirement_html}</div>'
    f"</div>",
    unsafe_allow_html=True,
)


# ==================================================
# 7. RESUME UPLOAD
# ==================================================
st.markdown(
    '<div class="sec-title">Upload resumes</div>'
    '<div class="sec-sub">Add up to two PDF resumes. '
    "Use text-based PDFs, not scans.</div>",
    unsafe_allow_html=True,
)

uploaded_files = st.file_uploader(
    "Choose PDF resume files",
    type=["pdf"],
    accept_multiple_files=True,
    label_visibility="collapsed",
)

if len(uploaded_files) > 2:
    st.warning("You can screen up to two resumes at a time. Remove the extras.")

st.markdown("")

run_screening = st.button(
    "Evaluate candidates",
    type="primary",
    use_container_width=True,
)

if run_screening:
    if not job_role.strip():
        st.error("Enter the job title in the sidebar.")

    elif not job_description.strip():
        st.error("Enter the job description in the sidebar.")

    elif not mandatory_skills:
        st.error("Enter at least one mandatory skill in the sidebar.")

    elif not uploaded_files:
        st.error("Upload at least one PDF resume.")

    elif len(uploaded_files) > 2:
        st.error("Remove resumes until two or fewer remain.")

    else:
        candidate_results = []

        with st.spinner("Reading resumes and checking skills..."):
            for uploaded_file in uploaded_files:
                resume_text = extract_resume_text(uploaded_file)

                if not resume_text:
                    candidate_results.append({
                        "filename": uploaded_file.name,
                        "error": (
                            "No readable text could be extracted. "
                            "The PDF may be scanned or image-based. "
                            "Upload a text-based PDF instead."
                        ),
                    })
                    continue

                result = evaluate_resume(
                    resume_text,
                    mandatory_skills,
                    preferred_skills,
                )

                candidate_results.append({
                    "filename": uploaded_file.name,
                    "result": result,
                })

        st.session_state["hireright_results"] = candidate_results
        st.session_state["hireright_role"] = job_role
        st.session_state["hireright_mandatory"] = list(mandatory_skills)
        st.session_state["hireright_preferred"] = list(preferred_skills)


# ==================================================
# 8. RESULTS
# ==================================================
if "hireright_results" not in st.session_state:
    st.markdown(
        '<div class="empty-state"><b>No results yet</b><br>'
        "Fill in the job details, upload a resume, and select "
        "Evaluate candidates.</div>",
        unsafe_allow_html=True,
    )

else:
    candidate_results = st.session_state["hireright_results"]
    ran_role = st.session_state.get("hireright_role", "")
    ran_mandatory = st.session_state.get("hireright_mandatory", [])
    ran_preferred = st.session_state.get("hireright_preferred", [])

    valid_results = [
        item for item in candidate_results
        if "result" in item
    ]

    total_candidates = len(candidate_results)

    all_mandatory_found = sum(
        len(item["result"]["mandatory_found"])
        for item in valid_results
    )

    all_mandatory_missing = sum(
        len(item["result"]["mandatory_missing"])
        for item in valid_results
    )

    st.divider()

    head_col, export_col = st.columns([3, 1])

    with head_col:
        st.markdown(
            f'<div class="sec-title">Results for {esc(ran_role)}</div>'
            '<div class="sec-sub">Keyword coverage shows how many '
            "mandatory skills appear in each resume.</div>",
            unsafe_allow_html=True,
        )

    with export_col:
        st.download_button(
            "Download summary (CSV)",
            data=build_csv(candidate_results, ran_role),
            file_name="hireright_screening.csv",
            mime="text/csv",
            use_container_width=True,
        )

    # ---------- Summary cards ----------
    s1, s2, s3, s4 = st.columns(4)

    with s1:
        st.markdown(
            stat_card(total_candidates, "Resumes uploaded"),
            unsafe_allow_html=True,
        )

    with s2:
        st.markdown(
            stat_card(len(valid_results), "Resumes evaluated"),
            unsafe_allow_html=True,
        )

    with s3:
        st.markdown(
            stat_card(
                all_mandatory_found,
                "Mandatory skills detected",
                "stat-accent",
            ),
            unsafe_allow_html=True,
        )

    with s4:
        st.markdown(
            stat_card(
                all_mandatory_missing,
                "Mandatory skills to review",
                "stat-warn",
            ),
            unsafe_allow_html=True,
        )

    st.caption(
        "Skill totals count each candidate-skill pair separately. "
        "They are not counts of unique candidates."
    )

    # ---------- Side-by-side comparison ----------
    if len(valid_results) == 2:
        st.markdown(
            '<div class="sec-title">Side by side</div>'
            '<div class="sec-sub">Which skills each candidate\'s '
            "resume mentions.</div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            comparison_html(valid_results, ran_mandatory, ran_preferred),
            unsafe_allow_html=True,
        )

        st.markdown("")

    # ---------- Candidate cards ----------
    st.markdown(
        '<div class="sec-title">Candidate details</div>'
        '<div class="sec-sub">Open the Evidence tab to read the lines '
        "behind each match.</div>",
        unsafe_allow_html=True,
    )

    for index, candidate in enumerate(candidate_results, start=1):
        label = candidate_label(candidate["filename"])

        with st.container(border=True):
            if "error" in candidate:
                st.markdown(
                    f'<div class="cand-name">{esc(label)}</div>'
                    f'<div class="cand-file">{esc(candidate["filename"])}'
                    f"</div>"
                    f'<span class="badge badge-bad">Not evaluated</span>',
                    unsafe_allow_html=True,
                )

                st.error(candidate["error"])
                continue

            result = candidate["result"]

            found_count = len(result["mandatory_found"])
            missing_count = len(result["mandatory_missing"])
            total_required = found_count + missing_count
            match_percentage = coverage_percent(found_count, total_required)

            all_found = result["status"] == "Mandatory keywords detected"

            badge = (
                '<span class="badge badge-ok">All mandatory keywords detected</span>'
                if all_found
                else '<span class="badge badge-warn">Needs human review</span>'
            )

            st.markdown(
                '<div class="cand-row">'
                + ring_html(
                    match_percentage,
                    found_count,
                    total_required,
                    all_found,
                )
                + '<div class="cand-main">'
                + f'<div class="cand-name">{esc(label)}</div>'
                + f'<div class="cand-file">{esc(candidate["filename"])}</div>'
                + badge
                + "</div></div>",
                unsafe_allow_html=True,
            )

            st.markdown("")

            tab1, tab2, tab3 = st.tabs([
                "Mandatory skills",
                "Preferred skills",
                "Evidence",
            ])

            with tab1:
                skill_columns(
                    result["mandatory_found"],
                    result["mandatory_missing"],
                )

            with tab2:
                if ran_preferred:
                    skill_columns(
                        result["preferred_found"],
                        result["preferred_missing"],
                    )
                else:
                    st.markdown(
                        '<div class="empty-note">No preferred skills '
                        "were specified.</div>",
                        unsafe_allow_html=True,
                    )

            with tab3:
                st.markdown(
                    '<div class="mini-title">Mandatory skills</div>',
                    unsafe_allow_html=True,
                )

                render_evidence(
                    result["mandatory_evidence"],
                    "No mandatory skills were specified.",
                )

                st.markdown(
                    '<div class="mini-title" style="margin-top:14px;">'
                    "Preferred skills</div>",
                    unsafe_allow_html=True,
                )

                render_evidence(
                    result["preferred_evidence"],
                    "No preferred skills were specified.",
                )

            st.markdown(
                '<div class="disclaimer">Keyword-based screening only. '
                "The percentage measures keyword coverage, not candidate "
                "quality or proficiency. A missing keyword does not prove "
                "a candidate lacks the skill. Human review is required."
                "</div>",
                unsafe_allow_html=True,
            )


# ==================================================
# 9. FOOTER
# ==================================================
st.markdown(
    '<div class="foot">HireRight · Portfolio prototype · '
    "Transparent, evidence-based preliminary screening</div>",
    unsafe_allow_html=True,
)