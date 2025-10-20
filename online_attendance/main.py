# -*- coding: utf-8 -*-
import time
import os
import pyautogui
from PIL import Image
from pyzbar.pyzbar import decode
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import winsound
from datetime import datetime

# 1️⃣ Ogrenci numarasini al / kaydet
NUMARA_DOSYA = "numara.txt"

if not os.path.exists(NUMARA_DOSYA):
    ogr_no = input("Ogrenci numarani gir: ").strip()
    with open(NUMARA_DOSYA, "w", encoding="utf-8") as f:
        f.write(ogr_no)
else:
    with open(NUMARA_DOSYA, "r", encoding="utf-8") as f:
        ogr_no = f.read().strip()

print(f"Ogrenci numarasi: {ogr_no}")

# 2️⃣ Log fonksiyonu
def log_yaz(metin):
    with open("katilim_log.txt", "a", encoding="utf-8") as log:
        zaman = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"[{zaman}] {metin}\n")

# 3️⃣ QR kod tarama fonksiyonu
def ekran_qr_tara():
    screenshot = pyautogui.screenshot()
    frame = screenshot.convert("RGB")
    barcodes = decode(frame)
    for barcode in barcodes:
        qr_data = barcode.data.decode("utf-8")
        return qr_data
    return None

# 4️⃣ Tarayici baslat
driver = None
print("Ekranda QR kod bekleniyor... (Cikmak icin Ctrl+C)")

# 5️⃣ Ana dongu
while True:
    try:
        qr_link = ekran_qr_tara()

        if qr_link:
            print("QR bulundu:", qr_link)
            log_yaz(f"QR bulundu: {qr_link}")

            # Tarayiciyi baslat
            if driver is None:
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service)

            # Sayfayi ac
            driver.get(qr_link)
            time.sleep(2)

            # Numara kutusunu bul ve doldur
            input_box = driver.find_element(By.CSS_SELECTOR, "input.ogrenciNo")
            input_box.clear()
            input_box.send_keys(ogr_no)

            # Butona tikla
            button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-success-2.fw-semibold")
            button.click()

            # Sesli bildirim
            winsound.Beep(800, 400)
            winsound.Beep(1000, 400)

            # Log kaydi
            log_yaz("Derse katilim basariyla tamamlandi.")
            print("Katilim tamamlandi! QR tekrar bekleniyor...")

            time.sleep(10)  # Ayni QR'i tekrar okumamak icin bekleme

        time.sleep(1)

    except KeyboardInterrupt:
        print("\nProgram sonlandirildi.")
        log_yaz("Program manuel olarak sonlandirildi.")
        break

    except Exception as e:
        print("Hata:", e)
        log_yaz(f"Hata: {e}")
        time.sleep(3)
