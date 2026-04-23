import streamlit as st
from groq import Groq

st.set_page_config(page_title="HopperChip Pro Suite", page_icon="🚀", layout="wide")

st.title("🚀 HopperChip Content & Social Engine")
st.markdown("Generate Articles, Comparisons, and Social Media Promos in seconds.")

with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Groq API Key:", type="password")
    model_choice = st.selectbox("Model", ["llama3-70b-8192", "llama3-8b-8192"])
    language = st.selectbox("Language", ["Arabic", "English", "French"])

if api_key:
    client = Groq(api_key=api_key)
    
    # زيادة Tab جديد للـ Social Media
    tab1, tab2, tab3 = st.tabs(["📄 SEO Articles", "⚔️ Comparisons", "📱 Social Media"])

    # --- Tab 1: المقالات ---
    with tab1:
        st.subheader("Write SEO Article")
        chip_name = st.text_input("Processor Name:")
        if st.button("Generate Article"):
            prompt = f"Write a full SEO tech article about {chip_name} in {language}. Include specs, benchmarks and verdict."
            res = client.chat.completions.create(messages=[{"role":"user","content":prompt}], model=model_choice).choices[0].message.content
            st.markdown(res)

    # --- Tab 2: المقارنات ---
    with tab2:
        st.subheader("Chip Battle")
        c1, c2 = st.columns(2)
        with c1: chip_a = st.text_input("Chip A:")
        with c2: chip_b = st.text_input("Chip B:")
        if st.button("Compare"):
            prompt = f"Compare {chip_a} vs {chip_b} in a table. Language: {language}."
            res = client.chat.completions.create(messages=[{"role":"user","content":prompt}], model=model_choice).choices[0].message.content
            st.markdown(res)

    # --- Tab 3: السوشيال ميديا (الجديد) ---
    with tab3:
        st.subheader("Generate Viral Social Posts")
        article_summary = st.text_area("عن ماذا يتحدث المقال؟ (مثلاً: إطلاق معالج Intel الجديد)")
        platform = st.multiselect("اختر المنصات:", ["Facebook", "Twitter (X)", "LinkedIn"])
        
        if st.button("Generate Social Pack"):
            if article_summary:
                with st.spinner('قيد الإنشاء...'):
                    social_prompt = f"""
                    Create professional social media posts for {platform} based on this: {article_summary}.
                    Language: {language}.
                    Requirements:
                    - Use emojis related to tech/chips.
                    - Include high-traffic hashtags.
                    - Add a clear Call-to-Action (CTA) to read the full article.
                    - Tone: Exciting and professional.
                    """
                    res = client.chat.completions.create(
                        messages=[{"role": "user", "content": social_prompt}],
                        model=model_choice
                    ).choices[0].message.content
                    st.info("Your Social Media Posts:")
                    st.markdown(res)
            else:
                st.warning("دخل شي ملخص باش يعرف الـ AI شنو يكتب.")

else:
    st.info("👈 Enter your Groq API Key to start.")

st.markdown("---")
st.caption("Custom built for HopperChip.com Automation")
