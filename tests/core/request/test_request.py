from tests import TestCase
from src.masonite.request import Request
from src.masonite.utils.helpers import generate_wsgi
import os


class TestRequest(TestCase):
    def test_request_can_get_path(self):
        request = Request(generate_wsgi({"PATH_INFO": "/test"}))
        self.assertEqual(request.get_path(), "/test")
        self.assertEqual(request.get_request_method(), "GET")
