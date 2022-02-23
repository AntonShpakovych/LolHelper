import requests
from pprint import pprint
URL = 'http://ddragon.leagueoflegends.com/cdn/12.3.1/data/en_US/profileicon.json'


data = requests.get(URL).json()
pprint(data)