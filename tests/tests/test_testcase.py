from tests import TestCase
from src.masonite.routes import Route


class TestTesting(TestCase):
    def setUp(self):
        super().setUp()
        self.addRoutes(Route.get("/test", "WelcomeController@show").name("test"))

    def test_can_get_route(self):
        self.get("/").assertContains("welcome")
        self.get("/").assertNotContains("welcome1")

    def test_named_route(self):
        self.get("/test").assertIsNamed("test")
        self.get("/test").assertIsNotNamed("welcome")

    def test_named_route(self):
        self.get("/test").assertIsNamed("test")
        self.get("/test").assertIsNotNamed("welcome")
