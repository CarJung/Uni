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

def cleaned_elevator(string):
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
    addreses = [] #List of flats adresses
    out_prices = [] #List house prices
    out_space = [] #List of house space
    out_rooms = [] #List of number of rooms in flat
    out_market = []
    out_year = []
    out_elevator = []
    out_balcony = []
    out_level = []
    out_parking_place = []

    page_url = "https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/warszawa?page="

    for number in range(200,300):
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

        market, year, elevator, balcony, level, parking_place = inner_page_data_scrap(soup)

        addreses += clean_addres
        out_prices += clean_price
        out_space += clean_space
        out_rooms += clean_rooms
        out_market += market
        out_year += year
        out_elevator += elevator
        out_balcony += balcony
        out_level += level
        out_parking_place += parking_place

        print(number)
    df = pd.DataFrame({
        'Address': addreses, 'Price': out_prices, 'Space': out_space, 'Rooms': out_rooms, 'Market': out_market, 'Year': out_year, 'Evelevator': out_elevator, 'Balcony': out_balcony, 'Level': out_level, 'Parking place': out_parking_place
        })
    return df.to_csv('listings_3.csv', index=False, encoding='utf-8')

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
    pages_url = []

    for a in soup.find_all('a', href=True)[3:42]:
        pages_url.append(inner_page_url + a['href'])

    for u in pages_url:
        if len(u) < 5:
            pass 
        else:
            page = requests.get(u)
            content = page.content
            soup = BeautifulSoup(content, features='html.parser')

            data= soup.find_all("div", class_="css-1qzszy5 estckra8")
            
        try:
            market.append(str(data[21].find_all('div',class_="css-1wi2w6s estckra5"))[35:-7])
        except IndexError:
            market.append('')
        try:
            year.append(str(data[25].find_all('div',class_="css-1wi2w6s estckra5"))[35:-7]) #clean(data[12])
        except IndexError:
            year.append('')
        try:
            elevator.append(str(data[31].find_all('div',class_="css-1wi2w6s estckra5"))[35:-7])
        except IndexError:
            elevator.append('')
        try:
            balcony.append(str(data[11].find_all('div',class_="css-1wi2w6s estckra5"))[35:-7])
        except IndexError:
            balcony.append('')
        try:
            level.append(str(data[9].find_all('div',class_="css-1wi2w6s estckra5"))[35:-7])
        except IndexError:
            level.append('')
        try:
            parking_place.append(str(data[15].find_all('div',class_="css-1wi2w6s estckra5"))[35:-7])
        except IndexError:
            parking_place.append('')

    return market, year, elevator, balcony, level, parking_place



data = scrap_data()