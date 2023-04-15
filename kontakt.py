import requests
from bs4 import BeautifulSoup


def get_item():

    item = input('Enter here:')

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }

    url = f'https://kontakt.az/?s={item}'

    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')

    articles_cards = soup.find_all('p',class_='gridprice_cash')
    for i in articles_cards:
        item = i.find('span', class_='nprice').text
        print(item)
        parents = i.find_parent().find_parent().find_parent().find('div', class_='name').find('a')
        clean = ''.join(parents.text.split('\n'))
        print(clean)
        print(parents.get('href'))
        print('\n')



get_item()