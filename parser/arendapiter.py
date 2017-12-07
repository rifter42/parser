#!/usr/bin/python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import re
import json
from datetime import datetime, date
import telegram
import socket
import logging
logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

socket.setdefaulttimeout(30000)

bot = telegram.Bot(token='460196768:AAE_xDprLl4-mQ5qHFDtaDgRQXkflaTTkcg')

post_data = {
                    "sposob": "1",
                    "region": "1",
                    "region_no": "0",
                    "tip_poiska": "3",
                    "oper": "1",
                    "term1": "1",
                    "prod_ch0": u"не+важно",
                    "est_ch_pro17": u"2к.кв.",
                    "s_ch0": u"не+важно",
                    "r_ch0": u"не+важно",
                    "rlo_ch0": u"не+важно",
                    "m_ch12": u"Горьковская",
                    "m_ch33": u"Московские+ворота",
                    "m_ch41": u"Петроградская",
                    "m_ch54": u"Технол.+институт",
                    "m_ch59": u"Фрунзенская",
                    "m_ch60": u"Электросила",
                    "price1": "",
                    "price2": "30000",
                    "val": "RUR",
                    "foto": "1",
                    "so1": "",
                    "so2": "",                                                                                                                                                                                     "sz1": "",                                                                                                                                                                                     "sz2": "",
                    "rinki": "0",                                                                                                                                                                                  "SearchGO": u"Искать",                                                                                                                                                                         "var_number": "",                                                                                                                                                                              "SearchGO": u"Искать",

                    }

params = {'act': 'date'}
cookies = {'pcode': 'rtst98vg6qggefbu3bn1pqmi66', 'ap_token': 'NHLQ3j1%2Bw66XcHiz3JSF7K5kWjTy9Q%2BPuHYlP%2F8I7oY%3D'}
base_url = 'http://arenda-piter.ru'
headers={'Accept-Encoding': 'plain'}

html = requests.post("http://arenda-piter.ru/master_result.php", cookies=cookies, data=post_data,  headers=headers).text

soup = BeautifulSoup(html, 'html.parser')

table = soup.find('table', class_='tbm_01')
rows = table.find_all('tr')
rows = list(filter(lambda tr: tr.has_attr('id'), rows))

ads = []
dates = []

date_regex = re.compile(r'\d{2}:\d{2}\d{2}\.\d{2}\.\d{2}')
subway_regex = re.compile(r'([^0-9\f\n\r\t\v]+\s?[^0-9\f\n\r\t\v\s])+')

for row in rows:
    date_tag = row.find('td', class_='tdm_01')
    date = date_regex.search(date_tag.text).group(0)
    time = date[:5]
    date = date[5:]
    
    subways = row.find('td', class_='tdm_03').text
    subways = subways.replace(u'\xa0', u' ').strip()
    subways = re.sub('\d+\sм\.п\.', '', subways).split(',') # P I Z D A R I K I

    uri = row.find('td', class_='tdm_09').find('a').get('href')

    ads.append({'date': date, 'time': time, 'link': base_url+uri, 'subways': subways})

print(ads)
with open('/home/fernir/scripts/python_scripts/parser/lastdate', 'r') as f:
        lastdate = f.readline()
        lastdate = lastdate.strip()


for i in range (0, len(ads)):
    date = ads[i]['date'] + " " + ads[i]['time']
    date = datetime.strptime(date, "%d.%m.%y %H:%M")
    dates.append(date)

dates.sort()

lastdate = datetime.strptime(lastdate,"%Y-%m-%d %H:%M:%S")
print(dates)
currentdate = dates[-1]
delta = currentdate - lastdate

if (delta != 0):
        for i in range(0, len(ads)):
            date = ads[i]['date'] + " " + ads[i]['time']
            if (datetime.strptime(date,"%d.%m.%y %H:%M") > lastdate):
                print("date:", ads[i]['date'], " subway:", ads[i]['subways'], " link:", ads[i]['link'])
                message = ' '.join(ads[i]['subways']) + ads[i]['link']
                bot.send_message(-309483787, message)

with open('/home/fernir/scripts/python_scripts/parser/lastdate', 'w') as f:
    f.write(str(dates[-1]))
