import streamlit as st
from groq import Groq
import feedparser
from bs4 import BeautifulSoup

# إعداد الصفحة
st.set_page_config(page_title="HopperChip Auto-Pilot v2.0", page_icon="🤖", layout="wide")

st.title("🤖 HopperChip Auto-Pilot: Content Machine")
st.markdown("هاد الأداة كتجيب آخر أخبار المعالجات وتعاود صياغتها بـ HTML واجد للمدونة ديالك.")

# الإعدادات في الجانب
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("Enter Groq API Key:", type="password")
    lang = st.selectbox("Language / اللغة:", ["Arabic", "English"])
    # مصادر الأخبار التقنية (تقدر تزيد روابط RSS أخرى هنا)
    RSS_SOURCES = {
        "TechCrunch Hardware": "https://techcrunch.com/category/hardware/feed/",
        "The Verge Tech": "https://www.theverge.com/rss/index.xml",
        "PC Gamer (Hardware)": "https://www.pcgamer.com/rss/",
        "Engadget": "https://www.engadget.com/rss.xml"
    }
    source_choice = st.selectbox("Select News Source:", list(RSS_SOURCES.keys()))

if api_key:
    client = Groq(api_key=api_key)
    
    if st.button("🚀 Start Fetching & Rewriting"):
        with st.spinner('جاري جلب الأخبار ومعالجتها...'):
            try:
                # 1. جلب الأخبار من الـ RSS
                feed = feedparser.parse(RSS_SOURCES[source_choice])
                
                if not feed.entries:
                    st.error("لم يتم العثور على أخبار في هذا المصدر حالياً.")
                else:
                    # نأخذ آخر 5 أخبار فقط لتوفير الـ API Quota
                    for entry in feed.entries[:5]:
                        st.markdown("---")
                        st.subheader(f"📍 Original Title: {entry.title}")
                        
                        # تنظيف محتوى الخبر الأصلي
                        content_raw = entry.summary if 'summary' in entry else entry.description
                        soup = BeautifulSoup(content_raw, "html.parser")
                        clean_text = soup.get_text()

                        # 2. إرسال المحتوى لـ Groq لإعادة الصياغة بـ HTML
                        prompt = f"""
                        You are an expert tech blogger for 'HopperChip.com'. 
                        Task: Rewrite the following news article into a high-quality, SEO-optimized blog post.
                        Language: {lang}.
                        Format: PURE HTML (use <h2>, <h3>, <p>, <ul>, <li>, <strong>).
                        
                        Original News:
                        Title: {entry.title}
                        Summary: {clean_text}
                        
                        Requirements:
                        - Create a new catchy SEO title.
                        - Structure with H2 and H3 tags.
                        - Write a detailed technical analysis.
                        - Add a 'Verdict' or 'Conclusion' section.
                        - Output ONLY the HTML code.
                        """

                        completion = client.chat.completions.create(
                            messages=[{"role": "user", "content": prompt}],
                            model="llama3-70b-8192", # موديل قوي للتحليل التقني
                            temperature=0.5
                        )
                        
                        html_output = completion.choices[0].message.content

                        # 3. عرض النتائج
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.info("👁️ Visual Preview (How it looks):")
                            st.markdown(html_output, unsafe_allow_html=True)
                        
                        with col2:
                            st.success("📄 HTML Code (Copy-Paste):")
                            st.code(html_output, language="html")
                            st.download_button(f"Download HTML", html_output, file_name=f"post_{entry.title[:20]}.html")
                            
            except Exception as e:
                st.error(f"حدث خطأ: {e}")
else:
    st.warning("👈 يرجى إدخال Groq API Key في القائمة الجانبية للبدء.")

st.markdown("---")
st.caption("Custom Build for HopperChip.com | Powered by Groq & Streamlit")
