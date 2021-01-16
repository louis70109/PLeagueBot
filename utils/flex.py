import os

from utils.db import find_streams, find_last_games

SHARE_ID = os.getenv('LIFF_SHARE_ID')


def stream_flex_template(title, image, link):
    return {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": image,
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
            "action": {
                "type": "uri",
                "uri": link
            }
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": title,
                    "weight": "bold",
                    "size": "lg",
                    "wrap": True
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "uri",
                        "label": "直播連結",
                        "uri": link
                    }
                }
            ],
            "flex": 0
        }
    }


def stream_flex():
    rows = find_streams()
    content = []
    for row in rows:
        content.append(stream_flex_template(row['title'], row['image'], row['link']))
    return {
        "type": "carousel",
        "contents": content
    }


def game_flex_template(guest_image, main_image, score, people, location, date):
    return {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "image",
                    "url": guest_image
                }, {
                    "type": "text",
                    "text": "ＶＳ",
                    "gravity": "center",
                    "align": "center",
                    "size": "xxl",
                    "weight": "bold"
                }, {
                    "type": "image",
                    "url": main_image
                }
            ]
        },
        "hero": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": score,
                    "align": "center",
                    "gravity": "center",
                    "size": "xxl",
                    "weight": "bold"
                }, {
                    "type": "text",
                    "text": f"現場 {people} 入場",
                    "gravity": "center",
                    "align": "center",
                    "size": "md",
                    "margin": "md"
                }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [{
                "type": "text",
                "text": f"🏀 {location} 🏀",
                "weight": "bold",
                "size": "xl",
                "gravity": "center",
                "align": "center"
            }, {
                "type": "text",
                "text": date,
                "align": "center",
                "size": "md",
                "margin": "md"
            }, {
                "type": "button",
                "action": {
                    "type": "uri",
                    "label": "官方網站",
                    "uri": "https://pleagueofficial.com/schedule-regular-season"
                },
                "style": "link"
            }
            ]
        }
    }


def last_games_flex():
    rows = find_last_games()
    content = []
    for row in rows:
        content.append(
            game_flex_template(
                row['customer_image'],
                row['main_image'],
                row['score'],
                row['people'],
                row['place'],
                row['event_date']))
    return {
        "type": "carousel",
        "contents": content
    }


def next_games_flex():
    rows = find_last_games()
    content = []
    for row in rows:
        content.append(
            game_flex_template(
                row['customer_image'],
                row['main_image'],
                row['score'],
                row['people'],
                row['place'],
                row['event_date']))
    return {
        "type": "carousel",
        "contents": content
    }
