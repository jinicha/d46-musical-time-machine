import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.billboard.com/charts/hot-100/"

date = input('Which year do you want to travel to? (in format YYYY-MM-DD): ')
response = requests.get(f'{BASE_URL}{date}/')
soup = BeautifulSoup(response.text, "html.parser")
titles = soup.select("ul li h3")[:100]
print(titles)
