from tests import TestCase
from src.masonite.routes import Route
from src.masonite.utils.helpers import generate_wsgi
from src.masonite.request import Request


class TestResponseHelpers(TestCase):
    def setUp(self):
        super().setUp()
        self.setRoutes(
            Route.get("/test-with-errors", "WelcomeController@with_errors"),
            Route.get("/test-with-input", "WelcomeController@form_with_input"),
        )

    def test_with_input(self):
        res = self.get("/test-with-input", {"name": "Sam"}).assertSessionHas(
            "name", "Sam"
        )

    def test_with_errors(self):
        self.get("/test-with-errors").assertSessionHasErrors().assertSessionHasErrors(
            ["email"]
        )
