import os
from tests import TestCase
from src.masonite.foundation import Application
from src.masonite.response import Response
from src.masonite.routes import Route


class TestResponseHelpers(TestCase):
    def setUp(self):
        super().setUp()
        self.setRoutes(
            Route.get("/test-with-errors", "WelcomeController@with_errors").name(
                "with_errors"
            ),
        )

    def test_with_input(self):
        pass

    def test_with_errors(self):
        # response = self.response.with_errors({"name": "Field is required"})
        # assert isinstance(response, Response)
        # TODO: check errors in session
        # assert Session.get("errors")
        self.get("/test-with-errors").assertSessionHasErrors().assertSessionHasErrors(
            ["email"]
        )
