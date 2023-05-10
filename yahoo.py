
import json
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep

# Configuração do driver do Chrome
options = Options()
options.headless = False
service = Service(ChromeDriverManager().install())

# Classe Yahoo
class Yahoo:
    def __init__(self, driver, region):
        self.driver = driver
        self.region = region
        self.url = 'https://finance.yahoo.com/screener/new'
        self.input_region = '//*[@data-test="label-filter-list"]//button'
        self.label_filter_dropdown = '//*[@data-test="dropdown"]'
        self.label_filter_region = '//*[contains(text(), "Brazil")]'.format(
        # self.label_filter_region = '//*[contains(text(), "Brazil")]'.format(
            self.region)
        self.button_find_stock = '//button[@data-test="find-stock"]'
        self.button_close = '//button[@title="Close"]'

    #  função que remove a região que vem setada por padrão - opção: 1
    def remove_info_region(self):
        remove_info_region = self.driver.find_element(
            By.XPATH, self.input_region)
        remove_info_region.click()
    
    # opção 3 - função que fecha o dropdown do region 
    def click_button_region(self):
        click_button_region = self.driver.find_element(
            By.XPATH, self.label_filter_region)
        click_button_region.click()
        button_close = self.driver.find_element(By.XPATH, self.button_close)
        if button_close:
            button_close.click()
        else:
            print('Obotão de fechar não foi encontrado na pagina.')

    # opção: 2 - função que clica para adicionar região
    def click_button_dropdown(self):
        click_button_dropdown = self.driver.find_element(
            By.XPATH, self.label_filter_dropdown)
        click_button_dropdown.click()

    #  opção 4 - função que clica no botão find stocks
    def click_button_stock(self):
        click_button_stock = self.driver.find_element(
            By.XPATH, self.button_find_stock)
        sleep(3)
        click_button_stock.click()

    # pega html da pagina - opção 5
    def get_html_from_table(self):
        self.html = self.driver.page_source

    # Extrai as informações da tabela
    def extract_table_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        table = soup.find('table')
        data = []
        for tr in table.find_all('tr')[1:52]:
            tds = tr.find_all('td')
            name = tds[0].text.strip()
            symbol = tds[1].text.strip()
            price = tds[2].text.strip()
            data.append({'name': name, 'symbol': symbol, 'price': price})
        return data

    # Salva os dados em um arquivo CSV
    def csv_from_data(self, data):
        df = pd.DataFrame(data)
        df.to_csv('yahoo_finance.csv', index=False)

    # Salva os dados em um arquivo JSON
    def json_from_data(self, data):
        with open('yahoo_finance.json', 'w') as f:
            json.dump(data, f, indent=4)

    # function navigate chrome
    def navigate(self):
        self.driver.get(self.url)

# instancia do chrome driver
gc = webdriver.Chrome(service=service, options=options)
y = Yahoo(gc, region='Brazil')

# ordem de exec
y.navigate()
y.remove_info_region()
y.click_button_dropdown()
y.click_button_region()
y.click_button_stock()
sleep(10)
y.get_html_from_table()
resultado = y.extract_table_data()
y.csv_from_data(resultado)
y.json_from_data(resultado)
