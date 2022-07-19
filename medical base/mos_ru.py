import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs




tld = 'https://www.mos.ru/'  # TDL - top level domain
sld = 'clinics/'  # SLD - second level domain

medical_type = None
page = 1
per = None
page_all = 0


params = {
    'page': f'{page}',
}


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/92.0.4515.107 Safari/537.36'}

response = requests.get(tld + sld, params=params, headers=headers)

pprint(response)