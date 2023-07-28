import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Inicjalizacja opcji przeglądarki
options = Options()
options.headless = True

# Inicjalizacja przeglądarki
driver = webdriver.Chrome(options=options)

BASE_URL = "http://quotes.toscrape.com/js-delayed/"
current_page = 1

# Otwórz plik do zapisu danych w formacie JSONL
with open("output.jsonl", "w", encoding="utf-8") as jsonl_file:
    while True:
        url = f"{BASE_URL}page/{current_page}/"
        driver.get(url)

        # Poczekaj na załadowanie się skryptu i danych
        time.sleep(10)

        # Pobierz dane z obiektów
        elements = driver.find_elements(By.CLASS_NAME, "quote")

        for element in elements:
            text = element.find_element(By.CLASS_NAME, "text").text.strip('"\u201c\u201d')
            # Zamień niepożądane znaki na standardowe odpowiedniki w polu "text"
            text = text.replace("\u2032", "'").replace("\u2019", "'").replace("\u00e9", "é")
            
            author = element.find_element(By.CLASS_NAME, "author").text
            # Zamień niepożądane znaki na standardowe odpowiedniki w polu "by"
            author = author.replace("\u00e9", "é")
            
            tags_elements = element.find_elements(By.CLASS_NAME, "tag")
            tags = [tag.text for tag in tags_elements]

            # Zapisz dane do pliku JSONL
            data = {
                "text": text,
                "by": author,
                "tags": tags
            }
            json.dump(data, jsonl_file)
            jsonl_file.write("\n")

        # Sprawdź, czy istnieje link "Next" do następnej strony
        try:
            next_link_element = driver.find_element(By.CLASS_NAME, "next")
            next_link = next_link_element.find_element(By.TAG_NAME, "a").get_attribute("href")
        except:
            break  # Przerwij pętlę, jeśli nie ma kolejnej strony

        # Przejdź do kolejnej strony
        current_page += 1

# Zamknij przeglądarkę
driver.quit()
