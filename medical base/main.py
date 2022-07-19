import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs

tld = 'https://mosgorzdrav.ru'  # TDL - top level domain
sld = '/ru-RU/citizens/medical.html'  # SLD - second level domain

medical_type = 1
page = 1
per = 10
page_all = 0

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/92.0.4515.107 Safari/537.36'}


def html():
    # Параметры страницы
    params = {
        'medical_type': f'{medical_type}',
        'p': f'{page}',
        'per': f'{per}',
    }
    # Запрос + получение HTML
    response = requests.get(tld + sld, params=params, headers=headers)
    soup = bs(response.text, 'html.parser')
    return soup


def item(sp, class_html):
    ls = []
    soup = sp
    # Вытаскиеваем элемент
    item = soup.findAll("div", attrs={'class': f'{class_html}'})
    # Убираем пробелы в конце и началле строчки
    # l = list(map(lambda x: x.strip(), ls))
    return item


data = []

while page <= 2:
    sp = html()
    medical_main = item(sp, 'medical-main')
    for itm in medical_main:
        bd = {}

        name = itm.find("div", attrs={'class': f'med-title'}).getText()
        name_string = name.strip()
        bd['name'] = f'{name_string}'

        try:
            mail = itm.find("div", attrs={'class': f'med-email'})
            m = mail.text
            bd['mail'] = f'{m.strip()}'
        except AttributeError:
            mail = None
            bd['mail'] = f'{mail}'

        try:
            url = itm.find("div", attrs={'class': f'med-site'})
            url_1 = url.find("p")
            url_2 = url.find("a").get('href')
            bd['url'] = url_2
        except AttributeError:
            bd['url'] = None


        data.append(bd)

    page += 1

pprint(data)