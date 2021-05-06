import json
import io
import pendulum

from src.masonite.tests.TestCommand import TestCommand
from src.masonite.tests import TestCase
from src.masonite.routes import Route, Router
from src.masonite.tests import HttpTestResponse
from src.masonite.foundation.response_handler import testcase_handler
from src.masonite.utils.helpers import generate_wsgi
from src.masonite.request import Request
from src.masonite.environment import LoadEnvironment


class TestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.application.bind(
            "router",
            Router(
                Route.set_controller_module_location(
                    "tests.integrations.controllers"
                ).get("/", "WelcomeController@show"),
                Route.set_controller_module_location(
                    "tests.integrations.controllers"
                ).post("/", "WelcomeController@show"),
            ),
        )
