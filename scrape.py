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
	csvwriter.writerow(['pub_date', 'title', 'teaser', 'url'])
	for page in range(1, 481, 15):
		r = requests.get(base + str(page))
		soup = BeautifulSoup(r.text)
		articles = soup.find_all('div', class_='item-info')
		for art in articles:
			row = []
			row.append(art.p.time['datetime'])
			row.append(ignore_ascii(art.h1.a.string, row[0]))
			tease = ignore_ascii(art.p.find('a').contents[1], row[0])
			row.append(tease)
			row.append(art.h1.a['href'])
			csvwriter.writerow(row)