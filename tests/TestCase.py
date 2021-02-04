from src.masonite.tests import TestCase
from src.masonite.foundation import Application, Kernel, HttpKernel
from src.masonite.providers import RouteProvider
from src.masonite.routes import Route, RouteCapsule
from src.masonite.tests import HttpTestResponse
from src.masonite.foundation.response_handler import testcase_handler
from src.masonite.utils.helpers import generate_wsgi
from src.masonite.middleware.route.VerifyCsrfToken import VerifyCsrfToken

import os
import json
import io


class TestCase(TestCase):
    def setUp(self):
        self.application = Application(os.getcwd())
        self.application.register_providers(Kernel, HttpKernel)
        self.application.add_providers(RouteProvider)

        self.application.bind(
            "router",
            RouteCapsule(
                Route.set_controller_module_location("tests.integrations.web").get(
                    "/", "WelcomeController@show"
                )
            ),
        )

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

    def fetch(self, route, data=None, method=None):
        if data is None:
            data = {}
        token = self.application.make("sign").sign("cookie")
        data.update({"__token": token})
        wsgi_request = generate_wsgi(
            {
                "HTTP_COOKIE": f"SESSID=cookie; csrf_token={token}",
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
