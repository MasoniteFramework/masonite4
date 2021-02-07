from tests import TestCase
from src.masonite.routes import Route


class TestTesting(TestCase):
    def setUp(self):
        super().setUp()
        self.addRoutes(
            Route.get("/test", "WelcomeController@show").name("test"),
            Route.get("/test-404", "WelcomeController@not_found").name("not_found"),
            Route.get("/test-creation", "WelcomeController@create").name("create"),
            Route.get("/test-unauthorized", "WelcomeController@unauthorized").name("unauthorized"),
            Route.get("/test-forbidden", "WelcomeController@forbidden").name("forbidden"),
            Route.get("/test-empty", "WelcomeController@empty").name("empty"),
        )

    def test_assert_contains(self):
        self.get("/").assertContains("welcome")
        self.get("/").assertNotContains("welcome1")

    def test_assert_is_named(self):
        self.get("/test").assertIsNamed("test")
        self.get("/test").assertIsNotNamed("welcome")

    def test_assert_not_found(self):
        self.get("/test-404").assertNotFound()

    def test_assert_is_status(self):
        self.get("/test").assertIsStatus(200)

    def test_assert_ok(self):
        self.get("/test").assertOk()

    def test_assert_created(self):
        self.get("/test-creation").assertCreated()

    def test_assert_created(self):
        self.get("/test-unauthorized").assertUnauthorized()

    def test_assert_forbidden(self):
        self.get("/test-forbidden").assertForbidden()
