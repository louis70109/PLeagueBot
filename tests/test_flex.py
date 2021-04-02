import json
import unittest
from _pytest.monkeypatch import MonkeyPatch
from mock import patch

from models.game import Game
from models.stream import Stream
from utils.flex import flex_message_type_condition, stream_flex_template, stream_flex, \
    game_flex_template, last_games_flex


class TestClient(unittest.TestCase):
    def setUp(self):
        # sub-function generates liff URL too.
        MonkeyPatch().setattr('utils.flex.SHARE_LINK', "https://liff.line.me/TEST_ID")

    def compare_object_json(self, object_data, json_data):
        self.assertEqual(json.loads(str(object_data)), json_data)

    def test_flex_type_condition(self):
        test_data = [{
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "IMAGE_URL",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "action": {
                    "type": "uri",
                    "uri": "LINK_RUL"
                }
            }}]
        result = flex_message_type_condition(alt='notification message', contents=test_data)

        expected_query_string = {"altText": "notification message",
                                 "contents": {"contents": [{"hero": {
                                     "action": {"type": "uri", "uri": "LINK_RUL"},
                                     "aspectMode": "cover", "aspectRatio": "20:13", "size": "full",
                                     "type": "image", "url": "IMAGE_URL"}, "type": "bubble"}],
                                     "type": "carousel"}, "type": "flex"}

        self.compare_object_json(result, expected_query_string)

    def test_flex_type_condition_by_empty_contents(self):
        test_data = []
        result = flex_message_type_condition(alt='notification message', contents=test_data)

        expected_query_string = {"altText": "notification message",
                                 "contents": {"contents": [], "type": "carousel"},
                                 "type": "flex"}

        self.compare_object_json(result, expected_query_string)

    def test_flex_type_condition_by_dict_flex(self):
        test_data = {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "IMAGE_URL",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "action": {
                    "type": "uri",
                    "uri": "LINK_RUL"
                }
            }}
        result = flex_message_type_condition(alt='notification message', contents=test_data)

        expected_query_string = {"altText": "notification message", "contents": {"hero": {
            "action": {"type": "uri", "uri": "LINK_RUL"}, "aspectMode": "cover",
            "aspectRatio": "20:13", "size": "full",
            "type": "image", "url": "IMAGE_URL"}, "type": "bubble"}, "type": "flex"}

        self.compare_object_json(result, expected_query_string)

    def test_stream_flex_template(self):
        result = stream_flex_template(id="1", title='TITLE', image='IMAGE_URL', link='JUST_LINK')
        expected_query_string = {
            'type': 'bubble',
            'hero': {'type': 'image', 'url': 'IMAGE_URL', 'size': 'full',
                     'aspectRatio': '20:13',
                     'aspectMode': 'cover',
                     'action': {'type': 'uri', 'uri': 'JUST_LINK'}},
            'body': {'type': 'box', 'layout': 'vertical', 'contents': [
                {'type': 'text', 'text': 'TITLE', 'weight': 'bold',
                 'size': 'lg', 'wrap': True}]},
            'footer': {'type': 'box', 'layout': 'horizontal', 'spacing': 'sm',
                       'contents': [
                           {'type': 'button', 'style': 'link', 'height': 'sm',
                            'action': {'type': 'uri', 'label': '影片連結',
                                       'uri': 'JUST_LINK'}},
                           {'type': 'button', 'style': 'link', 'height': 'sm',
                            'action': {'type': 'uri', 'label': '分享',
                                       'uri': 'https://liff.line.me/TEST_ID/?stream=1'}}],
                       'flex': 0}}
        self.assertEqual(result, expected_query_string)

    @patch('utils.flex.Stream')
    def test_stream_flex(self, mock_query):
        # Mock ORM query
        mock_query.query.order_by.return_value.limit.return_value.all.return_value = [
            Stream(id=1, link='https://link', image='https://image', title='title',
                   is_live=False)]

        result = stream_flex()
        expected = [{
            'type': 'bubble', 'hero': {
                'type': 'image', 'url': 'https://image', 'size': 'full',
                'aspectRatio': '20:13', 'aspectMode': 'cover',
                'action': {'type': 'uri', 'uri': 'https://link'}},
            'body': {'type': 'box', 'layout': 'vertical', 'contents': [
                {'type': 'text', 'text': 'title', 'weight': 'bold', 'size': 'lg', 'wrap': True}]},
            'footer': {'type': 'box', 'layout': 'horizontal', 'spacing': 'sm', 'contents': [
                {'type': 'button', 'style': 'link', 'height': 'sm',
                 'action': {'type': 'uri', 'label': '影片連結', 'uri': 'https://link'}},
                {'type': 'button', 'style': 'link', 'height': 'sm',
                 'action': {'type': 'uri', 'label': '分享',
                            'uri': 'https://liff.line.me/TEST_ID/?stream=1'}}], 'flex': 0}}]
        mock_query.ssert_called_once()
        self.assertEqual(result, expected)
        self.assertEqual(list, type(expected))

    def test_game_flex_template(self):
        result = game_flex_template(
            1,
            'http://guest_image',
            'http://main_image',
            '100：99',
            '1000/1001',
            '台北富邦',
            '3/10 星期六')
        expected = {
            'type': 'bubble', 'header': {
                'type': 'box', 'layout': 'horizontal',
                'contents': [{
                    'type': 'image',
                    'url': 'http://guest_image'},
                    {'type': 'text', 'text': 'ＶＳ',
                     'gravity': 'center',
                     'align': 'center', 'size': 'xxl',
                     'weight': 'bold'}, {'type': 'image',
                                         'url': 'http://main_image'}]},
            'hero': {'type': 'box', 'layout': 'vertical', 'contents': [
                {'type': 'text', 'text': '100：99', 'align': 'center', 'gravity': 'center',
                 'size': 'xxl', 'weight': 'bold'},
                {'type': 'text', 'text': '現場 1000/1001 入場', 'gravity': 'center',
                 'align': 'center', 'size': 'md', 'margin': 'md'}]},
            'body': {'type': 'box', 'layout': 'vertical', 'contents': [
                {'type': 'text', 'text': '台北富邦', 'weight': 'bold', 'size': 'xl',
                 'gravity': 'center', 'align': 'center'},
                {'type': 'text', 'text': '3/10 星期六', 'align': 'center', 'size': 'md',
                 'margin': 'md'}]},
            'footer': {
                'type': 'box', 'layout': 'horizontal', 'spacing': 'sm',
                'contents': [{
                    'type': 'button',
                    'action': {'type': 'uri', 'label': '官方網站',
                               'uri': 'https://pleagueofficial.com/schedule-regular-season'},
                    'style': 'link'},
                    {'type': 'button', 'style': 'link', 'height': 'sm',
                     'action': {'type': 'uri', 'label': '分享',
                                'uri': 'https://liff.line.me/TEST_ID/?game=1'}}],
                'flex': 0}}

        self.assertEqual(result, expected)

    @patch('utils.flex.Game')
    def test_last_games_flex(self, mock_query):
        mock_query.query.filter.return_value.order_by.return_value \
            .limit.return_value.all.return_value = [
            Game(id=1, customer='Nijia team', customer_image='https://link',
                 main='台中就是隊', main_image='https://image', score='100：99',
                 people='1000/1000', place='台灣', event_date='3/10 禮拜日')]

        result = last_games_flex()
        expected = [{
            'type': 'bubble', 'header': {
                'type': 'box', 'layout': 'horizontal',
                'contents': [
                    {'type': 'image', 'url': 'https://link'},
                    {'type': 'text', 'text': 'ＶＳ',
                     'gravity': 'center', 'align': 'center',
                     'size': 'xxl', 'weight': 'bold'},
                    {'type': 'image', 'url': 'https://image'}]},
            'hero': {'type': 'box', 'layout': 'vertical', 'contents': [
                {'type': 'text', 'text': '100：99', 'align': 'center', 'gravity': 'center',
                 'size': 'xxl', 'weight': 'bold'},
                {'type': 'text', 'text': '現場 1000/1000 入場', 'gravity': 'center',
                 'align': 'center', 'size': 'md', 'margin': 'md'}]},
            'body': {'type': 'box', 'layout': 'vertical', 'contents': [
                {'type': 'text', 'text': '台灣', 'weight': 'bold', 'size': 'xl',
                 'gravity': 'center', 'align': 'center'},
                {'type': 'text', 'text': '3/10 禮拜日', 'align': 'center', 'size': 'md',
                 'margin': 'md'}]},
            'footer': {
                'type': 'box', 'layout': 'horizontal', 'spacing': 'sm',
                'contents': [{
                    'type': 'button',
                    'action': {'type': 'uri', 'label': '官方網站',
                               'uri': 'https://pleagueofficial.com/schedule-regular-season'},
                    'style': 'link'},
                    {'type': 'button', 'style': 'link', 'height': 'sm',
                     'action': {'type': 'uri', 'label': '分享',
                                'uri': 'https://liff.line.me/TEST_ID/?game=1'}}],
                'flex': 0}}]

        mock_query.ssert_called_once()
        self.assertEqual(result, expected)
        self.assertEqual(list, type(expected))
