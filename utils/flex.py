import os

from utils.db import find_streams, find_last_games, find_next_games

SHARE_ID = os.getenv('LIFF_SHARE_ID')
SHARE_LINK = f"https://liff.line.me/{SHARE_ID}"


def stream_flex_template(id, title, image, link):
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
            "layout": "horizontal",
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
                }, {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "uri",
                        "label": "分享",
                        "uri": f"{SHARE_LINK}/?stream={id}"
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
        content.append(stream_flex_template(row['id'], row['title'], row['image'], row['link']))
    return {
        "type": "carousel",
        "contents": content
    }


def game_flex_template(id, guest_image, main_image, score, people, location, date):
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
                "text": f"{location}",
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
            }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": [
                 {
                    "type": "button",
                    "action": {
                        "type": "uri",
                        "label": "官方網站",
                        "uri": "https://pleagueofficial.com/schedule-regular-season"
                    },
                    "style": "link"
                }, {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "uri",
                        "label": "分享",
                        "uri": f"{SHARE_LINK}/?game={id}"
                    }
                }
            ],
            "flex": 0
        }
    }


def last_games_flex():
    rows = find_last_games()
    content = []
    for row in rows:
        content.append(
            game_flex_template(
                row['id'],
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
    rows = find_next_games()
    content = []
    for row in rows:
        content.append(
            game_flex_template(
                row['id'],
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


def help_flex():
    return {
        "type": "carousel",
        "contents": [
            {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "最新影片",
                                "text": "最新影片"
                            }
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "歷史例行賽賽程",
                                "text": "歷史例行賽賽程"
                            }
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "例行賽剩餘賽程",
                                "text": "例行賽剩餘賽程"
                            }
                        }
                    ]
                }
            }
        ]
    }
