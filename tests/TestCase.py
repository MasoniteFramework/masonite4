from src.masonite.tests import TestCase
from src.masonite.routes import Route


class TestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.addRoutes(
            Route.set_controller_locations("tests.integrations.controllers").get(
                "/", "WelcomeController@show"
            ),
            Route.set_controller_locations("tests.integrations.controllers").post(
                "/", "WelcomeController@show"
            ),
        )
