import requests
from bs4 import BeautifulSoup


def get_be_item():

    item = input('Enter here:')

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }

    url = f'https://www.bakuelectronics.az/search.html?query={item}'

    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')

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

        print(item_name)
        print(item_link)
        print(item_price)
        print('\n')


get_be_item()