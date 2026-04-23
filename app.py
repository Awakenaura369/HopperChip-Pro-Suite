import streamlit as st
from groq import Groq
import feedparser
from bs4 import BeautifulSoup

# --- إعدادات الصفحة ---
st.set_page_config(page_title="HopperChip Auto-Pilot v2.2", page_icon="⚡", layout="wide")

# --- ستايل الواجهة ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #eee; border-radius: 5px; }
    .stTabs [aria-selected="true"] { background-color: #007bff !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 HopperChip Content Machine")
st.caption("نظام أتمتة المقالات التقنية لمدونة HopperChip.com")

# --- القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.header("🛠️ التحكم والأمان")
    api_key = st.text_input("Enter Groq API Key:", type="password", help="حط هنا الـ API Key ديالك من Groq Cloud")
    
    # قائمة الموديلات المستقرة حالياً في 2026
    model_choice = st.selectbox("اختر الموديل:", [
        "llama-3.3-70b-versatile", 
        "llama-3.1-70b-versatile",
        "llama-3.1-8b-instant",
        "mixtral-8x7b-32768"
    ], index=0)
    
    language = st.selectbox("لغة المقال:", ["Arabic", "English", "French"])
    
    st.markdown("---")
    st.header("📡 مصادر الأخبار")
    RSS_SOURCES = {
        "TechCrunch Hardware": "https://techcrunch.com/category/hardware/feed/",
        "The Verge": "https://www.theverge.com/rss/index.xml",
        "Engadget": "https://www.engadget.com/rss.xml",
        "Ars Technica": "https://feeds.arstechnica.com/arstechnica/index"
    }
    source_choice = st.selectbox("المصدر:", list(RSS_SOURCES.keys()))
    num_posts = st.slider("عدد المقالات:", 1, 5, 2)

# --- المحرك الرئيسي ---
if api_key:
    try:
        client = Groq(api_key=api_key)
        
        if st.button("🔄 جلب الأخبار وصناعة المقالات"):
            with st.spinner('جاري معالجة البيانات...'):
                feed = feedparser.parse(RSS_SOURCES[source_choice])
                
                if not feed.entries:
                    st.error("المصدر مارد تا شي خبر، جرب مصدر آخر.")
                else:
                    for entry in feed.entries[:num_posts]:
                        # تنظيف المحتوى الأصلي
                        raw_html = entry.summary if 'summary' in entry else entry.description
                        clean_text = BeautifulSoup(raw_html, "html.parser").get_text()

                        # الـ Prompt الاحترافي لـ SEO
                        prompt = f"""
                        Rewrite this tech news into a professional SEO blog post for 'HopperChip.com'.
                        Language: {language}.
                        Format: PURE HTML (use <h2>, <h3>, <p>, <ul>, <li>, <strong>).
                        
                        Context:
                        Original Title: {entry.title}
                        Original Content: {clean_text}
                        
                        Requirements:
                        - Create a catchy SEO title.
                        - Use <h2> and <h3> tags for sections.
                        - Professional tech terminology only.
                        - Include a 'Technical Verdict' at the end.
                        - NO conversational text, output ONLY the HTML code.
                        """

                        try:
                            # استدعاء الموديل
                            completion = client.chat.completions.create(
                                messages=[{"role": "user", "content": prompt}],
                                model=model_choice,
                                temperature=0.5
                            )
                            
                            html_output = completion.choices[0].message.content

                            # عرض النتائج
                            st.markdown(f"### ✅ تم التوليد: {entry.title}")
                            t1, t2 = st.tabs(["👁️ المعاينة", "📄 الكود"])
                            
                            with t1:
                                st.markdown(f"<div style='background:white; padding:15px; border:1px solid #ddd;'>{html_output}</div>", unsafe_allow_html=True)
                            
                            with t2:
                                st.code(html_output, language="html")
                                st.download_button(f"Download HTML ({entry.title[:10]})", html_output, file_name=f"post_{entry.title[:10]}.html")
                            
                            st.markdown("---")

                        except Exception as model_err:
                            if "decommissioned" in str(model_err):
                                st.error(f"❌ الموديل '{model_choice}' مابقاش خدام. جرب تختار 'llama-3.1-8b-instant' من الجنب.")
                            else:
                                st.error(f"❌ خطأ في الموديل: {model_err}")

    except Exception as e:
        st.error(f"❌ خطأ عام: {e}")
else:
    st.info("👈 حط الـ API Key ديالك في القائمة الجانبية باش تبدا الأتمتة.")

st.sidebar.markdown("---")
st.sidebar.caption("HopperChip Pro Suite v2.2 | Built for Automation")
