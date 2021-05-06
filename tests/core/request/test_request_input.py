from tests import TestCase
from src.masonite.utils.helpers import generate_wsgi
from src.masonite.request import Request


class TestRequest(TestCase):
    def setUp(self):
        self.request = Request(generate_wsgi({"PATH_INFO": "/test"}))

    def test_request_no_input_returns_false(self):
        self.assertEqual(self.request.input("notavailable"), False)

    def test_request_can_get_string_value(self):
        storages = {"test": "value"}
        self.request.input_bag.query_string = storages
        self.assertEqual(self.request.input("test"), "value")

    def test_request_can_get_list_value(self):
        storages = {"test": ["foo", "bar"]}
        self.request.input_bag.query_string = storages
        self.assertEqual(self.request.input("test"), ["foo", "bar"])
