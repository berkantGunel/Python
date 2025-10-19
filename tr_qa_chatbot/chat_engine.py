# chat_engine.py
import random

def sohbet_cevapla(soru: str) -> str:
    """Kural tabanlı basit Türkçe sohbet motoru."""
    soru = soru.lower()

    selamlar = ["merhaba", "selam", "selamün aleyküm", "günaydın", "iyi akşamlar"]
    nasilsin = ["nasılsın", "nasılsın?", "nasılsın bugün", "nasıl gidiyor"]
    tesekkur = ["teşekkür", "sağ ol", "thanks", "eyvallah"]
    vedalar = ["görüşürüz", "bye", "hoşçakal", "kendine iyi bak"]

    if any(k in soru for k in selamlar):
        return random.choice(["Merhaba! 😊", "Selam! Nasılsın?", "Aleyküm selam!"])
    elif any(k in soru for k in nasilsin):
        return random.choice(["İyiyim, sen nasılsın?", "Harikayım! Sen?", "Fena değilim, sen nasılsın?"])
    elif any(k in soru for k in tesekkur):
        return random.choice(["Rica ederim 🤗", "Ne demek!", "Her zaman!"])
    elif any(k in soru for k in vedalar):
        return random.choice(["Görüşürüz 👋", "Hoşçakal!", "Kendine dikkat et!"])
    else:
        return random.choice([
            "Bunu tam anlayamadım ama ilgimi çekti 🤔",
            "İlginç bir soru, biraz daha açar mısın?",
            "Hmm... bilmiyorum ama kulağa ilginç geliyor 😅"
        ])
