import os

from linebot.models import FlexSendMessage

from utils.db import find_streams, find_last_games, find_next_games, find_players_rank, find_newsies, find_shops

SHARE_ID = os.getenv('LIFF_SHARE_ID')
SHARE_LINK = f"https://liff.line.me/{SHARE_ID}"


def flex_message_type_condition(alt: str, contents: list or dict, **kwargs):
    if type(contents) == list:
        output_flex_message = {
            "type": "carousel",
            "contents": [*contents]
        }
    else:
        output_flex_message = {**contents}

    return FlexSendMessage(
        alt,
        output_flex_message,
        **kwargs
    )


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
                        "label": "影片連結",
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
    return content


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
    return content


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
    return  content



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
                        }, {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "歷史例行賽賽程",
                                "text": "歷史例行賽賽程"
                            }
                        }, {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "例行賽剩餘賽程",
                                "text": "例行賽剩餘賽程"
                            }
                        }, {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "球員數據排行榜",
                                "text": "球員數據排行榜"
                            }
                        }, {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "新聞",
                                "text": "最新新聞"
                            }
                        }
                    ]
                }
            }
        ]
    }


def player_rank_flex_template(rows):
    mapping = {
        'scores': '得分',
        'rebounds': '籃板',
        'assists': '助攻',
        'steals': '抄截',
        'blocks': '阻攻',
        'two': '兩分球',
        'three': '三分球',
        'freethrow': '罰球'
    }
    content, rank_name = [], ''
    for row in rows:
        rank_name = row.get('rank_name')
        content.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [{
                "type": "text",
                "text": row.get('player'),
                "size": "lg",
                "color": "#555555",
                "flex": 0
            }, {
                "type": "text",
                "text": row.get('average'),
                "size": "sm",
                "color": "#111111",
                "align": "end"
            }]
        })
        content.append({
            "type": "box",
            "layout": "vertical",
            "contents": [{
                "type": "text",
                "text": row.get('team'),
                "size": "xxs",
                "color": "#aaaaaa",
                "wrap": True,
                "gravity": "top"
            }]
        })

    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [{
                "type": "text",
                "text": "排行榜",
                "weight": "bold",
                "color": "#1DB446",
                "size": "sm"
            }, {
                "type": "text",
                "text": mapping[rank_name],
                "weight": "bold",
                "size": "xxl",
                "margin": "md"
            }, {
                "type": "text",
                "text": "P. League+",
                "size": "xs",
                "color": "#aaaaaa",
                "wrap": True
            }, {
                "type": "separator",
                "margin": "xxl"
            }, {
                "type": "box",
                "layout": "vertical",
                "margin": "xxl",
                "spacing": "sm",
                "contents": content
            }, {
                "type": "separator",
                "margin": "xxl"
            }]
        },
        "styles": {
            "footer": {
                "separator": True
            }
        }
    }


def mapping_rank_name(rows):
    mapping = [
        'scores',
        'rebounds',
        'assists',
        'steals',
        'blocks',
        'two',
        'three',
        'freethrow'
    ]
    ranking, content = [], []
    for name in mapping:
        for row in rows:
            if row.get('rank_name') == name:
                ranking.append(row)
        content.append(player_rank_flex_template(ranking))
        ranking = []
    return content


def rank_flex():
    rows = find_players_rank()

    return mapping_rank_name(rows)


def news_flex():
    rows = find_newsies()
    content = []
    for row in rows:
        content.append(news_flex_template(row))

    return content


