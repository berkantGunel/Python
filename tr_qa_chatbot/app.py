# app.py
import streamlit as st
from qa_engine import cevap_uret

st.set_page_config(
    page_title="Bilgi Chatbotu 🇹🇷",
    page_icon="💬",
    layout="centered"
)

st.title("💬 Türkçe Bilgi Chatbotu")
st.caption("Wikipedia tabanlı akıllı soru-cevap ve sohbet sistemi. 🇹🇷")

soru = st.text_area("Sorunu yaz 👇", placeholder="Örneğin: Atatürk kimdir?", height=100)

if st.button("🔍 Gönder"):
    if not soru.strip():
        st.warning("Lütfen bir soru yaz.")
    else:
        with st.spinner("🤔 Düşünüyorum..."):
            cevap = cevap_uret(soru)
        st.success("✅ Cevap:")
        st.markdown(cevap)
