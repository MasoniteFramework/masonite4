from src.masonite.tests import TestCase
from src.masonite.foundation import Application, Kernel, HttpKernel
from src.masonite.providers import RouteProvider
from src.masonite.routes import Route, RouteCapsule
from src.masonite.tests import HttpTestResponse
from src.masonite.foundation.response_handler import testcase_handler
from src.masonite.utils.helpers import generate_wsgi
from src.masonite.middleware.route.VerifyCsrfToken import VerifyCsrfToken
from src.masonite.request import Request
from src.masonite.environment import LoadEnvironment
from unittest.mock import MagicMock

import os
import json
import io


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
        self.register_mocks()

    def addRoutes(self, routes):
        self.application.make("router").add(routes)
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
                "wsgi.input": io.BytesIO(bytes(json.dumps(data), "utf-8")),
            }
        )

        request, response = testcase_handler(
            self.application,
            wsgi_request,
            self.mock_start_response,
            exception_handling=False,
        )

        route = self.application.make("router").find(route, method)
        if route:
            return HttpTestResponse(self.application, request, response, route)
        raise Exception(f"NO route found for {route}")

    def mock_start_response(self, *args, **kwargs):
        pass

    def register_mocks(self):
        """Configure the default mock classes for all services which needs to be mocked.
        The mocks can now be overriden.
        A package could in its service provider call a method which could update one of the mock
        class with the one installed.
        """
        # from src.masonite.tests.mocks import MockMail
        # self.application.bind("mock.mail", MockMail)

        # for test but should remove src.
        self.application.bind("mock.mail", "src.masonite.tests.mocks.MockMail")

        # self.application.bind("mock.queue", MockQueue)

    def fake(self, binding, mock_class=None):
        """Mock a service with its mocked implementation or with a given custom
        one."""
        import pydoc
        if not mock_class:
            mock_class_path = self.application.make(f"mock.{binding}")
            mock_class = pydoc.locate(mock_class_path)
        mock = mock_class(self.application)
        self.application.bind(binding, mock)
        return mock

    def restore(self, binding):
        """Restore the service previously mocked to the original one."""
        # how to retrieve the original ?
        original = self.application.make(binding)
        self.application.bind(binding, original)