def news_flex_template(news):
    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [{
                "type": "image",
                "url": news['image'],
                "size": "full",
                "aspectMode": "cover",
                "aspectRatio": "2:3",
                "gravity": "top"
            }, {
                "type": "box",
                "layout": "vertical",
                "contents": [{
                    "type": "box",
                    "layout": "vertical",
                    "contents": [{
                        "type": "text",
                        "text": news['date'],
                        "size": "xl",
                        "color": "#ffffff",
                        "weight": "bold",
                    }]
                }, {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [{
                        "type": "text",
                        "text": news['description'],
                        "color": "#ebebeb",
                        "size": "sm",
                        "flex": 0,
                        "wrap": True
                    }],
                    "spacing": "lg"
                }, {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [{
                        "type": "filler"
                    }, {
                        "type": "box",
                        "layout": "baseline",
                        "contents": [{
                            "type": "filler"
                        }, {
                            "type": "text",
                            "text": "新聞連結",
                            "color": "#ffffff",
                            "flex": 0,
                            "offsetTop": "-2px"
                        }, {
                            "type": "filler"
                        }],
                        "spacing": "sm",
                        "action": {
                            "type": "uri",
                            "label": "新聞",
                            "uri": news['link']
                        }
                    }, {
                        "type": "filler"
                    }],
                    "borderWidth": "1px",
                    "cornerRadius": "4px",
                    "spacing": "sm",
                    "borderColor": "#ffffff",
                    "margin": "xxl",
                    "height": "40px"
                }],
                "position": "absolute",
                "offsetBottom": "0px",
                "offsetStart": "0px",
                "offsetEnd": "0px",
                "backgroundColor": "#03303Acc",
                "paddingAll": "20px",
                "paddingTop": "18px"
            }, {
                "type": "box",
                "layout": "vertical",
                "contents": [{
                    "type": "text",
                    "text": news['tag'],
                    "color": "#ffffff",
                    "align": "center",
                    "size": "xs",
                    "offsetTop": "3px",
                    "wrap": True
                }],
                "position": "absolute",
                "cornerRadius": "20px",
                "offsetTop": "18px",
                "backgroundColor": "#ff334b",
                "offsetStart": "18px",
                "height": "25px",
                "width": "100px"
            }, {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "#點我分享",
                        "align": "center",
                        "size": "xs",
                        "offsetTop": "3px",
                        "wrap": True
                    }
                ],
                "position": "absolute",
                "cornerRadius": "20px",
                "offsetTop": "18px",
                "backgroundColor": "#a6ed8e",
                "height": "25px",
                "width": "100px",
                "offsetEnd": "18px",
                "action": {
                    "type": "uri",
                    "label": "action",
                    "uri": f"{SHARE_LINK}/?news={news.get('id')}"
                }
            }],
            "paddingAll": "0px"
        }
    }


def shop_flex() -> list:
    rows = find_shops()
    content = []
    for row in rows:
        content.append(shop_flex_template(row))
    return content


def shop_flex_template(shop):
    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [{
                "type": "image",
                "url": shop['image'],
                "size": "full",
                "aspectMode": "cover",
                "aspectRatio": "2:2",
                "gravity": "top"
            }, {
                "type": "box",
                "layout": "vertical",
                "contents": [{
                    "type": "box",
                    "layout": "vertical",
                    "contents": [{
                        "type": "text",
                        "text": shop['product'],
                        "size": "xl",
                        "color": "#ffffff",
                        "weight": "bold",
                    }]
                }, {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [{
                        "type": "text",
                        "text": shop['price'],
                        "color": "#ebebeb",
                        "size": "sm",
                        "flex": 0,
                        "wrap": True
                    }],
                    "spacing": "lg"
                }, {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [{
                        "type": "filler"
                    }, {
                        "type": "box",
                        "layout": "baseline",
                        "contents": [{
                            "type": "filler"
                        }, {
                            "type": "text",
                            "text": "購買連結",
                            "color": "#ffffff",
                            "flex": 0,
                            "offsetTop": "-2px"
                        }, {
                            "type": "filler"
                        }],
                        "spacing": "sm",
                        "action": {
                            "type": "uri",
                            "label": "物品",
                            "uri": shop['link']
                        }
                    }, {
                        "type": "filler"
                    }],
                    "borderWidth": "1px",
                    "cornerRadius": "4px",
                    "spacing": "sm",
                    "borderColor": "#ffffff",
                    "margin": "xxl",
                    "height": "40px"
                }],
                "position": "absolute",
                "offsetBottom": "0px",
                "offsetStart": "0px",
                "offsetEnd": "0px",
                "backgroundColor": "#03303Acc",
                "paddingAll": "20px",
                "paddingTop": "18px"
            }, {
                "type": "box",
                "layout": "vertical",
                "contents": [{
                    "type": "text",
                    "text": "熱賣！",
                    "color": "#ffffff",
                    "align": "center",
                    "size": "xs",
                    "offsetTop": "3px",
                    "wrap": True
                }],
                "position": "absolute",
                "cornerRadius": "20px",
                "offsetTop": "18px",
                "backgroundColor": "#ff334b",
                "offsetStart": "18px",
                "height": "25px",
                "width": "100px"
            }, {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "#點我分享",
                        "align": "center",
                        "size": "xs",
                        "offsetTop": "3px",
                        "wrap": True
                    }
                ],
                "position": "absolute",
                "cornerRadius": "20px",
                "offsetTop": "18px",
                "backgroundColor": "#a6ed8e",
                "height": "25px",
                "width": "100px",
                "offsetEnd": "18px",
                "action": {
                    "type": "uri",
                    "label": "action",
                    "uri": f"{SHARE_LINK}/?shop={shop.get('id')}"
                }
            }],
            "paddingAll": "0px"
        }
    }
