import requests
from bs4 import BeautifulSoup
import json
from sorter import sort_json


def spider(pages):
    page = 1
    rates = []
    data = {}

    while page <= pages:
        url = 'https://www.jumia.com.tn/catalog/?q=led+rgb&page=' + str(page)
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, features="html.parser")
        links = []
        for link in soup.findAll('a', {'class': 'core'}):

            if not link.get('href'):
                continue
            href = 'https://www.jumia.com.tn' + link.get('href')
            links.append(href)

        names = []
        for link in soup.findAll('h3', {'class': 'name'}):
            text = link.string
            names.append(text)

        prices = []
        for link in soup.findAll('div', {'class': 'prc'}):
            text = link.string
            prices.append(text)
        for name, price, link in zip(names, prices, links):
            name_raw = ''
            for i in name:
                if not i.isspace():
                    name_raw += i.casefold()

            if 'm-avec' in name_raw:
                price_float = float(price[:-4])
                if price_float > 80:
                    continue
                meters = int(name_raw[name_raw.find('-') + 1:name_raw.find('m-')])
                rate = round(price_float / meters, 2)
                with open('results.txt', 'a') as f:
                    f.writelines(f'\n{name}\nPrice: {price}\nMeters: {meters}m\n{rate} tnd/m\n{link}\n')
                rates.append(rate)
                data[name] = {'price': price_float, 'meters': meters, 'rate': rate, 'link': link}
        page += 1

    with open('results_low_price.json', 'w') as jf:
        json.dump(data, jf, indent=3)


spider(3)

fi = 'results_low_price.json'
fo = 'results_low_price_sorted.json'
sort_json(fi, fo)
