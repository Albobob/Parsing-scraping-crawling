import requests
import json
from datetime import datetime
import csv

api = 'https://api.vk.com/method/'
method = 'wall.get'

token = '3c55da6c3c55da6c3c55da6c113c2d115333c553c55da6c5d53a344af10c64e3b8feaa8'
api_v = 5.131
domain = str(input('Введите короткий адрес пользователя или сообщества...   '))
count = 100

response = requests.get(f'{api}{method}',
                        params={
                            'access_token': token,
                            'v': api_v,
                            'domain': domain,
                            'count': count

                        })

data = response.json()

response = (data['response'])
items = (response['items'])


def post(itm_name):
    ls = []
    for i in range(count):
        id = (items[i][f'{itm_name}'])
        ls.append(id)

    return ls


id_post = []
likes = []
reposts = []
views = []
data_time = []
for i in post('id'):
    id_post.append(i)

for i in post('likes'):
    likes.append(i['count'])

for i in post('reposts'):
    reposts.append(i['count'])

for i in post('views'):
    views.append(i['count'])

for i in post('date'):
    data_time.append(i)

first_time = (max(data_time))
last_time = (min(data_time))

x = (datetime.fromtimestamp(int(first_time)).strftime("%Y-%m-%d %H:%M:%S.%f"))
y = (datetime.fromtimestamp(int(last_time)).strftime("%Y-%m-%d %H:%M:%S.%f"))

d1 = datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f")
d2 = datetime.strptime(y, "%Y-%m-%d %H:%M:%S.%f")

last_first_date = abs(d2 - d1)
date_string = (str(last_first_date))

x = ''
for i in date_string:

    if i != 'd':
        x += i
    else:
        break

tm = (int(x))
print(f'В сообществе (https://vk.com/{domain}) за последнии 100 постов среднее кол - во  \n'
      f'просмотров: {sum(views) // count}\n'
      f'лайков:     {sum(likes) // count}\n'
      f'репостов:   {sum(reposts) // count}\n'
      f'постов в день: {count / tm}'

      )

#
# for i in range(count):
#     print(f' В сообществе за последнии 100 постов: \n'
#           f'среднее кол - во  просмотров {sum(views) // count }'
#           f'\n id {id_post[i]}, лайки {likes[i]}, репостов {reposts[i]}, просмотров {views[i]}')

with open(f'{domain}.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

with open(f"{domain}.csv", mode="w", encoding='utf-8') as w_file:
    file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
    file_writer.writerow(["ID", "просмотров", "лайков", "репостов"])
    for i in range(count):
        file_writer.writerow([f"{id_post[i]}",f"{views[i]}", f"{likes[i]}", f"{reposts[i]}"])
