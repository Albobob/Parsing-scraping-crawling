import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs

tld = 'https://mosgorzdrav.ru'  # TDL - top level domain
sld = '/ru-RU/citizens/medical.html'  # SLD - second level domain

medical_type = 1

page = 1
page_all = []

per = 10
metro_id = 0
district_id = 1
district_all = 12

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/92.0.4515.107 Safari/537.36'}


def html():
    # Параметры страницы
    params = {
        'medical_type': f'{medical_type}',
        'p': f'{page}',
        'per': f'{per}',
        'metro_id': f'{metro_id}',
        'district_id': f'{district_id}',
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


# Всего 12 округов
# Узнаем сколько страниц в округе
def button_pg_next():
    """
    Проверяет наличие кнопки Далее на странице
    :return:Возвращает
    1 - на странице есть кнопка next
    0 - кнопкки next нет на странице
    """
    ls = []
    ls.clear()

    # district_id = ds_id

    sp = html()
    page_box = item(sp, 'pages')
    for itm in page_box:
        page_list = itm.find("ul", attrs={'class': f'pag-list'})
        try:
            next = page_list.find(attrs={'class': f'pag pag-next'})
            ls.append(next)
        except AttributeError:
            ls.clear()
    return len(ls)

# def next_page (next_btn):
#
#     page = 1
#     while next_btn == 1:
#
#         page += 1
#
#     return page
# while district_id <= district_all:
#     print(button_pg_next())
#
#     district_id += 1

data = []

while page <= 5:
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
            bd['url'] = url_2.strip()
        except AttributeError:
            bd['url'] = None

        try:
            phone = itm.find("div", attrs={'class': f'med-phone'}).getText()
            bd['phone'] = phone.strip()
        except AttributeError:
            bd['phone'] = None



        data.append(bd)

    page += 1

for i in data:
    name = i['name']
    mail = i['mail']
    url = i['url']
    phone = i['phone']
    print(f'{name};{mail};{phone};{url}')
