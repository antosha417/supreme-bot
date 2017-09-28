# -*- coding: utf-8 -*-

from order_data import *
from re import findall, split, search
from urllib import quote
from bs4 import BeautifulSoup
from requests import Session
from requests.adapters import HTTPAdapter


# with open('new_drop_indicator', 'r') as f:
#    old_drop_data = f.read()

s = Session()
s.mount('http://www.supremenewyork.com/', HTTPAdapter(max_retries=200))

# while True:
#    html_doc = s.get('http://www.supremenewyork.com/shop/new', timeout=2).text
#    soup = BeautifulSoup(html_doc, 'html.parser')
#    if soup.find_all('a').pop(20).get('href') != old_drop_data:
#        break

html_doc = s.get('http://www.supremenewyork.com/shop/all', timeout=2).text
soup = BeautifulSoup(html_doc, 'html.parser')

stop = name_is_good = False

search_r = None
cl_name = None

for link in soup.find_all('a'):
    if stop:
        break
    href = link.get('href')
    sp_link = split('/', href)
    if len(sp_link) == 5:
        if cl_name != sp_link[3] or name_is_good:
            cl_name = sp_link[3]
            basic_url = 'http://www.supremenewyork.com' + href
            search_r = s.get(basic_url, timeout=2)
            if search(clothes_name, search_r.text[:200]) is not None:
                name_is_good = True
                for color in clothes_colors:
                    if search(color, search_r.text[:200]) is not None:
                        stop = True
                        break
if not stop:
    print 'could not find item'
    exit(-1)

data_r = search_r

url = 'http://www.supremenewyork.com' + findall('action="(/shop/[\d]+/add)', data_r.text)[0]

size = None
for _size, size_name in findall('<option value="([\d]+)">(.+)</option>', data_r.text):
    if search(order_size, size_name) is not None:
        size = _size

if size is None:
    print 'could not find size'
    exit(-1)

style = int(findall('id="style" value="([\d]+)"', data_r.text)[0])
token = findall('name="csrf-token" content="(.*==)" />', data_r.text)[0]
price = findall('<span itemprop="price">.*?([\d]+)</span>', data_r.text)[0]

headers = {
    'Accept': '*/*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.8,ru;q=0.6',
    'Connection': 'keep-alive',
    'Content-Length': '58',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'www.supremenewyork.com',
    'Origin': 'http://www.supremenewyork.com',
    'Referer': 'http://www.supremenewyork.com/shop/jackets/pegroxdya',
    'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'X-CSRF-Token': token,
    'X-Requested-With': 'XMLHttpRequest'}

data = {'style': style,
        'size': size,
        'commit': 'add to basket'}

cart_r = s.post(url=url, data=data, headers=headers, timeout=2)

for item in split('[;,]', cart_r.headers['Set-Cookie']):
    if item[:9] == ' _supreme':
        sess = item
        break

for item in split('[;,]', cart_r.headers['Set-Cookie']):
    if item[:5] == ' cart':
        cart = item
        break

res = '{"' + str(size) + '":1,"cookie":"1 item--' + str(size) + ',' + str(style) + '","total":"' + '€' + str(
    price) + '"}'
pure_cart = quote(res, safe='')

url = 'https://www.supremenewyork.com/checkout'
headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, sdch, br',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive',
           'Cookie': cart[1:] + ';pure_cart=' + pure_cart + ';' + sess,
           'Host': 'www.supremenewyork.com',
           'If-None-Match': 'W/"352bf760094370aafbe0c45001be02d6"',  # ???
           'Referer': basic_url,
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87'
           }
auth_r = s.post(url=url, headers=headers, timeout=2)

authenticity_token = findall('<meta name="csrf-token" content="(.*==)" />', auth_r.text)[0]

for item in split('[;,]', auth_r.headers['Set-Cookie']):
    if item[:9] == ' _supreme':
        sess = item
        break

url = 'https://www.supremenewyork.com/checkout'

data = {'authenticity_token': authenticity_token,
        'order[billing_name]': billing_name,
        'order[email]': email,
        'order[tel]': tel,
        'order[billing_address]': billing_address,
        'order[billing_address_2]': '',
        'order[billing_address_3]': '',
        'order[billing_city]': billing_city,
        'order[billing_zip]': billing_zip,
        'order[billing_country]': billing_country,
        'same_as_billing_address': '1',
        'store_credit_id': '',
        'credit_card[type]': credit_card_type,
        'credit_card[cnb]': credit_card_cnb,
        'credit_card[month]': credit_card_month,
        'credit_card[year]': credit_card_year,
        'credit_card[vval]': credit_card_vval,
        'order[terms]': '1',
        'hpcvv': ''}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.8,ru;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # 'Content-Length':'635'
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': cart[1:] + ';pure_cart=' + pure_cart + ';' + sess,
    'Host': 'www.supremenewyork.com',
    'Origin': 'https://www.supremenewyork.com',
    'Referer': 'https://www.supremenewyork.com/checkout',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

final_r = s.post(url=url, headers=headers, data=data, timeout=4)
