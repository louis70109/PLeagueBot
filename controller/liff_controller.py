import os
from flask import request, render_template, Response
from flask_restful import Resource

from models.game import Game
from models.news import News
from models.shop import Shop
from models.stream import Stream
from utils.db import find_stream, find_news, find_shop
from utils.flex import game_flex_template, stream_flex_template, news_flex_template, shop_flex_template, add_me

LIFF_ID = os.getenv('LIFF_SHARE_ID')


class LiffController(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self):
        if request.args.get('liff.state'):
            return Response(render_template('liff_redirect.html', liff_id=LIFF_ID))
        game = request.args.get('game')
        stream = request.args.get('stream')
        news = request.args.get('news')
        shop = request.args.get('shop')
        content = []
        alt = '你已被標註。'
        if game:
            alt = "分享 P+ 聯盟賽程給你"
            row = Game.query.filter_by(id=game).first()

            content.append(game_flex_template(
                row.id,
                row.customer_image,
                row.main_image,
                row.score,
                row.people,
                row.place,
                row.event_date)
            )
        elif stream:
            alt = "分享一個 P+ 影片給你"
            row = Stream.query.filter_by(id=stream).first()
            content.append(stream_flex_template(row.id, row.title, row.image, row.link))
        elif news:
            alt = "我找到一篇 P+ 的新聞啦！！"
            row = News.query.filter_by(id=news).first()
            content.append(news_flex_template(row))
        elif shop:
            alt = "分享個 P+ 商品給你～"
            row = Shop.query.filter_by(id=shop).first()
            content.append(shop_flex_template(row))
        else:
            content = [add_me()]

        msg = {"type": "flex", "altText": alt, "contents": {**{
            "type": "carousel",
            "contents": content
        }}}
        return Response(render_template('share_message.html', flex=msg, liff_id=LIFF_ID))
