import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs
import json
import re
import  save_csv


data_vacancy = []

search_text = input('')


tld = 'https://hh.ru'  # TDL - top level domain
sld = '/search/vacancy'  # SLD - second level domain

items_on_page = 20
page = 0
page_all = 0

params = {
    'clusters': 'true',
    'area': '1',
    'ored_clusters': 'true',
    'enable_snippets': 'true',
    'st': 'searchVacancy',
    'text': f'{search_text}',
    'items_on_page': f'{items_on_page}',
    'page': f'{page}'

}

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/92.0.4515.107 Safari/537.36'}

# Узнаю кол - во вакансий


response = requests.get(tld + sld, params=params, headers=headers)
soup = bs(response.text, 'html.parser')

vacancy_amount = soup.find("h1", attrs={'class': 'bloko-header-section-3'})
ammout = vacancy_amount.getText()
ammout.replace('\u202f', '')
amount_page = re.findall('\d+', ammout)
x = ''
for i in amount_page:
    x += i
ammout_vac = 0
try:
    ammout_vac = int(x)
    print(f'{ammout_vac} вакансии "{search_text}"')
except ValueError:
    print('Вакансия не найдена...')

page_all = ammout_vac % items_on_page

if page_all > 0:
    page_all = ammout_vac // items_on_page + 1


def min_max_salary(salary_string):
    # Убираем ПРОБЕЛ БЕЗ РАЗРЫВА
    txt = salary_string.replace('\u202f', '')
    # Разделяем строку по ' – '
    short_string = txt.split(' – ')

    minimum_salary = ''
    maximum_salary = ''

    for i_min in short_string[0]:
        minimum_salary += i_min

    for i_max in short_string[len(short_string) - 1]:
        maximum_salary += i_max

    min_value = re.findall('\d+', minimum_salary)
    max_value = re.findall('\d+', maximum_salary)
    min_money = None
    max_money = None
    if len(min_value) != 0:
        min_money = min_value[0]

    if len(max_value) != 0:
        max_money = max_value[0]

    return int(min_money), int(max_money)


def currency(salary_string):
    return salary_string.split()[-1]


while page < page_all:

    params_two = {
        'clusters': 'true',
        'area': '1',
        'ored_clusters': 'true',
        'enable_snippets': 'true',
        'st': 'searchVacancy',
        'text': f'{search_text}',
        'items_on_page': f'{items_on_page}',
        'page': f'{page}'

    }
    print(f'Страниц {page}/{page_all}')
    print(params_two)

    response = requests.get(tld + sld, params=params_two, headers=headers)
    soup = bs(response.text, 'html.parser')

    items = soup.find_all("div", {"class": 'vacancy-serp-item'})

    for card_vacancy in items:
        card_vacancy_info = {}

        date = card_vacancy.find("span", {
            "class": "vacancy-serp-item__publication-date vacancy-serp-item__publication-date_short"}).getText()
        name = card_vacancy.find("a", {"data-qa": "vacancy-serp__vacancy-title"}).getText()
        employer = card_vacancy.find("a", {"data-qa": "vacancy-serp__vacancy-employer"}).getText()
        employer_clear = employer.replace("&nbsp;", " ")  # !!! НЕ РАБОТАЕТ

        url = card_vacancy.find("a", {"data-qa": "vacancy-serp__vacancy-title"}).get('href')

        try:
            salary = card_vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).getText()
        except AttributeError:
            salary = None

        card_vacancy_info["date"] = date
        card_vacancy_info["name"] = name
        card_vacancy_info["employer"] = employer_clear
        card_vacancy_info["url"] = url

        if salary != None:
            card_vacancy_info['salary_min'] = f'{min_max_salary(salary)[0]}'
            card_vacancy_info['salary_max'] = f'{min_max_salary(salary)[1]}'
            card_vacancy_info['salary_currency'] = f'{currency(salary)}'
        else:
            card_vacancy_info['salary_min'] = None
            card_vacancy_info['salary_max'] = None
            card_vacancy_info['salary_currency'] = None

        data_vacancy.append(card_vacancy_info)

    page += 1

# !!! нужно сделать Проверку уникальности URL`ов !!!

# Сохранение в JSON
with open(f'{search_text}.json', 'w', encoding='utf-8') as f:
    json.dump(data_vacancy, f, ensure_ascii=False, indent=4)

# Сохранение в CSV
save_csv.go(search_text)

