# ------------------------------------------------------------
# 📚 Importlar – Gerekli kütüphaneleri yüklüyoruz
# ------------------------------------------------------------
import streamlit as st
import wikipedia
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig
)
from sentence_transformers import SentenceTransformer, util

# ------------------------------------------------------------
# 1️⃣ Sayfa ayarları (bunu Streamlit'in en başında yapmak zorundayız)
# ------------------------------------------------------------
st.set_page_config(page_title="RAG Chatbot", page_icon="⚡", layout="centered")

# ------------------------------------------------------------
# 2️⃣ Wikipedia'dan bilgi çekme ve anlam benzerliği arama kısmı
# ------------------------------------------------------------

# Wikipedia dili İngilizce olsun
wikipedia.set_lang("en")

# Bu fonksiyon ilk çağrıldığında modeli belleğe alıyor (tekrar tekrar yüklemesin diye cache'li)
@st.cache_resource
def load_embedder():
    # "all-MiniLM-L6-v2" cümle benzerlikleri için kullanılan küçük ama güçlü bir model
    return SentenceTransformer("all-MiniLM-L6-v2")

# Embedder modelini çağırıyoruz
embedder = load_embedder()

# Wikipedia'dan arama yapıp makale içeriklerini alıyoruz
def fetch_context(question, max_docs=3):
    titles = wikipedia.search(question)
    docs = []
    for t in titles[:max_docs * 2]:  # birden fazla sonuç alalım diye 2 katı kadar
        try:
            page = wikipedia.page(t)
            # sadece ilk 3000 karakteri alıyoruz, çünkü çok uzun olursa model zorlanıyor
            docs.append(page.content[:3000])
        except:
            pass
    return docs

# Bu fonksiyon soruya en çok benzeyen makale kısmını buluyor
def find_best_context(question, docs):
    if not docs:
        return None
    # Soru ve dokümanları embedding (sayısal vektör) haline getiriyoruz
    q_vec = embedder.encode(question, convert_to_tensor=True)
    d_vecs = embedder.encode(docs, convert_to_tensor=True)
    # Cosine similarity ile en benzer olanı seçiyoruz
    idx = torch.argmax(util.cos_sim(q_vec, d_vecs)).item()
    return docs[idx]

# ------------------------------------------------------------
# 3️⃣ Burada dil modelini (LLM) yüklüyoruz – model metin üretecek olan kısım
# ------------------------------------------------------------
@st.cache_resource
def load_llm():
    # Microsoft’un Phi-3-mini modeli: hızlı, küçük ve uygun kalite
    MODEL_NAME = "microsoft/Phi-3-mini-4k-instruct"

    # Modeli 4-bit olarak yüklüyoruz (daha az VRAM kullansın diye)
    bnb_config = BitsAndBytesConfig(load_in_4bit=True)

    # Tokenizer: kelimeleri modelin anlayacağı forma çeviriyor
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    # Asıl model: metin üretiminden sorumlu kısım
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        quantization_config=bnb_config,  # 4-bit modu aktif
        device_map="auto",               # GPU varsa otomatik kullan
        trust_remote_code=True
    )
    return tokenizer, model

# Model ve tokenizer’ı belleğe alıyoruz
tokenizer, model = load_llm()

# ------------------------------------------------------------
# 4️⃣ RAG (Retrieval-Augmented Generation) mantığı
# ------------------------------------------------------------

# Bu fonksiyon modeli kullanarak cevabı oluşturuyor
def generate_answer(question, context):
    # Modelin anlayacağı bir prompt (metin girdisi) oluşturuyoruz
    prompt = f"""
You are a helpful English assistant.
Use the context below to answer the question clearly and concisely.

Context:
{context[:2000]}

Question: {question}
Answer:
"""
    # Prompt'u token'lara çevirip modele veriyoruz
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    # Model cevabı oluşturuyor (generate = metin üret)
    outputs = model.generate(
        **inputs,
        max_new_tokens=250,  # en fazla 250 kelime üretebilir
        temperature=0.7,     # 0.7 olunca cevaplar daha tutarlı olur
        top_p=0.9            # nucleus sampling (çeşitlilik ayarı)
    )

    # Token'ları tekrar normal metne çeviriyoruz
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # "Answer:" kısmından sonrasını alıyoruz (öncesi prompt zaten)
    return text.split("Answer:")[-1].strip()

# Bu fonksiyon hepsini birleştiriyor:
# 1. Wikipedia'dan bilgi al
# 2. En benzer kısmı seç
# 3. LLM'e ver ve cevap üret
def rag_answer(question):
    docs = fetch_context(question)
    if not docs:
        return "No relevant Wikipedia content found."
    best_ctx = find_best_context(question, docs)
    if not best_ctx:
        return "Could not find a relevant section."
    return generate_answer(question, best_ctx)

# ------------------------------------------------------------
# 5️⃣ Streamlit arayüzü – kullanıcıyla etkileşim kısmı
# ------------------------------------------------------------
st.title("⚡ Fast English RAG Chatbot (Student Version)")
st.caption("Type any question below and I’ll try to find the answer using Wikipedia and an AI model 🤖")

# Kullanıcıdan soru alıyoruz
question = st.text_area(
    "Your question:",
    placeholder="e.g. What is quantum computing?",
    height=100
)

# Butona basıldığında modeli çalıştırıyoruz
if st.button("🔍 Ask"):
    if not question.strip():
        st.warning("Please enter a question.")  # boş giriş olmasın
    else:
        with st.spinner("Thinking 🤔 ..."):      # yükleme animasyonu
            answer = rag_answer(question)
        st.success("✅ Answer:")                 # sonuç gösteriliyor
        st.markdown(answer)
