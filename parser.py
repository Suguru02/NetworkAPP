import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def parse(max_pages: int = 3):
    
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless=new")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(executable_path="/usr/bin/chromedriver")

    driver = webdriver.Chrome(
        service=service,
        options=options
    )

    all_articles = []
    base_url = "https://habr.com/ru/articles/"
    
    for page in range(1, max_pages + 1):
        page_url = f"{base_url}page{page}/"
        driver.get(page_url)
        
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'article.tm-articles-list__item'))
        )
        
        time.sleep(1.5)
        
        cards = driver.find_elements(By.CSS_SELECTOR, 'article.tm-articles-list__item')
        
        if not cards:
            break
        
        for card in cards:
            try:
                title_el = card.find_element(By.CSS_SELECTOR, 'a.tm-title__link')
                title = title_el.text.strip()
                article_link = title_el.get_attribute('href')
                
                author = None
                try:
                    author_el = card.find_element(By.CSS_SELECTOR, 'a.tm-user-info__username')
                    author = author_el.text.strip()
                except:
                    author = "Не указан"
                
                publish_date = None
                try:
                    date_el = card.find_element(By.CSS_SELECTOR, 'time[datetime]')
                    publish_date = date_el.get_attribute('datetime')[:10]
                except:
                    pass
                
                if title:
                    all_articles.append({
                        'title': title,
                        'author': author,
                        'publish_date': publish_date,
                        'url': article_link
                    })
                    
            except Exception as e:
                continue
    
    return all_articles
