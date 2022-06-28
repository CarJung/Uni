import requests
from bs4 import BeautifulSoup
import pandas as pd

address=[] #List of flats adresses
prices=[] #List house prices
space=[] #List of house space
rooms=[] #List of number of rooms in flat
driver.get("https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/warszawa")

page_url = 'https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/warszawa'
page = requests.get(page_url)
content = page.content
soup = BeautifulSoup(content, features='html.parser')

spans = soup.find_all("span", class_="css-rmqm02 eclomwz0")



for element in soup.findAll('li', attrs={'class': 'css-1k6141t es62z2j0'}):
   prices = element.find('span', attrs={'class': 'css-rmqm02 eclomwz0'})
   space = element.find('span', attrs={'class': 'css-rmqm02 eclomwz0'})
   address = element.find('span', attrs={'class': 'css-17o293g es62z2j9'})
   rooms = element.find('span', attrs={'class': 'css-rmqm02 eclomwz0'})


df = pd.DataFrame({'Address': address, 'Price': prices, 'Space': space, 'Rooms': rooms}, index=[0])
df.to_csv('listings.csv', index=False, encoding='utf-8')
