from src.masonite.tests import TestCase
from src.masonite.foundation import Application, Kernel
from src.masonite.providers import RouteProvider
from src.masonite.routes import Route, RouteCapsule
from src.masonite.tests import HttpTestResponse


class TestCase(TestCase):
    def setUp(self):
        self.application = Application()
        self.application.register_providers(Kernel)
        self.application.add_providers(RouteProvider)
        self.application.bind(
            "router", RouteCapsule(Route.get("/", "WelcomeController@show"))
        )

    def addRoutes(self, routes):
        self.application.make("router").add(routes)
        return self

    def test_can_get_route(self):
        self.get("/").assertContains("welcome")
        self.get("/").assertNotContains("welcome1")

    def get(self, route, data=None):
        return self.fetch(route, data, method="GET")

    def post(self, route, data=None):
        return self.fetch(route, data, method="POST")

    def put(self, route, data=None):
        return self.fetch(route, data, method="PUT")

    def patch(self, route, data=None):
        return self.fetch(route, data, method="PATCH")

    def fetch(self, route, data=None, method="GET"):
        if data is None:
            data = {}

        route = self.application.make("router").find(route, method)

        if route:
            return HttpTestResponse(self.application, route)
