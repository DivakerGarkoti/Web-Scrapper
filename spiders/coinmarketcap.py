import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from pymongo import MongoClient
import pandas as pd
import time
import csv

client = MongoClient("mongodb+srv://garkotid000:<db_password>@projects.f6mcr.mongodb.net/")
db = client.cryptocurrency

def insertToDB(rank, name, symbol, market_cap, price, circulating_supply, volume, percent_1h, percent_24h, percent_7d):
    collection = db.coinmarketcap
    post = {
        'Rank': rank,
        'Name': name,
        'Symbol': symbol,
        'Market Cap': market_cap,
        'Price': price,
        'Circulating Supply': circulating_supply,
        'Volume': volume,
        '% 1h': percent_1h,
        '% 24h': percent_24h,
        '% 7d': percent_7d
    }
    inserted = collection.insert_one(post).inserted_id
    print(f"Inserted document with ID: {inserted}")  # Debug statement
    return inserted

class CoinMarketCapSpider(scrapy.Spider):
    name = 'coinmarketcap'
    
    CHROME_DRIVER_PATH = 'H:\chromedriver-win64\chromedriver.exe'  # Ensure the path is correct
    
    start_urls = ['https://coinmarketcap.com/all/views/all/']

    def __init__(self):
        print("Initializing the Chrome driver...")  # Debug statement
        service = Service(self.CHROME_DRIVER_PATH)
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(service=service, options=options)
        self.data_file = 'coinmarketcap_data.csv'
        self.scroll_pause_time = 0.2  
        self.scroll_increment = 4000  
        self.scraped_set = set()  

        with open(self.data_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Rank', 'Name', 'Symbol', 'Market Cap', 'Price', 'Circulating Supply', 'Volume', '% 1h', '% 24h', '% 7d'])
        print("CSV file initialized.")

    def parse(self, response):
        print("Starting to parse the webpage...")
        self.driver.get(response.url)

        last_height = self.driver.execute_script("return document.body.scrollHeight")
        print(f"Initial page height: {last_height}")
        
        while True:
            print("Looking for table rows...")
            rows = self.driver.find_elements(By.XPATH, '//table/tbody/tr')
            print(f'Number of rows found: {len(rows)}')
            
            new_data = []
            for row in rows:
                try:
                    rank = row.find_element(By.XPATH, './td[1]/div').text
                    name = row.find_element(By.XPATH, './td[2]/div/a[2]').text
                    symbol = row.find_element(By.XPATH, './td[3]/div').text
                    market_cap = row.find_element(By.XPATH, './td[4]/p/span[2]').text
                    price = row.find_element(By.XPATH, './td[5]/div/span').text
                    circulating_supply = row.find_element(By.XPATH, './td[6]/div').text
                    volume = row.find_element(By.XPATH, './td[7]/a').text
                    percent_1h = row.find_element(By.XPATH, './td[8]/div').text
                    percent_24h = row.find_element(By.XPATH, './td[9]/div').text
                    percent_7d = row.find_element(By.XPATH, './td[10]/div').text

                    row_id = (rank, name, symbol, market_cap, price, circulating_supply, volume, percent_1h, percent_24h, percent_7d)
                    
                    if row_id not in self.scraped_set:
                        self.scraped_set.add(row_id)
                        new_data.append({
                            'Rank': rank,
                            'Name': name,
                            'Symbol': symbol,
                            'Market Cap': market_cap,
                            'Price': price,
                            'Circulating Supply': circulating_supply,
                            'Volume': volume,
                            '% 1h': percent_1h,
                            '% 24h': percent_24h,
                            '% 7d': percent_7d
                        })
                        print(f"Scraped data for {name} ({symbol})")  
                    insertToDB(rank, name, symbol, market_cap, price, circulating_supply, volume, percent_1h, percent_24h, percent_7d)
                except Exception as e:
                    print(f'Error scraping row: {e}')
            
            if new_data:
                df = pd.DataFrame(new_data)
                df.to_csv(self.data_file, mode='a', header=False, index=False)
                print(f'Data written to CSV: {len(new_data)} records')
            else:
                print('No new data to write.')           
            self.driver.execute_script(f"window.scrollBy(0, {self.scroll_increment});")
            time.sleep(self.scroll_pause_time)
            
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            print(f"New page height: {new_height}")  
            if new_height == last_height:
                print('No more data to load, exiting...')  
                break
            last_height = new_height
        
        self.driver.quit()
        print('Scraping completed.')  