import json
import io

from src.masonite.tests import TestCase
from src.masonite.routes import Route, RouteCapsule
from src.masonite.tests import HttpTestResponse
from src.masonite.foundation.response_handler import testcase_handler
from src.masonite.utils.helpers import generate_wsgi
from src.masonite.request import Request
from src.masonite.environment import LoadEnvironment
from unittest.mock import MagicMock


class TestCase(TestCase):
    def setUp(self):
        LoadEnvironment("testing")
        from wsgi import application

        self.application = application

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
        self._test_cookies = {}
        self._test_headers = {}

    def addRoutes(self, *routes):
        self.application.bind(
            "router",
            RouteCapsule(*routes),
        )
        return self

    def withCsrf(self):
        self._csrf = True
        return self

    def withoutCsrf(self):
        self._csrf = False
        return self

    def get(self, route, data=None):
        return self.fetch(route, data, method="GET")

    def post(self, route, data=None):
        return self.fetch(route, data, method="POST")

    def put(self, route, data=None):
        return self.fetch(route, data, method="PUT")

    def patch(self, route, data=None):
        return self.fetch(route, data, method="PATCH")

    def make_request(self, data={}):
        request = Request(generate_wsgi(data))
        request.app = self.application

        self.application.bind("request", request)
        return request

    def fetch(self, route, data=None, method=None):
        if data is None:
            data = {}
        token = self.application.make("sign").sign("cookie")
        data.update({"__token": token})
        wsgi_request = generate_wsgi(
            {
                "HTTP_COOKIE": f"SESSID={token}; csrf_token={token}",
                "CONTENT_LENGTH": len(str(json.dumps(data))),
                "REQUEST_METHOD": method,
                "PATH_INFO": route,
                "wsgi.input": io.BytesIO(bytes(json.dumps(data), "utf-8")),
            }
        )

        request, response = testcase_handler(
            self.application,
            wsgi_request,
            self.mock_start_response,
            exception_handling=False,
        )
        # add eventual cookies added inside the test (not encrypted to be able to assert value ?)
        for name, value in self._test_cookies.items():
            request.cookie(name, value, encrypt=False)
        # add eventual headers added inside the test
        for name, value in self._test_headers.items():
            request.header(name, value)

        route = self.application.make("router").find(route, method)
        print("rrr", route._name)
        if route:
            return HttpTestResponse(self.application, request, response, route)
        raise Exception(f"NO route found for {route}")

    def mock_start_response(self, *args, **kwargs):
        pass

    def withCookies(self, cookies_dict):
        self._test_cookies = cookies_dict
        return self

    def withHeaders(self, headers_dict):
        self._test_headers = headers_dict
        return self

    def actingAs(self, user):
        self.make_request()
        self.application.make("auth").guard("web").login_by_id(
            user.get_primary_key_value()
        )

    def fake(self, binding):
        mock = MagicMock(self.application.make(binding))
        self.application.bind(binding, mock)
        return mock
