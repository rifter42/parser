from bs4 import BeautifulSoup
import requests
import csv
import argparse
from params import *
import re
from datetime import datetime, timedelta
# from pprint import pprint


def get_html(url):
    cookies = {'u': '26k41o9t.1hwpsm.fk7lapyg58',
               'v': '1507202585',
               'f': '5.0c4f4b6d233fb90636b4dd61b04726f147e1eada7172e06c47e1eada7172e06c47e1eada7172e06c47e1eada7172e06cb59320d6eb6303c1b59320d6eb6303c1b59320d6eb6303c147e1eada7172e06c8a38e2c5b3e08b898a38e2c5b3e08b890df103df0c26013a7b0d53c7afc06d0b2ebf3cb6fd35a0ac7b0d53c7afc06d0b0df103df0c26013a2e1d4a3283ded56ac7cea19ce9ef44010f7bd04ea141548c71e7cb57bbcb8e0f91e52da22a560f550df103df0c26013a1d6703cbe432bc2a2da10fb74cac1eab2da10fb74cac1eabdc5322845a0cba1af722fe85c94f7d0c2da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eab3c02ea8f64acc0bd71e7cb57bbcb8e0f868aff1d7654931c9d8e6ff57b051a58fcdcb83ce67b2bc22e661fe11e4048251da9f488c469f075b45dedc156187ff9bff688bb9eddf4b753bc326cd5f74c8bb365f56e92c925c5f6d90886864009ff5dcded8022a3c9fccbf1a5019b899285164b09365f5308e7618389eb05215248e9588c3b47f43a942da10fb74cac1eab2da10fb74cac1eab659b3dea12741bc13045c25caf03c073',
               'dfp_group': '28'
               }
    r = requests.get(url, cookies=cookies)
    return r.text


def get_page_count(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        last_page = soup.find('div', class_='pagination-pages').find_all('a', class_='pagination-page')[-1].get('href')
        count = int(last_page.split('=')[1].split('&')[0])
    except:
        count = 1
    return count


def parse_date(date):
    ret = date
    today = datetime.today()
    yesterday = today - timedelta(days=1)
    fmt = "%d.%m"
    dates = {
            'Сегодня': datetime.strftime(today, fmt),
            'Вчера': datetime.strftime(yesterday, fmt),
            'января': '01',
            'февраля': '02',
            'марта': '03',
            'апреля': '04',
            'мая': '05',
            'июня': '06',
            'июля': '07',
            'августа': '08',
            'сентября': '09',
            'октября': '10',
            'ноября': '11',
            'декабря': '12',
            }

    for k, v in dates.items():
        if k in date:
            ret = ret.replace(k, v)
            ret = ret.replace(" ", ".")
    return ret


def get_rooms_param(rooms):
    if rooms is None:
        return ''
    params = {'0': '5702',
              '1': '5703',
              '2': '5704',
              '3': '5705',
              '4': '5706',
              '5': '5707',
              '6': '5708',
              '7': '11022',
              '8': '11023',
              '9': '11024',
              '10': '11025'
              }
    ret = []
    for number in rooms:
        if number in params:
            ret.append(params[number])
    return "&f=550_" + '-'.join(ret)


def get_subways_param(subways):
    if subways is None:
        return ''
    params = subways_list
    ret = []
    for subway in subways:
        if subway.capitalize() in params:
            ret.append(params[subway.capitalize()])
    return "&metro=" + '-'.join(ret)


def get_price_param(price):
    if price is None:
        return ''
    return '&pmax=' + price


def get_ads(html):
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('div', class_='catalog-list').find_all('div', class_='item_table')
    ads_list = []
    for ad in ads:
        try:
            title = ad.find('div', class_='description').find('h3').text.strip()
        except:
            title = ''

        try:
            url = 'https://www.avito.ru' + ad.find('div', class_='description').find('h3').find('a').get('href')
        except:
            url = ''

        try:
            address = "м. " + ad.find('div', class_='description').find('p', class_='address').text.strip()
        except:
            address = ''

        try:
            price = ad.find('div', class_='about').text.strip()
        except:
            price = ''

        try:
            date = ad.find('div', class_='data').find('div', class_='date').text.strip()
            
           # if "Вчера" in date or "Сегодня" in date: 
           #     date_d = date[:-6]
           #     date = re.sub("Сегодня", dates_list[date_d], date)
                #date.replace("Сегодня", dates_list[date[:-6]])
                #date_d = date[:-6]
           #     print(date)
                #print(dates_list[date[:-6]])
           # else:
           #     if (re.search('^\d{2}', date)):
           #         date_d = date[3:-6]
           #     else:
           #         date_d = date[2:-6]
    
        except:
            date = ''


        data = {'title': title,
                'price': price,
                'url': url,
                'address': address,
                'date': parse_date(date),
                }
        ads_list.append(data)
    return ads_list


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-m", "--max")
    argparser.add_argument("-r", "--rooms", nargs="*")
    argparser.add_argument("-s", "--subways", nargs="*")
    args = argparser.parse_args()

    base_url = 'https://www.avito.ru/sankt-peterburg/kvartiry/sdam/na_dlitelnyy_srok?'
    page_part = 'p='
    params = '{pmax}&pmin=0&s=101&user=1{subways}{rooms}'.format(pmax=get_price_param(args.max),
                                                                 subways=get_subways_param(args.subways),
                                                                 rooms=get_rooms_param(args.rooms))
    page_count = get_page_count(get_html(base_url+params))
    for i in range(1, page_count+1):
        url = base_url + page_part + str(i) + params
        ads = get_ads(get_html(url))
        with open('shit.csv', 'a') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=['title', 'price', 'address', 'url', 'date'])
            writer.writeheader()
            writer.writerows(ads)

        # print(get_ads(get_html(url)))

if __name__ == '__main__':
    main()
