from src.masonite.tests import TestCase
from src.masonite.routes import Route, RouteCapsule


class TestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.application.bind(
            "router",
            RouteCapsule(
                Route.set_controller_module_location(
                    "tests.integrations.controllers"
                ).get("/", "WelcomeController@show"),
                Route.set_controller_module_location(
                    "tests.integrations.controllers"
                ).post("/", "WelcomeController@show"),
            ),
        )
