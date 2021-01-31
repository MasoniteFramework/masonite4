from .HTTPRoute import HTTPRoute
from ..utils.helpers import flatten


class Route:

    routes = []
    compilers = {
        "int": r"(\d+)",
        "integer": r"(\d+)",
        "string": r"([a-zA-Z]+)",
        "default": r"([\w.-]+)",
        "signed": r"([\w\-=]+)",
    }

    controller_module_location = "app.http.controllers"

    def __init__(self, routes=[]):
        if routes:
            self.routes = routes

    @classmethod
    def add(self, route):
        self.routes.append(route)
        return self

    @classmethod
    def get(self, url, controller, **options):
        route = HTTPRoute(
            url,
            controller,
            request_method=["get"],
            compilers=self.compilers,
            module_location=self.controller_module_location,
            **options
        )
        self.routes.append(route)
        return route

    @classmethod
    def post(self, url, controller, **options):
        route = HTTPRoute(
            url,
            controller,
            request_method=["post"],
            compilers=self.compilers,
            **options
        )
        self.routes.append(route)
        return route

    @classmethod
    def put(self, url, controller, **options):
        self.routes.append(
            HTTPRoute(
                url,
                controller,
                request_method=["put"],
                compilers=self.compilers,
                **options
            )
        )
        return self

    @classmethod
    def patch(self, url, controller, **options):
        route = HTTPRoute(
            url,
            controller,
            request_method=["patch"],
            compilers=self.compilers,
            **options
        )
        self.routes.append(route)
        return route

    @classmethod
    def delete(self, url, controller, **options):
        route = HTTPRoute(
            url,
            controller,
            request_method=["delete"],
            compilers=self.compilers,
            **options
        )
        self.routes.append(route)
        return route

    @classmethod
    def option(self, url, controller, **options):
        route = HTTPRoute(
            url,
            controller,
            request_method=["options"],
            compilers=self.compilers,
            **options
        )
        self.routes.append(route)
        return route

    @classmethod
    def default(self, url, controller, **options):
        return self

    @classmethod
    def match(self, request_methods, url, controller, **options):
        route = HTTPRoute(
            url,
            controller,
            request_method=request_methods,
            compilers=self.compilers,
            **options
        )
        self.routes.append(route)
        return route

    @classmethod
    def group(self, *routes, **options):
        for route in routes:
            if options.get("prefix"):
                route.url = options.get("prefix") + route.url
                route.compile_route_to_regex()

            if options.get("name"):
                route._name = options.get("name") + route._name

            self.routes.append(route)
        return self.routes

    @classmethod
    def compile(self, key, to=""):
        self.compilers.update({key: to})
        return self

    @classmethod
    def set_controller_module_location(self, controller_location):
        self.controller_module_location = controller_location
