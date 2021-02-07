from tests import TestCase
from src.masonite.routes import Route


class TestTesting(TestCase):
    def setUp(self):
        super().setUp()
        self.addRoutes(
            Route.get("/test", "WelcomeController@show").name("test"),
            Route.get("/view", "WelcomeController@view").name("view"),
            Route.get("/view-context", "WelcomeController@view_with_context").name("view_with_context"),
            Route.get("/test-404", "WelcomeController@not_found").name("not_found"),
            Route.get("/test-creation", "WelcomeController@create").name("create"),
            Route.get("/test-unauthorized", "WelcomeController@unauthorized").name("unauthorized"),
            Route.get("/test-forbidden", "WelcomeController@forbidden").name("forbidden"),
            Route.get("/test-empty", "WelcomeController@empty").name("empty"),
            Route.get("/test-response-header", "WelcomeController@response_with_headers"),
            Route.get("/test-redirect-1", "WelcomeController@redirect_url"),
            Route.get("/test-redirect-2", "WelcomeController@redirect_route"),
            Route.get("/test-redirect-3", "WelcomeController@redirect_route_with_params"),
            Route.get("/test/@id", "WelcomeController@with_params").name("test_params"),
            Route.get("/test-json", "WelcomeController@json").name("json"),
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

    def test_assert_unauthorized(self):
        self.get("/test-unauthorized").assertUnauthorized()

    def test_assert_forbidden(self):
        self.get("/test-forbidden").assertForbidden()

    def test_assert_no_content(self):
        self.get("/test-empty").assertNoContent()

    def test_assert_cookie(self):
        self.with_cookies({"test": "value"}).get("/").assertCookie("test")

    def test_assert_cookie_value(self):
        self.with_cookies({"test": "value"}).get("/").assertCookie("test", "value")

    def test_assert_cookie_missing(self):
        self.get("/").assertCookieMissing("test")

    def test_assert_plain_cookie(self):
        # for now test cookies are not encrypted
        self.with_cookies({"test": "value"}).get("/").assertPlainCookie("test")

    def test_assert_has_header(self):
        self.get("/test-response-header").assertHasHeader("TEST")
        self.get("/test-response-header").assertHasHeader("TEST", "value")

    def test_assert_header_missing(self):
        self.get("/").assertHeaderMissing("X-Test")

    def test_assert_request_with_headers(self):
        request = self.with_headers({"X-TEST": "value"}).get("/").request
        assert request.header("X-Test").value == "value"

    def test_assert_redirect_to_url(self):
        self.get("/test-redirect-1").assertRedirect("/")

    def test_assert_redirect_to_route(self):
        self.get("/test-redirect-2").assertRedirect(name="test")
        self.get("/test-redirect-3").assertRedirect(name="test", params={"id": 1})

    def test_assert_session_has(self):
        self.get("/").assertSessionHas("testkey")

    def test_assert_view_is(self):
        self.get("/view").assertViewIs("view")

    def test_assert_view_has(self):
        self.get("/view-context").assertViewHas("count")
        self.get("/view-context").assertViewHas("count", 1)
        self.get("/view-context").assertViewHas("users", ["John", "Joe"])

        with self.assertRaises(AssertionError):
            self.get("/view-context").assertViewHas("not_in_view")
        with self.assertRaises(AssertionError):
            self.get("/view-context").assertViewHas("not_in_view", 3)

    def test_assert_view_helpers_raise_error_if_not_rendering_a_view(self):
        # json response
        with self.assertRaises(ValueError):
            self.get("/test-json").assertViewIs("test")
        # string response
        with self.assertRaises(ValueError):
            self.get("/test").assertViewIs("test")

    def test_assert_view_has_all(self):
        self.get("/view-context").assertViewHasAll(["users", "count"])
        self.get("/view-context").assertViewHasAll({"count": 1, "users": ["John", "Joe"]})

        with self.assertRaises(AssertionError):
            self.get("/view-context").assertViewHasAll(["users", "count", "not in data"])

        with self.assertRaises(AssertionError):
            self.get("/view-context").assertViewHasAll({"count": 1})

    def test_assert_view_missing(self):
        self.get("/view-context").assertViewMissing("not in data")

        with self.assertRaises(AssertionError):
            self.get("/view-context").assertViewMissing("users")
