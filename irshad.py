import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities



def get_irshad_item():
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    import time

    url = 'https://irshad.az/search?q=honor%20x9a'

    chrome_options = Options()
    chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)


    # Обновляем страницу и ждем еще 3 секунды
    driver.refresh()
    time.sleep(3)

    # Получаем содержимое страницы
    html = driver.page_source

    # Закрываем драйвер
    driver.quit()
    # print(html)
    #
    soup = BeautifulSoup(html, 'lxml')

    articles = soup.find_all('div', class_='sgm-product')
    for article in articles:
        article_name = article.find('a', class_='seg-name').text
        article_link = article.find('a', class_='seg-name').get('href')
        article_price_list = article.find('div', class_='product__price__current')
        if article_price_list.find('span', class_='old-price'):
            article_price = article_price_list.find('span', class_='old-price').text
            print(article_name)
            print(article_link)
            print(article_price)
            print('\n')
        elif article_price_list.find('p', class_='new-price'):
            article_price = article_price_list.find('p', class_='new-price').text
            print(article_name)
            print(article_link)
            print(article_price)
            print('\n')
        else:
            continue






get_irshad_item()