import re

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


def fetch(query: str):
    with Database() as db, db.connect() as conn, conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(query)
        fetch_condition = re.compile(r'(LIMIT 1)$|(LIMIT 1)\s+')

        if fetch_condition.search(query) is None:
            data = cur.fetchall()
        else:
            data = cur.fetchone()
    return data


def find_streams():
    return fetch("SELECT * FROM stream ORDER BY id DESC LIMIT 12")


def find_next_games():
    return fetch("SELECT * FROM game WHERE score = '0：0' ORDER BY id ASC LIMIT 12")


def find_last_games():
    return fetch("SELECT * FROM game WHERE score != '0：0' ORDER BY id DESC LIMIT 12")


def find_game(id: int):
    return fetch(f"SELECT * FROM game WHERE id = {id}")


def find_stream(id: int):
    return fetch(f"SELECT * FROM stream WHERE id = {id}")


def find_players_rank():
    return fetch("SELECT * FROM player_rank")


def find_newsies():
    return fetch("SELECT * FROM news ORDER BY date DESC LIMIT 12")


def find_news(id: int):
    return fetch(f"SELECT * FROM news WHERE id = {id}")


def find_shops():
    return fetch("SELECT * FROM shop LIMIT 12")


def find_shop(id: int):
    return fetch(f"SELECT * FROM shop WHERE id = {id}")
