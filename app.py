import streamlit as st
from groq import Groq
import feedparser
from bs4 import BeautifulSoup
import re
from datetime import datetime

# --- إعدادات الصفحة ---
st.set_page_config(page_title="HopperChip Authority Engine", page_icon="🚀", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Syne:wght@400;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Syne', sans-serif;
        background-color: #080b12;
        color: #e2e8f0;
    }
    .main { background-color: #080b12; }

    /* Header */
    .hc-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 32px 40px;
        margin-bottom: 28px;
        position: relative;
        overflow: hidden;
    }
    .hc-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle at 30% 50%, rgba(99,102,241,0.08) 0%, transparent 60%);
        pointer-events: none;
    }
    .hc-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #818cf8, #c084fc, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .hc-subtitle {
        color: #94a3b8;
        font-size: 0.95rem;
        margin-top: 6px;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.05em;
    }
    .hc-badge {
        display: inline-block;
        background: rgba(99,102,241,0.15);
        border: 1px solid rgba(99,102,241,0.3);
        color: #818cf8;
        font-size: 0.7rem;
        padding: 3px 10px;
        border-radius: 20px;
        font-family: 'JetBrains Mono', monospace;
        margin-top: 12px;
    }

    /* Metric Cards */
    .metric-row {
        display: flex;
        gap: 12px;
        margin-bottom: 20px;
        flex-wrap: wrap;
    }
    .metric-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 16px 20px;
        flex: 1;
        min-width: 140px;
    }
    .metric-label {
        font-size: 0.72rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-family: 'JetBrains Mono', monospace;
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: 800;
        color: #c084fc;
        margin-top: 4px;
    }
    .metric-value.green { color: #34d399; }
    .metric-value.blue  { color: #60a5fa; }
    .metric-value.orange { color: #fb923c; }

    /* Article card */
    .article-header {
        background: linear-gradient(135deg, #0f172a, #1e1b4b);
        border: 1px solid #312e81;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 16px;
    }
    .article-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #e0e7ff;
        margin: 0 0 8px 0;
    }
    .article-meta {
        font-size: 0.75rem;
        color: #64748b;
        font-family: 'JetBrains Mono', monospace;
    }

    /* SEO Score Bar */
    .seo-bar-bg {
        background: #1e293b;
        border-radius: 999px;
        height: 8px;
        overflow: hidden;
        margin-top: 6px;
    }
    .seo-bar-fill {
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(90deg, #818cf8, #c084fc);
    }
    .seo-row {
        margin-bottom: 14px;
    }
    .seo-label-row {
        display: flex;
        justify-content: space-between;
        font-size: 0.78rem;
        color: #94a3b8;
        font-family: 'JetBrains Mono', monospace;
        margin-bottom: 4px;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0a0e1a !important;
        border-right: 1px solid #1e293b;
    }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stTextInput label,
    [data-testid="stSidebar"] .stSlider label {
        color: #94a3b8 !important;
        font-size: 0.8rem;
        font-family: 'JetBrains Mono', monospace;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
        color: white !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 10px !important;
        height: 3em !important;
        font-family: 'Syne', sans-serif !important;
        letter-spacing: 0.04em;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 24px rgba(79,70,229,0.35) !important;
    }

    /* History item */
    .history-item {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-left: 3px solid #6366f1;
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 8px;
        font-size: 0.82rem;
        color: #94a3b8;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Copy button */
    .copy-btn {
        display: inline-block;
        background: rgba(99,102,241,0.12);
        border: 1px solid rgba(99,102,241,0.3);
        color: #818cf8;
        padding: 6px 16px;
        border-radius: 6px;
        font-size: 0.8rem;
        cursor: pointer;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab"] {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        color: #64748b;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #818cf8 !important;
        border-bottom-color: #818cf8 !important;
    }

    .stTextInput>div>div>input {
        background-color: #0f172a !important;
        color: white !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }

    div[data-testid="stSelectbox"] > div {
        background-color: #0f172a !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }

    .footer {
        text-align: center;
        padding: 20px;
        color: #334155;
        font-size: 0.72rem;
        font-family: 'JetBrains Mono', monospace;
        border-top: 1px solid #1e293b;
        margin-top: 40px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Session State ---
if "history" not in st.session_state:
    st.session_state.history = []
if "generated_count" not in st.session_state:
    st.session_state.generated_count = 0

# --- Header ---
st.markdown("""
<div class="hc-header">
    <p class="hc-title">🔥 HopperChip Authority Engine</p>
    <p class="hc-subtitle">AI-Powered Blogger Content System · hopperchip.com</p>
    <span class="hc-badge">v4.0 · GROQ POWERED · 2026</span>
</div>
""", unsafe_allow_html=True)

# --- Session Metrics ---
total_words = sum([h["words"] for h in st.session_state.history]) if st.session_state.history else 0
st.markdown(f"""
<div class="metric-row">
    <div class="metric-card">
        <div class="metric-label">Articles Generated</div>
        <div class="metric-value">{st.session_state.generated_count}</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Total Words</div>
        <div class="metric-value blue">{total_words:,}</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Session Start</div>
        <div class="metric-value orange" style="font-size:1rem;">{datetime.now().strftime("%H:%M")}</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Avg Read Time</div>
        <div class="metric-value green">{max(1, total_words // 200)} min</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    api_key = st.text_input("Groq API Key:", type="password")

    model_choice = st.selectbox("Engine:", [
        "llama-3.3-70b-versatile",
        "llama-3.1-70b-versatile",
        "llama-3.1-8b-instant"
    ])

    language = st.selectbox("Article Language:", ["English", "Arabic"])

    st.markdown("---")
    st.markdown("### 📡 Live Sources")

    RSS_SOURCES = {
        "Hardware News": "https://techcrunch.com/category/hardware/feed/",
        "Chip Tech": "https://www.theverge.com/rss/index.xml",
        "Ars Technica": "https://feeds.arstechnica.com/arstechnica/index",
        "Wired Gear": "https://www.wired.com/feed/category/gear/latest/rss"
    }

    source_choice = st.selectbox("News Source:", list(RSS_SOURCES.keys()))
    num_posts = st.slider("Number of articles:", 1, 3, 1)

    st.markdown("---")

    # History
    if st.session_state.history:
        st.markdown("### 🕓 Session History")
        for h in reversed(st.session_state.history[-5:]):
            st.markdown(f"""
            <div class="history-item">
                📄 {h['title'][:35]}...<br>
                <span style="color:#475569">{h['time']} · {h['words']} words</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div style="color:#334155; font-size:0.7rem; font-family:\'JetBrains Mono\',monospace; text-align:center;">HopperChip Pro Suite v4.0<br>Powered by Groq 2026</div>', unsafe_allow_html=True)


# --- SEO Analyzer ---
def analyze_seo(html_text, topic_title):
    words = len(re.sub(r'<[^>]+>', '', html_text).split())
    h2_count = len(re.findall(r'<h2', html_text, re.IGNORECASE))
    h3_count = len(re.findall(r'<h3', html_text, re.IGNORECASE))
    table_count = len(re.findall(r'<table', html_text, re.IGNORECASE))
    has_pros_cons = 1 if re.search(r'pros|cons', html_text, re.IGNORECASE) else 0
    read_time = max(1, words // 200)

    # Simple keyword density (first keyword in title)
    plain_text = re.sub(r'<[^>]+>', '', html_text).lower()
    kw = topic_title.split()[0].lower() if topic_title else "chip"
    kw_count = plain_text.count(kw)
    kw_density = round((kw_count / max(words, 1)) * 100, 1)

    # Score
    score = 0
    if words >= 1000: score += 30
    elif words >= 700: score += 20
    if h2_count >= 4: score += 20
    elif h2_count >= 2: score += 10
    if table_count >= 1: score += 15
    if has_pros_cons: score += 15
    if 0.5 <= kw_density <= 3.0: score += 20

    return {
        "words": words,
        "read_time": read_time,
        "h2": h2_count,
        "h3": h3_count,
        "tables": table_count,
        "kw_density": kw_density,
        "score": min(score, 100)
    }


def generate_meta(client, model, title, lang):
    prompt = f"""Write a compelling SEO meta description (max 155 characters) for a blog post titled: "{title}".
Language: {lang}. Output ONLY the meta description text, nothing else."""
    try:
        r = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=model,
            temperature=0.5,
            max_tokens=80
        )
        return r.choices[0].message.content.strip()
    except:
        return "—"


def generate_slug(title):
    slug = re.sub(r'[^a-z0-9\s-]', '', title.lower())
    slug = re.sub(r'\s+', '-', slug.strip())
    return slug[:60]


# --- Main Engine ---
if api_key:
    client = Groq(api_key=api_key)

    if st.button("🚀 Generate High-Authority Blogger Posts"):
        entries_to_process = []

        with st.spinner("📡 Fetching RSS feed..."):
            feed = feedparser.parse(RSS_SOURCES[source_choice])
            if not feed.entries:
                st.error("Could not fetch news. Try another source.")
                st.stop()
            for entry in feed.entries[:num_posts]:
                content_raw = entry.get("summary", entry.get("description", ""))
                clean_text = BeautifulSoup(content_raw, "html.parser").get_text()
                entries_to_process.append({"title": entry.title, "clean_text": clean_text})

        for item in entries_to_process:
            title = item["title"]
            clean_text = item["clean_text"]

            with st.spinner(f'⚙️ Building article: {title[:50]}...'):

                # ---- SAME AI LOGIC — UNCHANGED ----
                master_prompt = f"""
Write a 1200-word, high-authority technical blog post for 'HopperChip.com' about: {title}.
Target Language: {language}.
Format: PURE HTML ONLY.

STRUCTURE (Blogger Optimized):
1. [H1 Title]: Catchy, SEO-rich title.
2. [Introduction]: 3 detailed paragraphs about the industry impact and historical context.
3. [Technical Deep-Dive (H2)]: Deep analysis of specs, architecture, and engineering details.
4. [Market & Competitors (H2)]: Comparison with rivals (Intel, AMD, Nvidia, Apple).
5. [Technical Specifications Table]: Clean HTML table (<table>).
6. [Pros & Cons (H2)]: Detailed bullet points.
7. [Future Outlook (H2)]: What happens next in the market?
8. [Technical Verdict (H2)]: Final score and recommendation.

STRICT RULES:
- Use ONLY HTML tags (<h2>, <h3>, <p>, <ul>, <li>, <strong>, <table>).
- NO conversational text (Don't say "Here is your post").
- Tone: Analytical, professional, and critical.
- Ensure maximum length by expanding every technical claim.

Original Info: {clean_text}
"""
                try:
                    completion = client.chat.completions.create(
                        messages=[{"role": "user", "content": master_prompt}],
                        model=model_choice,
                        temperature=0.6
                    )
                    html_output = completion.choices[0].message.content

                    # Post-processing
                    seo = analyze_seo(html_output, title)
                    meta_desc = generate_meta(client, model_choice, title, language)
                    slug = generate_slug(title)

                    # Save to history
                    st.session_state.generated_count += 1
                    st.session_state.history.append({
                        "title": title,
                        "time": datetime.now().strftime("%H:%M"),
                        "words": seo["words"]
                    })

                    # --- Article Header ---
                    st.markdown(f"""
                    <div class="article-header">
                        <p class="article-title">✅ {title}</p>
                        <p class="article-meta">
                            🕐 {seo['read_time']} min read &nbsp;·&nbsp;
                            📝 ~{seo['words']:,} words &nbsp;·&nbsp;
                            🔗 /hopperchip.com/{slug}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                    # --- Tabs ---
                    tab_view, tab_code, tab_seo, tab_meta = st.tabs([
                        "👁️ Preview", "📄 HTML Code", "📊 SEO Analysis", "🏷️ Meta & Slug"
                    ])

                    with tab_view:
                        st.markdown(
                            f"<div style='background:white; color:#1e293b; padding:36px; border-radius:12px; line-height:1.8; font-family:Georgia,serif;'>{html_output}</div>",
                            unsafe_allow_html=True
                        )

                    with tab_code:
                        st.info("📋 Copy this code → Blogger HTML View")
                        st.code(html_output, language="html")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.download_button(
                                "⬇️ Download HTML",
                                html_output,
                                file_name=f"hopperchip_{slug[:20]}.html",
                                mime="text/html"
                            )
                        with col2:
                            st.download_button(
                                "⬇️ Download TXT",
                                re.sub(r'<[^>]+>', '', html_output),
                                file_name=f"hopperchip_{slug[:20]}.txt",
                                mime="text/plain"
                            )

                    with tab_seo:
                        score = seo["score"]
                        score_color = "#34d399" if score >= 75 else "#fb923c" if score >= 50 else "#f87171"

                        st.markdown(f"""
                        <div style="text-align:center; padding: 20px 0;">
                            <div style="font-size: 3.5rem; font-weight: 800; color: {score_color}; font-family:'Syne',sans-serif;">{score}</div>
                            <div style="color: #64748b; font-family:'JetBrains Mono',monospace; font-size:0.8rem;">SEO SCORE / 100</div>
                        </div>
                        """, unsafe_allow_html=True)

                        metrics_html = f"""
                        <div class="seo-row">
                            <div class="seo-label-row"><span>Word Count</span><span>{seo['words']:,} words</span></div>
                            <div class="seo-bar-bg"><div class="seo-bar-fill" style="width:{min(seo['words']//15, 100)}%"></div></div>
                        </div>
                        <div class="seo-row">
                            <div class="seo-label-row"><span>H2 Headings</span><span>{seo['h2']} headings</span></div>
                            <div class="seo-bar-bg"><div class="seo-bar-fill" style="width:{min(seo['h2']*15, 100)}%"></div></div>
                        </div>
                        <div class="seo-row">
                            <div class="seo-label-row"><span>Keyword Density</span><span>{seo['kw_density']}%</span></div>
                            <div class="seo-bar-bg"><div class="seo-bar-fill" style="width:{min(int(seo['kw_density']*25), 100)}%"></div></div>
                        </div>
                        <div class="seo-row">
                            <div class="seo-label-row"><span>Data Tables</span><span>{seo['tables']} table(s)</span></div>
                            <div class="seo-bar-bg"><div class="seo-bar-fill" style="width:{min(seo['tables']*50, 100)}%"></div></div>
                        </div>
                        """
                        st.markdown(metrics_html, unsafe_allow_html=True)

                        c1, c2, c3 = st.columns(3)
                        c1.metric("Read Time", f"{seo['read_time']} min")
                        c2.metric("H3 Subheadings", seo["h3"])
                        c3.metric("Keyword Count", f"{seo['kw_density']}%")

                    with tab_meta:
                        st.markdown("**🏷️ SEO Slug**")
                        st.code(f"hopperchip.com/{slug}", language="text")

                        st.markdown("**📝 Meta Description**")
                        st.text_area("Copy this into Blogger's meta description field:", meta_desc, height=80, key=f"meta_{slug}")
                        char_count = len(meta_desc)
                        color = "#34d399" if char_count <= 155 else "#f87171"
                        st.markdown(f'<span style="color:{color}; font-family:\'JetBrains Mono\',monospace; font-size:0.75rem;">{char_count}/155 characters</span>', unsafe_allow_html=True)

                        st.markdown("**📌 Blogger Checklist**")
                        checklist = [
                            ("✅", "HTML content ready"),
                            ("✅", "Meta description generated"),
                            ("✅", "SEO slug generated"),
                            ("⬜", "Add featured image"),
                            ("⬜", "Add internal links"),
                            ("⬜", "Set labels/categories in Blogger"),
                        ]
                        for icon, item in checklist:
                            st.markdown(f"`{icon}` {item}")

                    st.markdown("---")

                except Exception as e:
                    st.error(f"Error: {e}")
else:
    st.markdown("""
    <div style="text-align:center; padding: 60px 20px; color: #475569;">
        <div style="font-size: 3rem; margin-bottom: 16px;">🔑</div>
        <div style="font-size: 1.1rem; color: #64748b; font-family:'JetBrains Mono',monospace;">
            Enter your Groq API Key in the sidebar to start generating
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="footer">HopperChip Authority Engine v4.0 · Built for hopperchip.com · Powered by Groq 2026</div>', unsafe_allow_html=True)
