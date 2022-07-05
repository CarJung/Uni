import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


def clean(raw_html):
   """clean numbers froim html 

   Args:
       raw_html (beautiful suoup object): _description_

   Returns:
       int: scrapped number
   """
   cleanr = re.compile('<.*?>')
   cleantext  = re.sub(cleanr, '', str(raw_html))
   cleantext= re.sub("[^0-9]", "", cleantext)
   return cleantext 

def cleaned_addreses(string):
    """_summary_

    Args:
        string (_type_): _description_

    Returns:
        _type_: _description_
    """
    a = str(string)
    return a.replace('<span class="css-17o293g es62z2j9">', '').replace('</span>', '')


def cleaned_space(string):
    """_summary_

    Args:
        string (_type_): _description_

    Returns:
        _type_: _description_
    """
    s = str(string)
    return (s[34:40].replace('m','').replace('<',"").replace('²','').replace(' ','')) 


def scrap_data():
   """scrap data

   Returns:
       pandas_data_frame: four colums
   """
   addreses=[] #List of flats adresses
   out_prices=[] #List house prices
   out_space=[] #List of house space
   out_rooms=[] #List of number of rooms in flat

   page_url = "https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/warszawa?page="

   for number in range(593):
        page = requests.get(page_url +str(number))
        content = page.content
        soup = BeautifulSoup(content, features='html.parser')

        spans = soup.find_all("span", class_="css-rmqm02 eclomwz0")
        addres = soup.find_all("span", class_="css-17o293g es62z2j9")
        price = spans[::4]
        rooms = spans[2::4]
        space = spans[3::4]

        clean_price = [clean(p) for p in price]
        clean_rooms = [clean(r) for r in rooms]
        clean_space = [cleaned_space(s) for s in space]
        clean_addres = [cleaned_addreses(a) for a in addres]

        addreses += clean_addres
        out_prices += clean_price
        out_space += clean_space
        out_rooms += clean_rooms

   df = pd.DataFrame({'Address': addreses, 'Price': out_prices, 'Space': out_space, 'Rooms': out_rooms})
   return df.to_csv('listings.csv', index=False, encoding='utf-8')


data = scrap_data()

def inner_page_data_scrap(soup):
    """scraps detail from inner html page of an offert

    Args:
        soup (bs4.BeautifulSoup): current html page of offerts list

    Returns:
       market, year, elevator, balcony, level, parking_place (list): _description_
    """

    inner_page_url = "https://www.otodom.pl"
    market = []
    year = []
    elevator = []
    balcony = []
    level = []
    parking_place = []

    for a in soup.find_all('a', href=True)[2:41]:
        pages_url = inner_page_url + a['href']

    for url in pages_url:
        page = requests.get(url)
        content = page.content
        soup = BeautifulSoup(content, features='html.parser')

        market = soup.find_all("div", class_="css-1wi2w6s estckra5")
        year = soup.find_all("div", class_="css-1wi2w6s estckra5")
        elevator = soup.find_all("div", class_="css-1wi2w6s estckra5")
        balcony = soup.find_all("div", class_="css-1wi2w6s estckra5")
        level = soup.find_all("div", class_="css-1wi2w6s estckra5")
        parking_place = soup.find_all("div", class_="css-e72ul8 ekf916v1")


    return market, year, elevator, balcony, level, parking_place
