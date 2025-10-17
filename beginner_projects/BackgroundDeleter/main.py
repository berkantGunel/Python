from rembg import remove
from PIL import Image
import os
import threading
import time
import uuid

# Hata alınan dosyaları takip etmek için bir liste oluştur
failed_files = []

# Renk tanımları
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
RESET = '\033[0m'
text = "GYMCORE"
colors = [RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE]

for i, char in enumerate(text):
    color = colors[i % len(colors)]  # Renkleri döngüye sok
    print(f"{color}{char}{RESET}", end='')

print()


def process_image(inputPath, outputPath):
    try:
        print(f"{CYAN}Processing {inputPath}{RESET}")

        # Dosyaları binary modda oku
        with open(inputPath, "rb") as i:
            inputFile = i.read()
            outputFile = remove(inputFile)

            # Benzersiz geçici dosya adı oluştur
            temp_path = os.path.join(output_folder, f"temp_{uuid.uuid4().hex}.png")
            with open(temp_path, "wb") as temp:
                temp.write(outputFile)

            # Arka planı beyaz yap ve son dosyayı oluştur
            with Image.open(temp_path) as img:
                img = img.convert("RGBA")
                # Yeni beyaz arka plan
                white_bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
                white_bg.paste(img, (0, 0), img)
                white_bg.convert("RGB").save(outputPath, "PNG")

        # Geçici dosyayı sil
        os.remove(temp_path)

        # Her resim işleminden sonra 2 saniye bekle
        time.sleep(4)

        print(f"{GREEN}Success: {inputPath}{RESET}")

    except Exception as e:
        # Hata durumunda dosya ismini kaydet
        failed_files.append(inputPath)
        print(f"{RED}Error processing file {inputPath}: {e}{RESET}")


def process_images(input_folder, output_folder):
    # Eğer çıktı klasörü mevcut değilse oluştur
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    files = [f for f in os.listdir(input_folder) if f.endswith(('jpeg', 'jpg', 'png'))]

    threads = []

    for file in files:
        inputPath = os.path.join(input_folder, file)
        outputPath = os.path.join(output_folder, file)

        thread = threading.Thread(target=process_image, args=(inputPath, outputPath))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    if failed_files:
        print(f"\n{RED}Bu dosyalar işlenemedi:")
        for file in failed_files:
            print(file)
    else:
        print(f"\n{GREEN}Tüm dosyalar başarıyla işlendi{RESET}")


input_folder = str(input(f"{BLUE}Dosya İsmi: {RESET}"))
output_folder = str(input(f"{BLUE}Nereye Kaydolsun: {RESET}"))
process_images(input_folder, output_folder)
