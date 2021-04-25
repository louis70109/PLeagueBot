import os

from flask import request
from flask_restful import Resource, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, \
    QuickReply, QuickReplyButton, MessageAction, URIAction

from utils.flex import stream_flex, regular_last_games_flex, regular_next_games_flex, help_flex, \
    rank_flex, \
    news_flex, shop_flex, \
    flex_message_type_condition, playoffs_last_games_flex, playoffs_next_games_flex, \
    final_games_flex

line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))


class LineController(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self):
        body = request.get_data(as_text=True)
        signature = request.headers['X-Line-Signature']

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            print("Invalid signature. Please check your channel access token/channel secret.")
            abort(400)

        return 'OK'

    @handler.add(MessageEvent, message=TextMessage)
    def handle_message(event):
        add_me_uri = f"https://liff.line.me/{os.getenv('LIFF_SHARE_ID')}"

        text = event.message.text
        alt = '觀看更多'
        quick_reply = QuickReply(
            items=[
                QuickReplyButton(action=MessageAction(label="影片🎬", text="最新影片")),
                QuickReplyButton(action=MessageAction(label="新聞📖", text="最新新聞")),
                QuickReplyButton(action=MessageAction(label="過往例行賽賽程", text="歷史例行賽賽程")),
                QuickReplyButton(action=MessageAction(label="例行賽剩餘賽程", text="例行賽剩餘賽程")),
                QuickReplyButton(action=MessageAction(label="排行榜✍️", text="球員數據排行榜")),
                QuickReplyButton(action=MessageAction(label="商品🛒", text="商品")),
                QuickReplyButton(action=URIAction(label="分享", uri=add_me_uri))
            ])
        if text == '最新影片':
            flex = stream_flex()
            alt = '最新影片'
        elif text == '歷史例行賽賽程':
            flex = regular_last_games_flex()
            alt = '歷史例行賽賽程'
        elif text == '例行賽剩餘賽程':
            flex = regular_next_games_flex()
            if not flex:
                flex = {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "目前例行賽程結束囉🏀"
                            }
                        ]
                    }
                }

            alt = '例行賽剩餘賽程'

        elif text == '過往季後賽':
            flex = playoffs_last_games_flex()
            alt = '過往季後賽賽程'
        elif text == '當前季後賽':
            flex = playoffs_next_games_flex()
            if not flex:
                flex = {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "目前季後賽賽程結束囉🏀"
                            }
                        ]
                    }
                }

            alt = '季後賽剩餘賽程'
        elif text == 'final':
            flex = final_games_flex()
            if not flex:
                flex = {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "目前尚未有總決賽喔🏀"
                            }
                        ]
                    }
                }

            alt = '總決賽賽程'
        elif text == '球員數據排行榜':
            flex = rank_flex()
            alt = '球員數據排行榜'
        elif text == '最新新聞':
            flex = news_flex()
            alt = '最新新聞'
        elif text == '商品':
            flex = shop_flex()
            alt = '來看看最近賣什麼吧！'
        else:
            flex = help_flex()

        flex_message = flex_message_type_condition(
            alt,
            flex,
            quick_reply=quick_reply
        )
        line_bot_api.reply_message(
            event.reply_token,
            messages=flex_message
        )
        return 'OK'
