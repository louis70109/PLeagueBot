import re
import time

import requests
from bs4 import BeautifulSoup, element
import psycopg2
import psycopg2.extras

import urllib.parse as urlparse
import os

from requests import models

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


def insert_shop_data(news):
    with Database() as db, db.connect() as conn, conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        for new in news:
            cur.execute(f'''
                INSERT INTO news (product, image, price)
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
    # db_table_check()
    print("Check DB Done")

    res: models.Response = requests.get('https://pleagueofficial.com/shop', headers={
        'User-Agent': 'IE browser\'s user-agent',
    })

    soup: BeautifulSoup = BeautifulSoup(res.content, 'html.parser')
    # time.sleep(2)
    print("Got shop data and clear them...")
    shops: list = []
    for dt in soup.find_all(class_='card product-card'):
        shop: dict = {}
        img: element.Tag = dt.find('img')
        if 'src' in img.attrs and (img['src'].endswith('.png') or img['src'].endswith('.jpg')):
            shop['image']: str = 'https://pleagueofficial.com' + img['src']

        shop['product']: str = dt.find(class_='fs12 py-0 my-0 text-black').get_text()
        shop['price']: str = dt.find(class_='py-1 my-0 text-black fs18').get_text()

        shops.append(shop)
    # time.sleep(1)
    # insert_shop_data(news)
    print("Insert ok!")


news_crawler()
