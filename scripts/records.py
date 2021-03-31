import re
import time

import requests
from bs4 import BeautifulSoup
import psycopg2
import psycopg2.extras

import urllib.parse as urlparse
import os

URL = urlparse.urlparse(os.getenv('DATABASE_URI'))
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
                CREATE TABLE public.player_rank
                (
                    id serial NOT NULL PRIMARY KEY,
                    player character varying(10) COLLATE pg_catalog."default",
                    team character varying(10) COLLATE pg_catalog."default",
                    average character varying(10) COLLATE pg_catalog."default",
                    rank_name character varying(10) COLLATE pg_catalog."default" NOT NULL
                );
                CREATE TABLE public.team_rank
                (
                    win character varying(3) COLLATE pg_catalog."default",
                    lose character varying(3) COLLATE pg_catalog."default",
                    average character varying(7) COLLATE pg_catalog."default",
                    team character varying(15) COLLATE pg_catalog."default" NOT NULL,
                    game character varying(3) COLLATE pg_catalog."default",
                    CONSTRAINT team_rank_pkey PRIMARY KEY (team)
                )
                TABLESPACE pg_default;

                ALTER TABLE public.team_rank
                    OWNER to {USER};
                ALTER TABLE public.player_rank
                    OWNER to {USER};
            ''')
            conn.commit()
    except psycopg2.errors.DuplicateTable:
        print('Tables have been create.')
        pass
    except Exception as e:
        raise Exception(e)


def player_ranking(rank_soup):
    players = rank_soup.find_all(class_='fs14 font-weight-bold')
    team_name = rank_soup.find_all(class_='fs12 d-block text-secondary opacity-4')
    average = rank_soup.find_all(class_='text-light fs14')

    ranking_list = []
    for index in range(len(players)):
        ranking_list.append({
            'player': players[index].get_text(),
            'team': team_name[index].get_text(),
            'average': average[index].get_text()
        })
    return ranking_list


def ranking_list(soup):
    rank = {
        'scores': [],
        'rebounds': [],
        'assists': [],
        'steals': [],
        'blocks': [],
        'two': [],
        'three': [],
        'freethrow': []
    }

    for dt in soup.find_all(class_='table-responsive fs14'):
        data_list = dt.find(
            class_='text-md-left text-center fs14 text_strong pl-md-3 pl-0').get_text()
        ranking = player_ranking(dt)
        if re.search('(\s+)?得分(\s+)?', data_list):
            rank['scores'] = ranking
        elif re.search('(\s+)?籃板(\s+)?', data_list):
            rank['rebounds'] = ranking
        elif re.search('(\s+)?助攻(\s+)?', data_list):
            rank['assists'] = ranking
        elif re.search('(\s+)?抄截(\s+)?', data_list):
            rank['steals'] = ranking
        elif re.search('(\s+)?阻攻(\s+)?', data_list):
            rank['blocks'] = ranking
        elif re.search('(\s+)?二分球(\s+)?', data_list):
            rank['two'] = ranking
        elif re.search('(\s+)?三分球(\s+)?', data_list):
            rank['three'] = ranking
        elif re.search('(\s+)?罰球(\s+)?', data_list):
            rank['freethrow'] = ranking
    return rank


def game_record_list(soup):
    teams, games, games_win, games_lose, games_records = [], [], [], [], []
    for dt in soup.find_all(class_='bg-deepgray text-light'):
        teams.append(dt.find('a', class_='fs14').get_text())
    for dt in soup.find_all(class_='bg-deepgray text-light'):
        tmp_records = []
        records_list = dt.find_all('td', class_='')
        records_length = len(records_list)
        for index in range(records_length):
            tmp_records.append(records_list[index].get_text())
        games.append(tmp_records[0])
        games_win.append(tmp_records[1])
        games_lose.append(tmp_records[2])
        games_records.append(tmp_records[3])
    result = []
    for index in range(len(teams)):
        result.append({
            'team': teams[index],
            'game': games[index],
            'win': games_win[index],
            'lose': games_lose[index],
            'average': games_records[index]
        })
    return result


def insert_to_player_team_rank(ranks):
    with Database() as db, db.connect() as conn, conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute('DELETE FROM team_rank')
        print("Refresh team_rank table.")

        for rank in ranks:
            cur.execute(f'''
                INSERT INTO team_rank (team, game, win, lose, average)
                    VALUES (
                    '{rank.get('team')}',                        
                    '{rank.get('game')}',
                    '{rank.get('win')}',
                    '{rank.get('lose')}',                        
                    '{rank.get('average')}'
                )''')
        conn.commit()


def insert_to_player_rank(ranks):
    with Database() as db, db.connect() as conn, conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute('DELETE FROM player_rank')
        print("Refresh player_rank table.")

        for key, rank_list in ranks.items():
            for rank in rank_list:
                cur.execute(f'''
                    INSERT INTO player_rank (player, team, average, rank_name)
                        VALUES (
                        '{rank.get('player')}', 
                        '{rank.get('team')}',
                        '{rank.get('average')}',
                        '{key}'
                    )''')
        conn.commit()


def full_ranking():
    print("Check DB status")
    db_table_check()
    print("Check DB Done")
    res = requests.get('https://pleagueofficial.com/stat_ranking', headers={
        'User-Agent': 'Firefox browser\'s user-agent',
    })
    soup = BeautifulSoup(res.content, 'html.parser')
    time.sleep(1)
    print('Load games ranking...')
    games_rank = game_record_list(soup=soup)
    print('Start to insert data.')
    insert_to_player_team_rank(games_rank)
    print('Insert games ranking records done.')
    time.sleep(2)
    print('Load players racords...')
    players_rank = ranking_list(soup=soup)
    print('Start to insert data.')
    insert_to_player_rank(players_rank)
    print('Insert players records done.')
    time.sleep(2)


full_ranking()
