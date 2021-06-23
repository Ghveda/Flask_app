import sqlite3
import requests
from bs4 import BeautifulSoup

conn = sqlite3.connect('wrote.sqlite')
cursor = conn.cursor()




data = []
for i in range(3):
        url = 'https://www.bbcgoodfood.com/recipes/collection/cocktail-recipes/'+str(i)
        req = requests.get(url).text
        bs = BeautifulSoup(req, 'html.parser')
        table = bs.find('div', class_='row-cards')
        all_data = table.find_all('div', class_='template-article__row')

        for each in all_data:
            try:
                main = each.find('h4', class_='standard-card-new__display-title heading-4')
                title = main.text
                link = main.a.attrs['href']
                row = (title, link)
                data.append(row)
                cursor.execute('''
                INSERT INTO parsing(title, link) VALUES (?,?)
                ''', data)
            except:
                pass

