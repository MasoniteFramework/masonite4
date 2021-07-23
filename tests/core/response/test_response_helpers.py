import os
from tests import TestCase
from src.masonite.foundation import Application
from src.masonite.response import Response


class TestResponseHelpers(TestCase):
    def setUp(self):
        application = Application(os.getcwd())
        self.response = Response(application)

    def test_with_input(self):
        pass

    def test_with_errors(self):
        response = self.response.with_errors({"name": "Field is required"})
        assert isinstance(response, Response)
        # TODO: check errors in session
        # assert Session.get("errors")
