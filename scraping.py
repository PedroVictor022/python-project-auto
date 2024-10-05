from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import datetime
import csv

class NewsScraper:
    def __init__(self, search_term, output_csv, qtd_paginas=3):
        self.search_term = search_term
        self.output_csv = output_csv
        self.qtd_paginas = qtd_paginas
        self.driver = self._setup_driver()
        self.months = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]

    def _setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Executa sem abrir a janela do navegador
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        return driver

    def _get_date(self, date_str):
        if "horas" in date_str:
            return datetime.datetime.now()
        elif "dia" in date_str:
            return datetime.datetime.now() - datetime.timedelta(days=1)
        elif "semana" in date_str:
            return datetime.datetime.now() - datetime.timedelta(weeks=1)
        elif "mês" in date_str:
            return datetime.datetime.now() - datetime.timedelta(days=28)
        else:
            parts = date_str.split(" ")
            formatted_date = f"{parts[0]}/{self.months.index(parts[2].replace('.', '')) + 1}/{parts[4]}"
            return datetime.datetime.strptime(formatted_date, '%d/%m/%Y')

    def fetch_news(self):
        url = f"https://www.google.com/search?q={self.search_term}&tbm=nws"
        self.driver.get(url)
        time.sleep(3)

        with open(self.output_csv, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';', quoting=csv.QUOTE_MINIMAL)
            if file.tell() == 0:
                writer.writerow(['Title', 'Link', 'Date', 'Sentiment'])

            for i in range(self.qtd_paginas):
                articles = self.driver.find_elements(By.CLASS_NAME, "SoaBEf")
                for article in articles:
                    try:
                        title_brute = article.find_element(By.CLASS_NAME, "n0jPhd").text
                        title = title_brute.replace(';', ",")
                        link = article.find_element(By.CLASS_NAME, "WlydOe").get_attribute("href")
                        date_text = article.find_element(By.CLASS_NAME, "OSrXXb").text
                        article_date = self._get_date(date_text)

                        writer.writerow([title, link, article_date])
                        #print(f"{title[:10]} - {article_date} - ")

                    except Exception as e:
                        print(f"Erro ao processar artigo: {e}")

                try:
                    next_button = self.driver.find_element(By.XPATH, "//a[@id='pnnext']")
                    next_button.click()
                    time.sleep(2)
                except Exception as e:
                    print(f"Erro ao clicar no botão de 'Mais Resultados': {e}")
                    break

    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    search_term = "bbas3"
    output_csv = '/home/vitor/Documentos/Wordspace/Machine Learning/mercado_/noticias.csv'
    
    scraper = NewsScraper(search_term, output_csv, qtd_paginas=10)
    scraper.fetch_news()
    scraper.close()
