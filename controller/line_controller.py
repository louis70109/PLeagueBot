import os

from flask import request
from flask_restful import Resource, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import InvalidSignatureError
from linebot.models import FlexSendMessage, MessageEvent, TextMessage, \
    QuickReply, QuickReplyButton, MessageAction

from utils.flex import stream_flex, last_games_flex, next_games_flex, help_flex

line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))
NOTIFY_BIND_URL = f"https://liff.line.me/{os.getenv('LIFF_BIND_ID')}"


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
        text = event.message.text
        alt = '觀看更多'
        quick_reply = QuickReply(
            items=[
                QuickReplyButton(action=MessageAction(label="排定直播", text="排定直播")),
                QuickReplyButton(action=MessageAction(label="歷史例行賽賽程", text="歷史例行賽賽程")),
                QuickReplyButton(action=MessageAction(label="例行賽剩餘賽程", text="例行賽剩餘賽程"))
            ])
        if text == '排定直播':
            flex = stream_flex()
            alt = 'Youtube 直播'
        elif text == '歷史例行賽賽程':
            flex = last_games_flex()
            alt = '歷史例行賽賽程'
        elif text == '例行賽剩餘賽程':
            flex = next_games_flex()
            alt = '例行賽剩餘賽程'
        else:
            flex = help_flex()

        flex_message = FlexSendMessage(
            alt_text=alt,
            contents=flex,
            quick_reply=quick_reply
        )
        line_bot_api.reply_message(
            event.reply_token,
            messages=flex_message
        )
        return 'OK'
