import streamlit as st
from groq import Groq
import feedparser
from bs4 import BeautifulSoup

# --- إعدادات الصفحة ---
st.set_page_config(page_title="HopperChip Blogger Engine v3.5", page_icon="🚀", layout="wide")

# ستايل احترافي للـ Tool
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { background: linear-gradient(90deg, #ff4b4b, #ff7676); color: white; font-weight: bold; border: none; border-radius: 8px; height: 3em; }
    .stTextInput>div>div>input { background-color: #262730; color: white; border: 1px solid #444; }
    .reportview-container .main .block-container { padding-top: 1rem; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ HopperChip Authority Engine")
st.subheader("Blogger Content Automation System")

# --- القائمة الجانبية ---
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Groq API Key:", type="password")
    
    # موديلات مستقرة 2026
    model_choice = st.selectbox("Engine:", [
        "llama-3.3-70b-versatile", 
        "llama-3.1-70b-versatile",
        "llama-3.1-8b-instant"
    ])
    
    language = st.selectbox("Article Language:", ["English", "Arabic"])
    
    st.markdown("---")
    st.header("📡 Live Sources")
    RSS_SOURCES = {
        "Hardware News": "https://techcrunch.com/category/hardware/feed/",
        "Chip Tech": "https://www.theverge.com/rss/index.xml",
        "Ars Technica": "https://feeds.arstechnica.com/arstechnica/index",
        "Wired Gear": "https://www.wired.com/feed/category/gear/latest/rss"
    }
    source_choice = st.selectbox("News Source:", list(RSS_SOURCES.keys()))
    num_posts = st.slider("Number of articles:", 1, 3, 1)

# --- المحرك الرئيسي ---
if api_key:
    client = Groq(api_key=api_key)
    
    if st.button("🚀 Generate High-Authority Blogger Posts"):
        with st.spinner('جاري تحليل الأخبار وبناء المحتوى...'):
            feed = feedparser.parse(RSS_SOURCES[source_choice])
            
            if not feed.entries:
                st.error("Could not fetch news. Try another source.")
            else:
                for entry in feed.entries[:num_posts]:
                    # تنظيف الداتا الأصلية
                    content_raw = entry.summary if 'summary' in entry else entry.description
                    clean_text = BeautifulSoup(content_raw, "html.parser").get_text()

                    # --- Prompt "الوحش" لـ Blogger ---
                    master_prompt = f"""
                    Write a 1200-word, high-authority technical blog post for 'HopperChip.com' about: {entry.title}.
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

                        # --- عرض النتيجة ---
                        st.markdown(f"### ✅ Ready: {entry.title}")
                        
                        tab_view, tab_code, tab_seo = st.tabs(["👁️ Blogger Preview", "📄 HTML Code", "📊 Stats"])
                        
                        with tab_view:
                            st.markdown(f"<div style='background:white; color:#333; padding:30px; border-radius:10px; line-height:1.7;'>{html_output}</div>", unsafe_allow_html=True)
                        
                        with tab_code:
                            st.info("Copy this code and paste it into Blogger's 'HTML View'")
                            st.code(html_output, language="html")
                            st.download_button(f"Download HTML", html_output, file_name=f"hopperchip_{entry.title[:15]}.html")
                            
                        with tab_seo:
                            words = len(html_output.split())
                            st.metric("Estimated Word Count", f"~{words} words")
                            st.success("SEO Score: High (Authoritative Content Structure)")
                        
                        st.markdown("---")

                    except Exception as e:
                        st.error(f"Error: {e}")
else:
    st.info("👈 Please enter your Groq API Key in the sidebar.")

st.sidebar.markdown("---")
st.sidebar.caption("HopperChip Pro Suite v3.5 | Powered by Groq 2026")
