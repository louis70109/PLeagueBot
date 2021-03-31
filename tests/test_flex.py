import json
import unittest
import responses
from _pytest.monkeypatch import MonkeyPatch

from utils.flex import flex_message_type_condition, stream_flex_template, SHARE_ID


class BufferedIOBase:
    def __init__(self, name="example.png"):
        self.name = name


class TestClient(unittest.TestCase):
    def setUp(self):
        pass

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

        expected_query_string = {"altText": "notification message", "contents": {"contents": [{"hero": {
            "action": {"type": "uri", "uri": "LINK_RUL"}, "aspectMode": "cover", "aspectRatio": "20:13", "size": "full",
            "type": "image", "url": "IMAGE_URL"}, "type": "bubble"}], "type": "carousel"}, "type": "flex"}

        self.compare_object_json(result, expected_query_string)

    def test_flex_type_condition_by_empty_contents(self):
        test_data = []
        result = flex_message_type_condition(alt='notification message', contents=test_data)

        expected_query_string = {"altText": "notification message", "contents": {"contents": [], "type": "carousel"},
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
            "action": {"type": "uri", "uri": "LINK_RUL"}, "aspectMode": "cover", "aspectRatio": "20:13", "size": "full",
            "type": "image", "url": "IMAGE_URL"}, "type": "bubble"}, "type": "flex"}

        self.compare_object_json(result, expected_query_string)

    def test_stream_flex_template(self):
        MonkeyPatch().setattr('utils.flex.SHARE_LINK', "https://liff.line.me/TEST_ID")
        result = stream_flex_template(id="1", title='TITLE', image='IMAGE_URL', link='JUST_LINK')
        expected_query_string = {'type': 'bubble',
                                 'hero': {'type': 'image', 'url': 'IMAGE_URL', 'size': 'full', 'aspectRatio': '20:13',
                                          'aspectMode': 'cover', 'action': {'type': 'uri', 'uri': 'JUST_LINK'}},
                                 'body': {'type': 'box', 'layout': 'vertical', 'contents': [
                                     {'type': 'text', 'text': 'TITLE', 'weight': 'bold', 'size': 'lg', 'wrap': True}]},
                                 'footer': {'type': 'box', 'layout': 'horizontal', 'spacing': 'sm', 'contents': [
                                     {'type': 'button', 'style': 'link', 'height': 'sm',
                                      'action': {'type': 'uri', 'label': '影片連結', 'uri': 'JUST_LINK'}},
                                     {'type': 'button', 'style': 'link', 'height': 'sm',
                                      'action': {'type': 'uri', 'label': '分享',
                                                 'uri': 'https://liff.line.me/TEST_ID/?stream=1'}}], 'flex': 0}}
        self.assertEqual(result, expected_query_string)
