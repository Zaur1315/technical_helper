import re
from bs4 import BeautifulSoup
from selenium import webdriver
import aiohttp
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


#OPTIMAL ELECTRONICS
async def optimal(item):
    callback = []
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    url = f'https://www.elitoptimal.az/search/?search={item}'
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            soup = BeautifulSoup(await response.text(), 'lxml')
            articles_cards = soup.find_all('div', class_='box-view')
            for i in articles_cards:
                item = i.find('p', class_='price')
                if item.find('span', class_='price-new'):
                    item_cost = item.find('span', class_='price-new').text

                elif item.text:
                    item_cost = item.text.split()[0]
                else:
                    continue

                name = i.find('div', class_='name').find('a')
                callback.append([name.text, name.get('href'), item_cost])

    return callback


#Baku electronics
async def baku_electronics(item):
    callback = []
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    url = f'https://www.bakuelectronics.az/search.html?query={item}'
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as resp:
            soup = BeautifulSoup(await resp.text(), 'lxml')
            articles_cards = soup.find_all('div',class_='product__card')
            for article_card in articles_cards:
                item_name = article_card.find('a', class_='product__title').text
                item_link = article_card.find('a', class_='product__title').get('href')
                price = float(article_card.find('div', class_='product__price--cur').text)
                if article_card.find('span', class_='product__price--discount-price'):
                    discount = float(article_card.find('span', class_='product__price--discount-price').text)
                    item_price = round((price - discount), 2)
                else:
                    item_price = price
                callback.append([item_name, item_link, item_price])

    return callback

#Kontakt Home
async def kontakt(item):
    callback = []
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    url = f'https://kontakt.az/?s={item}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            soup = BeautifulSoup(await resp.text(), 'html.parser')

    articles_cards = soup.find_all('p',class_='gridprice_cash')
    for i in articles_cards:
        item = i.find('span', class_='nprice').text
        item = re.sub('[^0-9\.]+', '', item)
        item = float(item)
        if i.find_parent().find_parent().find_parent().find('div', class_='name').find('b'):
            b = i.find_parent().find_parent().find_parent().find('div', class_='name').find('b').text
            new_b = float(b.replace('M', '').replace('-', '').strip())
            final_price = round((item - new_b),2)
        else:
            final_price = item
        parents = i.find_parent().find_parent().find_parent().find('div', class_='name').find('a')
        clean = ''.join(parents.text.split('\n'))
        callback.append([clean, parents.get('href'), final_price])

    return callback

#IRSHAD ELECTRONICS

async def irshad(item):
    callback = []
    url = f'https://irshad.az/search?q={item}'
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    try:
        # Ждем, пока появится хотя бы один элемент с результатом поиска
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "sgm-product")))
    except:
        print("Ошибка: результаты поиска не найдены или страница не загрузилась")
        driver.quit()
        return callback

    # Получаем содержимое страницы
    html = driver.page_source

    # Закрываем драйвер
    driver.quit()

    soup = BeautifulSoup(html, 'lxml')

    articles = soup.find_all('div', class_='sgm-product')
    for article in articles:
        article_name = article.find('a', class_='seg-name').text
        article_link = article.find('a', class_='seg-name').get('href')
        article_price_list = article.find('div', class_='product__price__current')
        if article_price_list.find('p', class_='new-price'):
            article_price = article_price_list.find('p', class_='new-price').text
            callback.append([article_name, article_link, article_price])
        elif article_price_list.find('span', class_='old-price'):
            article_price = article_price_list.find('span', class_='old-price').text
            callback.append([article_name, article_link, article_price])
        else:
            continue

    return callback

#MAXI
def maxi(item):
    callback = []
    url = f'https://maxi.az/search/q-{item}'
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    html = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html, 'lxml')
    articles_cards = soup.find_all('article', class_='product-card')
    for article in articles_cards:
        article_name = article.find('a', class_='product-card__name').text
        article_link = ('https://maxi.az' + article.find('a', class_='product-card__name').get('href'))
        article_price = article.find('span', class_='price-manat').text + 'AZN'

        callback.append([article_name, article_link, article_price])

    return callback


