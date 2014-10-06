# -*- coding: utf-8 -*-

import requests, csv
from bs4 import BeautifulSoup

base = 'http://www.npr.org/series/4578972/kitchen-window/archive?start='

# .encode replaces long dash characters with ? then replace with short dash
def ignore_ascii(text, date):
	try:
		return text.encode('ascii', 'replace').replace(' ? ', ' - ')
	except TypeError:
		print 'could not encode, skipped '+date

with open('articles.csv', 'wb') as c:
	csvwriter = csv.writer(c)
	csvwriter.writerow(['pub_date', 'title', 'teaser', 'url', 'img_url'])
	for page in range(1, 485, 15):
		r = requests.get(base + str(page))
		soup = BeautifulSoup(r.text)
		articles = soup.find_all('article')
		for article in articles:
			if article['class'][0] == 'item':
				row = []
				itemdiv = article.find('div', class_='item-info')
				row.append(itemdiv.p.time['datetime'])
				row.append(ignore_ascii(itemdiv.h1.a.string, row[0]))
				tease = ignore_ascii(itemdiv.p.find('a').contents[1], row[0])
				row.append(tease)
				row.append(itemdiv.h1.a['href'])
				if article['class'][1] == 'has-image':
					row.append(article.img['src'])
				else:
					row.append('')
				csvwriter.writerow(row)