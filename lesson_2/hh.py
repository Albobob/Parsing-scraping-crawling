import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import re
import json
import csv

search_input = input('Введите профессию, должность, вакансию...')

url = f'https://hh.ru'
link = '/search/vacancy'

page = 0
page_all = 0
items_on_page = 20

params = {
    'clusters': 'true',
    'area': '1',
    'ored_clusters': 'true',
    'enable_snippets': 'true',
    'st': 'searchVacancy',
    'text': f'{search_input}',
    'items_on_page': f'{items_on_page}',
    'page': f'{page}'

}

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                  ' (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}

response = requests.get(url + link, params=params, headers=headers)
soup = bs(response.text, 'html.parser')

# Узнаю кол - во вакансий
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
    print(f'{ammout_vac} вакансии "{search_input}"')
except ValueError:
    print('Вакансия не найдена...')

page_all = ammout_vac % items_on_page

if page_all > 0:
    page_all = ammout_vac // items_on_page + 1

print(f'Всего страниц {page_all} (по {items_on_page} вакансий на странице)')


# ***/\/\/\***\\\***/\/\/\***\\\***/\/\/\***\\\***/\/\/\***\\\***/\/\/\***\\\***/\/\/\***\\\***/\/\/\***\\\***/\/\/\***\


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


info = []

while page < page_all:

    response = requests.get(url + link, params=params, headers=headers)  # Запрос
    soup = bs(response.text, 'html.parser')
    vacancy_list = soup.find_all("div", attrs={'class': 'vacancy-serp-item'})

    for vacancy in vacancy_list:
        vacancy_data = {}
        name = vacancy.find('a', {'class': 'bloko-link'}).getText()

        date = vacancy.find('span', {
            'class': 'vacancy-serp-item__publication-date vacancy-serp-item__publication-date_short'}).getText()

        url_vacancy = vacancy.find('a', {'class': 'bloko-link'}).get('href')
        employer = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'}).getText()

        try:
            salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).getText()
        except AttributeError:
            salary = None

        vacancy_data['date'] = date
        vacancy_data['name'] = name
        vacancy_data['url'] = url_vacancy
        vacancy_data['employer'] = employer

        if salary != None:
            vacancy_data['salary_min'] = f'{min_max_salary(salary)[0]}'
            vacancy_data['salary_max'] = f'{min_max_salary(salary)[1]}'
            vacancy_data['salary_currency'] = f'{currency(salary)}'
        else:
            vacancy_data['salary_min'] = None
            vacancy_data['salary_max'] = None
            vacancy_data['salary_currency'] = None

        info.append(vacancy_data)
    pprint(f'{str(page)}/{page_all} ЖДИТЕ... ')

    page += 1

pprint(info)

with open(f'{search_input}.json', 'w', encoding='utf-8') as f:
    json.dump(info, f, ensure_ascii=False, indent=4)

date_ls = []
employer_ls = []
name_ls = []
url_ls = []
salary_min_ls = []
salary_max_ls = []
salary_currency_ls = []

with open(f'{search_input}.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


    def get_info(key, ls):
        for i in data:
            ls.append(i[f'{key}'])


    get_info('date', date_ls)
    get_info('name', name_ls)
    get_info('employer', employer_ls)
    get_info('url', url_ls)
    get_info('salary_min', salary_min_ls)
    get_info('salary_max', salary_max_ls)
    get_info('salary_currency', salary_currency_ls)

with open(f"{search_input}.csv", mode="w") as w_file:
    file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
    file_writer.writerow(
        ["Дата",
         "Название вакансии",
         "Работадатель",
         "Минимальная зп",
         "Максимальная зп",
         "Валюта",
         "url"])
    for i in range(len(name_ls)):
        file_writer.writerow(
            [f"{date_ls[i]}",
             f"{name_ls[i]}",
             f"{employer_ls[i]}",
             f"{salary_min_ls[i]}",
             f"{salary_max_ls[i]}",
             f"{salary_currency_ls[i]}",
             f"{url_ls[i]}"])
