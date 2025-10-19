# qa_engine.py
import re
import wikipedia
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForQuestionAnswering,
    pipeline
)
from chat_engine import sohbet_cevapla  # 🔹 GPT-2 sohbet modeli

# --- Wikipedia ayarı ---
wikipedia.set_lang("tr")

# --- Bilgi (Question Answering) modeli ---
QA_MODEL = "savasy/bert-base-turkish-squad"

print("🔄 Bilgi modeli yükleniyor... (ilk seferde biraz sürebilir)")
qa_tokenizer = AutoTokenizer.from_pretrained(QA_MODEL)
qa_model = AutoModelForQuestionAnswering.from_pretrained(QA_MODEL)

device = 0 if torch.cuda.is_available() else -1
qa_pipeline = pipeline(
    "question-answering",
    model=qa_model,
    tokenizer=qa_tokenizer,
    device=device
)

# --- Yardımcı fonksiyonlar ---
def temizle(metin: str) -> str:
    """Wikipedia metninden gereksiz boşluk ve referansları temizler."""
    metin = re.sub(r"\[[0-9]+\]", "", metin)
    metin = re.sub(r"\s+", " ", metin).strip()
    return metin

def wiki_ara(soru: str) -> tuple[str, str] | None:
    """Wikipedia'dan en alakalı içeriği ve başlığı döndürür."""
    try:
        basliklar = wikipedia.search(soru)
        if not basliklar:
            return None
        soru_kelimeleri = set(soru.lower().split())
        en_iyi = max(basliklar, key=lambda t: len(set(t.lower().split()) & soru_kelimeleri))
        sayfa = wikipedia.page(en_iyi)
        return temizle(sayfa.content[:4000]), sayfa.title
    except Exception as e:
        print("Wikipedia hatası:", e)
        return None

def anlamli_mi(cevap: str) -> bool:
    """Cevabın anlamlı olup olmadığını kontrol eder."""
    if not cevap or len(cevap.split()) < 2:
        return False
    if any(k in cevap.lower() for k in ["bilinmemektedir", "yoktur", "belirsiz", "bir şeydir"]):
        return False
    if len(cevap) > 200:
        return False
    return True

# --- Ana cevap üretici ---
def cevap_uret(soru: str) -> str:
    bilgi_kelime = any(k in soru.lower() for k in [
        "nedir", "kimdir", "ne zaman", "kaç", "hangi", "nerede", "nasıl oluşur", "tanımı"
    ])

    # 1️⃣ Bilgi Modu
    if bilgi_kelime:
        sonuc = wiki_ara(soru)
        if not sonuc:
            return "Bu konuda bilgi bulamadım."
        context, title = sonuc
        try:
            output = qa_pipeline({"question": soru, "context": context})
            cevap = output.get("answer", "").strip()
            if anlamli_mi(cevap):
                return f"**Kaynak:** [{title} - Wikipedia]\n\n{cevap}"
        except Exception as e:
            print("Model hatası:", e)

    # 2️⃣ Sohbet modu (yedek)
    return sohbet_cevapla(soru)
