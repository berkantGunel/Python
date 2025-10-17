#WEB-SCRAPING

import requests
from bs4 import BeautifulSoup
URL = "https://www.amazon.com.tr/HP-Diz%C3%BCst%C3%BC-Bilgisayar-Performans-71T73EA/dp/B0BH4LK6NH/ref=sr_1_6?dib=eyJ2IjoiMSJ9.8d8H1qtclgBIZa7j3pTA7Z6yF8_ennfnlUGPHna7NM96BbScS7vdeo-PvauFKnxWxGl9yzbrzu2IHNVaWu6LdviUVVlzFZZtIixLKgwQzOVeL5J8tXjsG3deM0cbPYH-W7ZtVf-qqNS0gWYpb5cdUqpRvT95JC3ikfbqzKe31bAVkFV8EFfQUCRMfQFFTUIu2lnNZ0q8SPrL5ETaqhCuqq-GmopXzEqMb_uxAxvuOb5sTiw5JfprakqH2ZE1Nrtpz3dEy2J-MVUSuyqyIRwW5M5NgAiG4SCHE9bi3HeHjJk.f6LVgvmtrR6W51i7ubQIV4DKEHedxV5F71mhi4NVFE8&dib_tag=se&keywords=laptop&qid=1722446298&sr=8-6"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"}
page = requests.get(URL, headers=headers)
content = BeautifulSoup(page.content, 'html.parser')

productName = content.find(id='productTitle').getText().strip()
productPrice = content.find(class_='a-price-whole').getText().strip()
productConverted = productPrice[0:6].replace(".","")
print(productName)
print(productConverted)

