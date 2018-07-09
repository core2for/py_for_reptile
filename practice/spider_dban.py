import requests
import chardet
from bs4 import BeautifulSoup
import time
import string
import pymysql


def get_text(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'}
    r = requests.get(url, headers=headers)
    return r.text


def get_all_url(soup):
    tag_urls = list()
    home_url = 'https://book.douban.com'
    for link in soup.find_all('a'):
        tag = link.get('href')
        if tag is not None:
            tag_urls.append(home_url + tag)
    return tag_urls


def get_conn():
    conn = pymysql.connect(host='localhost', db='douban', user='root', password='', port=3306)
    return conn


def create_table(table_sql):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(table_sql)
        conn.commit()
    except ConnectionError:
        conn.rollback()
    finally:
        if conn is not None:
            conn.close()


def insert_data(title, author_price, pl, rating_nums, intros):
    insert_sql = "insert into db_book(title, author_price, rating_nums, pl, intros) values('" + title + "'," \
                 + "'" + author_price + "','" + rating_nums + "','" + pl + "','" + intros + "')"
    conn = get_conn()
    cursor = conn.cursor()
    # '''insert into db_book(title, author_price, rating_nums, pl, intros) values(%s, %s, %s, %s, %s)''' % (
    # title, author_price, rating_nums, pl, intros))这种方式字符串太长拼接失败
    try:
        cursor.execute(insert_sql)
        conn.commit()
    except ConnectionError:
        conn.rollback()
    finally:
        if conn is not None:
            conn.close()


def get_messages():
    table_sql = 'create table IF NOT EXISTS db_book(bid bigint primary key auto_increment, ' \
                'title varchar(60),' \
                'author_price varchar(200),' \
                'pl varchar(50),' \
                'rating_nums char(3),' \
                'intros varchar(500))'
    create_table(table_sql)
    url = 'https://book.douban.com/tag/'
    home_url = 'https://book.douban.com'
    text = get_text(url)
    soup = BeautifulSoup(text, 'lxml')
    divs = soup.find(name='div', attrs={'class', ''})
    tag_urls = get_all_url(divs)
    # one = tag_urls[0]
    # 开始爬“豆瓣标签页”
    # 这个循环是全部的标签
    for tag_url in tag_urls:
        # print(tag_url)
        # one_text = get_text(one)
        if tag_url is not None:
            for i in range(0, 1000, 20):
                one_text = get_text(tag_url + '?start={0}'.format(i))
                one_soup = BeautifulSoup(one_text, 'lxml')
                one_div = one_soup.find(name='ul', attrs={'class', 'subject-list'})
                subject_items = one_div.find_all(name='li', attrs={'class', 'subject-item'})
                # 开始获取当前标签的每一页的书籍
                for subject_item in subject_items:
                    info = subject_item.find(name='div', attrs={'class', 'info'})
                    title = info.find('a').get('title')
                    author_price = info.find(name='div', attrs={'class', 'pub'}).string
                    pl = info.find(name='span', attrs={'class', 'pl'}).string
                    rating_nums = info.find(name='span', attrs={'class', 'rating_nums'}).string
                    intros = info.find('p').string
                    insert_data(title.strip(), author_price.strip().replace(' ', ''), pl.strip(), rating_nums.strip(), intros.strip())
                    time.sleep(8)
                time.sleep(30)
        time.sleep(60)


if __name__ == '__main__':
    get_messages()
