"""
This code scrapes from Eater's restaurant lists and adds it to a Google spreadsheet.
You can then import the sheet into a Google map!
"""

import requests
import csv
from bs4 import BeautifulSoup
from slugify import slugify


# Webscraper code
# Replace the URL with your desired URL
URL = "https://pdx.eater.com/maps/best-portland-brunches-restaurants"
page = requests.get(URL, timeout=30)


soup = BeautifulSoup(page.content, "html.parser")
page_title = soup.title.string
output_file_name =  slugify(page_title) + ".csv"

fieldnames = ['name', 'description', 'address', 'website', 'phone']
restaurants = [
    {
        'name': (''.join(tag.text for tag in restaurant.find_all('h1'))).replace(u'\xa0', ' '),
        'description': (''.join(tag.text for tag in restaurant.find_all('p'))).replace(u'\xa0', ' '),
        'address': ''.join([(tag.find("a")).text for tag in restaurant.find_all("div", class_="c-mapstack__address")]),
        'website': ''.join([tag['href'] for tag in restaurant.find_all("a", {'href': True}) if tag.text == "Visit Website"]),
        'phone': (''.join([(tag.find("a")).text for tag in restaurant.find_all("div", class_="c-mapstack__phone-url")])).replace('+', '\'+'),
    } for restaurant in soup.find_all("section", class_="c-mapstack__card")
]


with open(output_file_name, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writerows(restaurants)