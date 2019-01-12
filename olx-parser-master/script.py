#!/usr/bin/python3
# coding: utf-8
from bs4 import BeautifulSoup
import requests
import csv
import sys
import re
header = ['link', 'title', 'price', 'name', 'phone', 'time',
          'date', 'address', 'tags', 'content', 'ad_num', 'img']
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}

def get_phone(url):#Получить номер телефона со страницы
    uid = re.findall(r'-ID(.*?).html', url)[0]
    r = requests.get('http://olx.ua/ajax/misc/contact/phone/' + uid)
    phones = re.findall(r'([ 0-9]+)', r.text)

def get_html(url):#Получть страницу
    r = requests.get(url)
    return r.text

def get_page_data(url_page):#получить даные из обьявления 
    html = get_html(url_page)
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('div', class_='offercontentinner')
    try:
        title = ads.find('div', class_='offer-titlebox').find('h1').text.strip()
    except:
        title = ''
    try:
        text = ads.find('div', id='textContent').text.strip()
    except:
        text = ''
    try:
        data_pub = ads.find('em').text
    except:
        data_pub = ''
    try:
        img = ads.find('img', class_='vtop').get('src').split(';')[0]
    except:
        img =''
    try:
        data = {'title': title,'text': text,'data_pub': data_pub,'img': img}
        #print(data)
        write_csv(data)
    except:
        pass
def get_all_pages(html):#получить список всех страниц возвращает число
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('div', class_='pager').find_all('a', class_='block')[-1].get('href')
    total_pages = pages.split('=')[1]
    return int(total_pages)

def write_csv(data):#сохранить даные
    with open('olx.csv', 'a') as f:
        writer= csv.writer(f)
        writer.writerow((data['title'],data['text'],data['data_pub'],data['img']))

def get_all_post(html):#получить список обьявлений get_all_post возвращает ссылки
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find_all('tr', class_='wrap')
    for ad in ads:
        ad = ad.find('a').get('href').split('#')[0]
        get_page_data(ad)
def main():
    url = 'https://www.olx.ua/uslugi/stroitelstvo-otdelka-remont/'
    base_url = 'https://www.olx.ua/uslugi/stroitelstvo-otdelka-remont/'
    page_part = '?page='
    query_part = 'q-демонтаж/'
    total_pages = get_all_pages(get_html(url))
    for i in range(1, 2):
            url_gen = base_url + page_part + str(i)+'/' + query_part
            html = get_html(url_gen)
            get_all_post(html) 
            

if __name__ == '__main__':
    main()