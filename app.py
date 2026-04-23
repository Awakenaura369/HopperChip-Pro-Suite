import streamlit as st
from groq import Groq
import feedparser
from bs4 import BeautifulSoup

# إعداد الصفحة وتصميمها
st.set_page_config(page_title="HopperChip Auto-Pilot v2.1", page_icon="⚡", layout="wide")

# ستايل CSS خفيف باش تبان الواجهة احترافية
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    .stCodeBlock { border: 1px solid #e0e0e0; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 HopperChip Auto-Pilot Engine")
st.subheader("أتمتة المحتوى التقني باستخدام الـ AI والأخبار المباشرة")

# القائمة الجانبية للإعدادات
with st.sidebar:
    st.header("⚙️ الإعدادات والتحكم")
    api_key = st.text_input("Enter Groq API Key:", type="password")
    
    # تحديث قائمة الموديلات لآخر إصدارات 2026
    model_choice = st.selectbox("Select Model:", [
        "llama-3.3-70b-specdec", 
        "llama-3.1-8b-instant",
        "mixtral-8x7b-32768"
    ])
    
    language = st.selectbox("لغة المقال:", ["Arabic", "English", "French"])
    
    st.markdown("---")
    st.header("🌐 مصادر الأخبار")
    RSS_SOURCES = {
        "TechCrunch (Hardware)": "https://techcrunch.com/category/hardware/feed/",
        "The Verge": "https://www.theverge.com/rss/index.xml",
        "Ars Technica": "https://feeds.arstechnica.com/arstechnica/index",
        "Engadget": "https://www.engadget.com/rss.xml"
    }
    source_choice = st.selectbox("اختر مصدر الخبر:", list(RSS_SOURCES.keys()))
    num_posts = st.slider("عدد المقالات لمعالجتها:", 1, 5, 3)

# المحرك الرئيسي
if api_key:
    client = Groq(api_key=api_key)
    
    if st.button("🔄 إبدأ جلب الأخبار وإعادة الصياغة"):
        with st.spinner('جاري الاتصال بالمصادر وتحليل البيانات...'):
            try:
                # 1. جلب البيانات من RSS
                feed = feedparser.parse(RSS_SOURCES[source_choice])
                
                if not feed.entries:
                    st.error("لم نتمكن من جلب الأخبار من هذا المصدر حالياً.")
                else:
                    for entry in feed.entries[:num_posts]:
                        st.markdown(f"### 📰 الخبر الأصلي: {entry.title}")
                        
                        # تنظيف النص
                        content_raw = entry.summary if 'summary' in entry else entry.description
                        soup = BeautifulSoup(content_raw, "html.parser")
                        clean_text = soup.get_text()

                        # 2. إعداد الـ Prompt الاحترافي لـ SEO
                        prompt = f"""
                        Task: Rewrite this technical news into a professional, SEO-friendly blog post for 'HopperChip.com'.
                        Target Language: {language}.
                        Output Format: HTML ONLY (use <h2>, <h3>, <p>, <ul>, <li>, <strong>).
                        
                        Context:
                        Original Title: {entry.title}
                        Original Content: {clean_text}
                        
                        Specific Instructions:
                        - Create a new, unique SEO title that attracts clicks.
                        - Break the content into logical sections with <h2> and <h3> headers.
                        - Use professional tech terminology (Processors, Nano-tech, Architecture, etc.).
                        - Include a 'Technical Verdict' section at the end.
                        - Ensure the HTML is clean and ready for WordPress/Blogger.
                        - DO NOT include any conversational text, ONLY the HTML code.
                        """

                        # 3. استدعاء الموديل الجديد
                        completion = client.chat.completions.create(
                            messages=[{"role": "user", "content": prompt}],
                            model=model_choice,
                            temperature=0.4 # درجة منخفضة لضمان الدقة التقنية
                        )
                        
                        html_output = completion.choices[0].message.content

                        # 4. عرض النتائج للمستخدم
                        tab_view, tab_code = st.tabs(["👁️ معاينة المقال", "📄 كود HTML"])
                        
                        with tab_view:
                            st.markdown(f"<div style='border: 1px solid #ddd; padding: 20px; border-radius: 10px; background: white;'>{html_output}</div>", unsafe_allow_html=True)
                        
                        with tab_code:
                            st.code(html_output, language="html")
                            st.download_button(
                                label="Download HTML File",
                                data=html_output,
                                file_name=f"hopperchip_{entry.title[:15]}.html",
                                mime="text/html"
                            )
                        st.markdown("---")
                        
            except Exception as e:
                st.error(f"خطأ تقني: {e}")
else:
    st.info("👈 يرجى إدخال Groq API Key في القائمة الجانبية لتفعيل الماكينة.")

st.sidebar.markdown("---")
st.sidebar.caption("HopperChip Pro Suite v2.1 | Built with ❤️ for Automation")
