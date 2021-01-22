import re
import time

import requests
from bs4 import BeautifulSoup
import psycopg2
import psycopg2.extras

import urllib.parse as urlparse
import os

URL = urlparse.urlparse(os.getenv('DATABASE_URL'))
DB_NAME = URL.path[1:]
USER = URL.username
PASSWORD = URL.password
HOST = URL.hostname
PORT = URL.port


class Database:
    conns = []

    def __enter__(self):
        return self

    def connect(self):
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT
        )
        self.conns.append(conn)

        return conn

    def __exit__(self, type, value, traceback):
        for conn in self.conns:
            conn.close()

        self.conns.clear()


def db_table_check():
    try:
        with Database() as db, db.connect() as conn, conn.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(f'''
                CREATE TABLE public.news
                (
                    id serial NOT NULL PRIMARY KEY,                    
                    image character varying(255) COLLATE pg_catalog."default",
                    link character varying(255) COLLATE pg_catalog."default",
                    date character varying(12) COLLATE pg_catalog."default",
                    tag character varying(15) COLLATE pg_catalog."default" NOT NULL,
                    "description" character varying(100) COLLATE  pg_catalog."default" NOT NULL,
                    CONSTRAINT desc_unique UNIQUE (description)
                    INCLUDE(description)                    
                )
                TABLESPACE pg_default;

                ALTER TABLE public.news
                    OWNER to {USER};
            ''')
            conn.commit()
    except psycopg2.errors.DuplicateTable:
        print('Tables have been create.')
        pass
    except Exception as e:
        raise Exception(e)


def insert_news(news):
    with Database() as db, db.connect() as conn, conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        for new in news:
            cur.execute(f'''
                INSERT INTO news (date, image, link, tag, description)
                    VALUES (
                    '{new.get('date')}', 
                    '{new.get('image')}',
                    '{new.get('link')}',
                    '{new.get('tag')}',
                    '{new.get('description')}'
                ) ON CONFLICT ON CONSTRAINT desc_unique
                DO NOTHING''')
        conn.commit()


def news_crawler():
    print("Check DB status")
    db_table_check()
    print("Check DB Done")

    res = requests.get('https://pleagueofficial.com/news', headers={
        'User-Agent': 'Firefox browser\'s user-agent',
    })
    soup = BeautifulSoup(res.content, 'html.parser')
    time.sleep(2)
    print("Got news and clear them...")
    news = []
    for dt in soup.find_all(class_='col-lg-4 col-md-4 col-6 mb-md-5 mb-3 px-md-2 px-2'):
        new: dict = {}
        img = dt.find('img')
        if 'src' in img.attrs and (img['src'].endswith('.png') or img['src'].endswith('.jpg')):
            new['image'] = 'https://pleagueofficial.com' + img['src']
        news_more = dt.find('a', class_='news_more')
        if 'href' in news_more.attrs and news_more['href'].startswith('/news-detail'):
            new['link'] = 'https://pleagueofficial.com' + news_more['href']
        new['date'] = dt.find(class_='text-light opacity-5 fs12').get_text()
        new['tag'] = dt.find(class_='news_cate fs12 float-right').get_text()
        new['description'] = dt.find(
            class_='text-light fs16 mt-3 line-height-12 font-weight-normal').get_text()

        news.append(new)
    time.sleep(1)
    insert_news(news)
    print("Insert ok!")


news_crawler()
