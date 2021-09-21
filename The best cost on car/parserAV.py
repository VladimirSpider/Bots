import requests
from bs4 import BeautifulSoup as BS
import re
import math
nc = "1"
nm = "1"
np = "1"
URL = "https://cars.av.by/filter?brands[0][brand]=" + nc + "&brands[0][model]=" + nm + "&page=" + np
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 OPR/77.0.4054.277', 'accept': '*/*'}
HOST = 'https://cars.av.by'

def get_html(url, params=None):
    r = requests.get(url, headers = HEADERS, params = params)
    return r

def number_pages(nc, nm):
    np = "1"
    URL = "https://cars.av.by/filter?brands[0][brand]=" + nc + "&brands[0][model]=" + nm + "&page=" + np
    html = get_html(URL)
    html = BS(html.content, 'html.parser')
    np = html.find('div', class_ = 'paging__text').get_text(strip=True)
    np = np.replace("\u2009","")
    match = re.findall(r'\d+', np)
    np = int(match[1]) / int(match[0])
    np = math.ceil(np)
    return np

'''def parse_name_car():
    dict_cars = {}
    for i in range(1,15000):
        nc = str(i)
        URL = "https://cars.av.by/filter?brands[0][brand]=" + nc + "&brands[0][model]=" + nm + "&page=" + np
        html = get_html(URL)
        print(URL)
        if html.status_code == 404:
            print("NO")
        else:
            html = BS(html.content, 'html.parser')
            name_car = html.find('div', class_='filter-models__row')\
                           .find('span', class_ = "dropdown-floatlabel__value").text
            dict_cars[name_car] = nc
    print(dict_cars)
    return dict_cars'''


def parse(nc, nm):
    all_cars = {}
    j = 0
    print(nc)
    np = number_pages(nc, nm)
    print("Pages number:", np)
    for i in range(1, int(np)+1):
        print("Number page:", i)
        URL = "https://cars.av.by/filter?brands[0][brand]=" + nc + "&brands[0][model]=" + nm + "&page=" + str(i)
        html = get_html(URL)
        if html.status_code == 200:
            html = BS(html.content, 'html.parser')
            for el in html.find_all('div', class_='listing-item'):
                try:
                    title = el.find('div', class_='listing-item__about') \
                        .find('h3', class_='listing-item__title') \
                        .find('a', class_='listing-item__link') \
                        .find('span', class_='link-text').get_text(strip=True)
                except:
                    title = "Error"
                try:
                    city = el.find('div', class_='listing-item__about') \
                        .find('div', class_='listing-item__info') \
                        .find('div', class_='listing-item__location').get_text(strip=True)
                except:
                    city = "Error"
                try:
                    year = el.find('div', class_='listing-item__params') \
                        .find('div').get_text(strip=True)
                    year = year.replace("\xa0", " ")
                    year = year.replace("г.", "")
                    year = year.replace(" ", "")
                except:
                    year = "Error"
                try:
                    description = el.find('div', class_='listing-item__params') \
                        .find('div') \
                        .find_next_siblings('div')[0].get_text(strip=True)
                    description = description.replace("\xa0", " ")
                except:
                    description = "Error"
                try:
                    cost = el.find('div', class_='listing-item__prices') \
                        .find('div') \
                        .find_next_siblings('div')[0].get_text(strip=True)
                    cost = cost.replace("\xa0", "")
                    cost = cost.replace("\u2009", "")
                    cost = cost.replace("≈", "")
                    cost = cost.replace("$", "")
                except:
                    cost = "Error"
                try:
                    link = el.find('div', class_='listing-item__about') \
                        .find('h3', class_='listing-item__title') \
                        .find('a', class_='listing-item__link').get('href')
                except:
                    link = "Error"
                if True:
                    j += 1
                    element = "№"+ str(j)
                    information_about_car = {
                        "country": "Belarus",
                        "city": city,
                        "title": title,
                        "description": description,
                        "year": year,
                        "cost": cost,
                        "link": HOST + link
                    }
                    all_cars[element] = information_about_car
                    print("№", j)
                    print(title)
                    print(year)
                    print(description)
                    print(cost)
                    print(city)
                    print(HOST + link)
                else:
                    print("Error")

        else:
            print('Error')
    return all_cars

