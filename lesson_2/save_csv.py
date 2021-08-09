import csv
import json


def go(name_json):
    # Достаю из JSON
    date_ls = []
    employer_ls = []
    name_ls = []
    url_ls = []
    salary_min_ls = []
    salary_max_ls = []
    salary_currency_ls = []

    with open(f'{name_json}.json', 'r', encoding='utf-8') as f:
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

    with open(f"{name_json}.csv", mode="w") as w_file:
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
