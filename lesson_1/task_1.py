import requests
import json


def get_data(lnik):
    useragent = {
        'UserAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                     'AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/91.0.4472.164 Safari/537.36'
    }



    response = requests.get(lnik, headers=useragent)




    return response.json()


username = input('Username...   ')
url = 'https://api.github.com'
lnik = f'{url}/users/{username}/repos'

data = (get_data(lnik))

with open(f'{username}.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print('########################################\n')
print(f'Репозитории " {username} "\n{lnik}\n')
print('########################################\n')



for i in data:
    print(i['name'])


