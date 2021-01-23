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


def find_streams():
    with Database() as db, db.connect() as conn, conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("SELECT * FROM stream ORDER BY id DESC LIMIT 12")
        rows = cur.fetchall()
    return rows


def find_next_games():
    with Database() as db, db.connect() as conn, conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("SELECT * FROM game WHERE score = '0：0' ORDER BY id ASC LIMIT 12")
        rows = cur.fetchall()
    return rows


def find_last_games():
    with Database() as db, db.connect() as conn, conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("SELECT * FROM game WHERE score != '0：0' ORDER BY id DESC LIMIT 12")
        rows = cur.fetchall()
    return rows


def find_game(id):
    with Database() as db, db.connect() as conn, conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(f"SELECT * FROM game WHERE id = {id}")
        row = cur.fetchone()
    return row


def find_stream(id):
    with Database() as db, db.connect() as conn, conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(f"SELECT * FROM stream WHERE id = {id}")
        row = cur.fetchone()
    return row


def find_players_rank():
    with Database() as db, db.connect() as conn, conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("SELECT * FROM player_rank")
        rows = cur.fetchall()
    return rows


def find_newsies():
    with Database() as db, db.connect() as conn, conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("SELECT * FROM news ORDER BY date DESC LIMIT 12")
        rows = cur.fetchall()
    return rows


def find_news(id):
    with Database() as db, db.connect() as conn, conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(f"SELECT * FROM news WHERE id = {id}")
        row = cur.fetchone()
    return row
