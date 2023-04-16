from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_maxi_item():
    # item = input('Enter here:')
    item = 'iphone 12'
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

        print(article_name)
        print(article_link)
        print(article_price)
        print('\n')


get_maxi_item()
