import json
import time

import requests
from bs4 import BeautifulSoup
import psycopg2
import psycopg2.extras

import urllib.parse as urlparse
import os
from lotify.client import Client

lotify = Client()
notify = os.getenv('LINE_NOTIFY_TOKEN')

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
                CREATE TABLE public.stream
                (
                    id serial NOT NULL PRIMARY KEY,
                    link character varying(255) COLLATE pg_catalog."default",
                    image character varying(255) COLLATE pg_catalog."default",
                    title character varying(100) COLLATE pg_catalog."default",
                    is_live boolean DEFAULT false,
                    CONSTRAINT stream_unique UNIQUE (link, image, title)
                        INCLUDE(link, image, title)
                )
                TABLESPACE pg_default;
    
                ALTER TABLE public.game
                    OWNER to {USER};
                ALTER TABLE public.stream
                    OWNER to {USER};
            ''')
            conn.commit()
    except psycopg2.errors.DuplicateTable:
        print('Tables have been create.')
        pass
    except Exception as e:
        raise Exception(e)


def stream_parser():
    yt = requests.get('https://www.youtube.com/c/PLEAGUEofficial/videos?view=2&sort=dd&live_view=502&shelf_id=2')
    message = BeautifulSoup(yt.content, 'html.parser')
    video_scripts = message.find_all('script')
    bs_to_string = str(video_scripts[32])
    variable_string = bs_to_string.split('var ytInitialData = ')[1].split(';')[0]
    variable_dict = json.loads(variable_string)
    clean_list = variable_dict["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][1]["tabRenderer"]["content"][
        "sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"][0]["gridRenderer"]["items"]
    streams = []
    for data in clean_list:
        if data.get("gridVideoRenderer") is None:
            break
        image = data["gridVideoRenderer"]["thumbnail"]['thumbnails'][3]["url"].split('?sqp')[0]
        title = data["gridVideoRenderer"]["title"]["runs"][0]["text"]
        link_path = "https://www.youtube.com/" + \
                    data["gridVideoRenderer"]["navigationEndpoint"]["commandMetadata"]["webCommandMetadata"]["url"]
        streams.append({'title': title, 'link': link_path, 'image': image})

    return streams


def insert_or_update_to_stream(streams):
    with Database() as db, db.connect() as conn, conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        print("Refresh stream table.")
        for stream in streams:
            cur.execute(f'''
                INSERT INTO stream (title, image, link)
                    VALUES (
                    '{stream.get('title')}', 
                    '{stream.get('image')}',
                    '{stream.get('link')}'
                ) ON CONFLICT ON CONSTRAINT stream_unique
                DO UPDATE SET
                title = '{stream.get('title')}',
                image = '{stream.get('image')}',
                link = '{stream.get('link')}'
            ''')
        conn.commit()


def all_game():
    schedule = requests.get(
        'https://pleagueofficial.com/schedule-regular-season', headers={
            'User-Agent': 'Google browser\'s user-agent',
        })
    soup = BeautifulSoup(schedule.content, 'html.parser')
    date, week, time, teams, images, scores, places, people = [], [], [], [], [], [], [], []
    try:
        for dt in soup.find_all(class_='fs16 mt-2 mb-1'):
            date.append(dt.get_text())
        for wk in soup.find_all(class_='fs12 mb-2'):
            week.append(wk.get_text())
        for t in soup.select('.col-lg-1.col-12.text-center.align-self-center.match_row_datetime > h6[class~=fs12]'):
            time.append(t.get_text())
    except Exception as e:
        lotify.send_message(access_token=notify, message=f'比賽資訊網站格式錯誤 \n{e}')

    event_date = []  # Arrange date to one
    for index in range(len(date)):
        event_date.append(f'{date[index]}{week[index]} {time[index]}')

    for team in soup.find_all(class_='PC_only fs14'):
        teams.append(team.get_text())
    for img in soup.find_all('img', {'class': 'w105'}):  # 2 to be a play
        if 'src' in img.attrs:
            if img['src'].startswith('https://pleagueofficial.com/') and img['src'].endswith('.png'):
                images.append(img['src'])
    for score in soup.find_all('h6', {'class': 'PC_only fs22'}):
        scores.append(score.get_text())
    for place in soup.find_all('h5', {'class': 'fs12 mb-0'}):
        places.append(place.get_text())
    for person in soup.find_all('div', {'class': 'mt-3 mb-md-0 mb-3 fs12 text-center PC_only'}):
        people.append(person.get_text())
    return event_date, teams, scores, places, people, images


def arrange_lists_to_one(event, teams, scores, places, people, images) -> list:
    games = []
    length = len(event)
    index, index2 = 0, 0
    while index < length:
        games.append({
            'event_date': event[index],
            'customer': teams[index2],
            'main': teams[index2 + 1],
            'customer_image': images[index2],
            'main_image': images[index2 + 1],
            'people': people[index],
            'place': places[index],
            'score': f'{scores[index2]}：{scores[index2 + 1]}'
        })
        index += 1
        index2 += 2
    return games


def insert_or_update_to_game(games: list):
    with Database() as db, db.connect() as conn, conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        for game in games:
            cur.execute(f'''
                INSERT INTO game (customer, customer_image, main, main_image, score, people, place, event_date)
                    VALUES (
                    '{game.get('customer')}', 
                    '{game.get('customer_image')}', 
                    '{game.get('main')}', 
                    '{game.get('main_image')}', 
                    '{game.get('score')}', 
                    '{game.get('people')}', 
                    '{game.get('place')}',
                    '{game.get('event_date')}'
                ) ON CONFLICT ON CONSTRAINT game_unique
                DO UPDATE SET
                score = '{game.get('score')}',
                place = '{game.get('place')}',
                people = '{game.get('people')}',
                event_date = '{game.get('event_date')}'
            ''')
        conn.commit()


def main():
    print('Check tables status...')
    try:
        db_table_check()
    except Exception as e:
        lotify.send_message(access_token=notify, message=f'DB 建立出錯 \n{e}')
    time.sleep(1)
    print('Youtube stream loading...')
    try:
        streams = stream_parser()
    except Exception as e:
        lotify.send_message(
            access_token=notify,
            message=f'Youtube 爬蟲出事啦\n{e}')
    print('Stream gotcha!')
    time.sleep(1)
    print('Sync stream data to database.')
    try:
        insert_or_update_to_stream(streams)
    except Exception:
        lotify.send_message(
            access_token=notify,
            message=f'影片檔案資訊無法進入 db\n陣列: {str(streams)}')
    print('Sync games...')
    event_date, teams, scores, places, people, images = all_game()
    print('Sync game data to database...')
    games: list = arrange_lists_to_one(event_date, teams, scores, places, people, images)
    print('Game arrange done.')
    time.sleep(2)
    print('Ready to insert games.')
    try:
        insert_or_update_to_game(games)
    except Exception:
        lotify.send_message(
            access_token=notify,
            message=f'比賽資訊無法進入 db\n陣列: {str(games)}')
    print('Insert games done.')


main()
