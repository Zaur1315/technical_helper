import requests
from bs4 import BeautifulSoup


def get_optimal_item():
    callback = []
    item = input('Enter here:')
    #item = 'samsung'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }

    url = f'https://www.elitoptimal.az/search/?search={item}'

    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')

    articles_cards = soup.find_all('div',class_='box-view')
    for i in articles_cards:
        item = i.find('p', class_='price')
        if item.find('span', class_='price-new'):
            item_cost = item.find('span', class_='price-new').text

        elif item.text:
            item_cost = item.text.split()[0]
        else:
            continue

        name = i.find('div', class_='name').find('a')
        print(name.text)
        print(name.get('href'))
        print(item_cost)
        print('\n')

        callback.append([name.text, ])


get_optimal_item()