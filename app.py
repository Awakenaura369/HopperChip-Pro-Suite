import streamlit as st
from groq import Groq
import feedparser
from bs4 import BeautifulSoup

# --- Configuration ---
st.set_page_config(page_title="HopperChip Authority v2.3", page_icon="🏆", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #fafafa; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #f0f2f6; border-radius: 5px; padding: 10px; }
    .reportview-container .main .block-container { padding-top: 2rem; }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.header("💎 HopperChip Control")
    api_key = st.text_input("Enter Groq API Key:", type="password")
    
    # اختيار الموديل الأقوى للمقالات الطويلة
    model_choice = st.selectbox("Engine:", [
        "llama-3.3-70b-versatile", 
        "llama-3.1-70b-versatile"
    ])
    
    language = st.selectbox("Content Language:", ["Arabic", "English"])
    
    st.markdown("---")
    st.header("📡 News Feed")
    RSS_SOURCES = {
        "TechCrunch (Hardware)": "https://techcrunch.com/category/hardware/feed/",
        "The Verge (Tech)": "https://www.theverge.com/rss/index.xml",
        "Wired (Gear)": "https://www.wired.com/feed/category/gear/latest/rss",
        "Ars Technica": "https://feeds.arstechnica.com/arstechnica/index"
    }
    source_choice = st.selectbox("Target Source:", list(RSS_SOURCES.keys()))
    num_articles = st.slider("Articles to generate:", 1, 3, 1)

if api_key:
    client = Groq(api_key=api_key)
    
    if st.button("🔥 Generate High-Authority Articles"):
        with st.spinner('جاري بناء مقالات احترافية (قد يستغرق الأمر 30 ثانية لكل مقال)...'):
            feed = feedparser.parse(RSS_SOURCES[source_choice])
            
            for entry in feed.entries[:num_articles]:
                raw_summary = entry.summary if 'summary' in entry else entry.description
                clean_context = BeautifulSoup(raw_summary, "html.parser").get_text()

                # --- الـ Prompt "الوحش" للمقالات الطويلة والعميقة ---
                master_prompt = f"""
                You are a Senior Tech Analyst and Journalist for 'HopperChip.com'. 
                Your task is to write a comprehensive, 1000-word authority article based on this news: {entry.title}.
                Language: {language}.
                
                ### CONTENT STRATEGY:
                1. **Hook Title**: Create a magnetic, SEO-optimized title (H1).
                2. **The Big Picture**: Start with a deep introduction (3-4 paragraphs). Why does this news matter? What is the historical context?
                3. **Technical Deep-Dive (H2)**: Explain the 'under-the-hood' details. Focus on semiconductors, architecture, nanometer nodes, or software optimization. Use technical jargon correctly.
                4. **Market Disruption (H2)**: How will this affect competitors (Intel, AMD, Nvidia, Apple)? Analyze the business side.
                5. **Detailed Specifications Table**: Create a clean HTML table with all available technical data.
                6. **Pros, Cons & Performance**: A detailed section analyzing potential performance gains or drawbacks.
                7. **Expert Verdict (H2)**: Provide a final, authoritative score and recommendation. Who is this for?
                
                ### FORMATTING RULES:
                - Use HTML tags only (<h2>, <h3>, <p>, <ul>, <li>, <strong>, <table>).
                - NO conversational filler (e.g., "Here is the article").
                - Ensure the tone is professional, critical, and analytical.
                - Maximize word count by providing detailed explanations for every technical claim.
                
                Source Data: {clean_context}
                """

                try:
                    completion = client.chat.completions.create(
                        messages=[{"role": "user", "content": master_prompt}],
                        model=model_choice,
                        temperature=0.65 # توازن بين الإبداع والدقة التقنية
                    )
                    
                    final_html = completion.choices[0].message.content

                    # --- عرض النتيجة ---
                    st.success(f"Successfully Generated: {entry.title}")
                    
                    tab1, tab2, tab3 = st.tabs(["📝 Authority Preview", "💻 HTML Code", "📊 SEO Stats"])
                    
                    with tab1:
                        st.markdown(f"<div style='background:white; padding:40px; border:1px solid #ddd; border-radius:10px; color:#333; line-height:1.6;'>{final_html}</div>", unsafe_allow_html=True)
                    
                    with tab2:
                        st.code(final_html, language="html")
                        st.download_button("Download HTML", final_html, file_name=f"hopperchip_{entry.title[:20]}.html")
                    
                    with tab3:
                        word_count = len(final_html.split())
                        st.metric("Estimated Word Count", f"~{word_count} words")
                        st.info("SEO Tip: Add high-quality images of the hardware to increase engagement by 40%.")
                    
                    st.markdown("---")

                except Exception as e:
                    st.error(f"Error during generation: {e}")
else:
    st.info("👈 Please enter your Groq API Key to launch the HopperChip Engine.")
